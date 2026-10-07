#!/usr/bin/env python3
"""Synthetic content with actual Git: explicit legacy conversion and CRUD recovery."""
from copy import deepcopy
import hashlib
import json
import re
from pathlib import Path
import subprocess
import sys
import uuid

from validate_v3_migration_executor import ACTIVE_COLLECTIONS, manifest, review
from v3_crud_engine import ContractError, RecordCrud
from v3_migration_engine import LEGACY_CONTRACT, LEGACY_APPROVAL_SCOPE, context_fingerprint, validate_execution_manifest
from v3_migration_executor import run
from v3_record_store import MarkdownRecordStore, parse_record, serialize_record

SOURCE = ('---\r\nid: legacy-fixture\r\nrevision: 4\r\n'
    'custom_field: "ação 🧠"\r\nvisibility: internal\r\nsource: conversa\r\nttl: "2026-01-01"\r\nrelated: [other.md]\r\n'
    'attachment: image.png\r\n---\r\nCorpo com ação 🧠.\r\n![Imagem](image.png)\r\n').encode('utf-8')

def git(root, *args):
    return subprocess.run(['git', '-C', str(root), *args], capture_output=True,
        check=True, timeout=30).stdout

def make(root):
    (root / 'records').mkdir(parents=True)
    (root / 'records/rec-migration-001.md').write_bytes(SOURCE)
    (root / 'records/other.md').write_bytes(b'Unrelated source.\n')
    (root / 'records/image.png').write_bytes(b'synthetic-attachment\x00\xff')
    (root / 'policy.md').write_bytes(b'Synthetic scope and privacy policy.\n')
    git(root, 'init', '-b', 'main')
    git(root, 'config', 'user.name', 'Synthetic Validator')
    git(root, 'config', 'user.email', 'fixture@example.test')
    git(root, 'config', 'core.autocrlf', 'false')
    git(root, 'add', '.')
    git(root, 'commit', '-m', 'Synthetic input')
    git(root, 'checkout', '-b', 'migration/legacy-recovery-fixture')
    data = manifest(SOURCE)
    data.update(source_contract=LEGACY_CONTRACT, source_version='unknown',
        source_version_status='not_established', source_contract_status='accepted',
        source_contract_approval_ref='synthetic-route-approval', source_evidence_ref='synthetic-history',
        approval_scope=LEGACY_APPROVAL_SCOPE,
        context_files={'policy.md': hashlib.sha256((root / 'policy.md').read_bytes()).hexdigest()})
    item = data['records'][0]
    fields, body, _ = MarkdownRecordStore(root).read_legacy_document(item['source_path'])
    item.update(source_context_sha256=context_fingerprint(data['context_files']), legacy_source_evidence_ref='synthetic-schema-crosswalk')
    item['record'].update(content=body, legacy_frontmatter=fields, legacy_source_sha256=item['source_sha256'])
    return data

def ticket(root):
    folder = Path(git(root, 'rev-parse', '--absolute-git-dir').decode().strip()) / 'canonical-migration-recovery'
    files = list(folder.glob('*.json'))
    assert len(files) == 1
    raw = files[0].read_bytes()
    return json.loads(raw), hashlib.sha256(raw).hexdigest(), files[0]

def recovery_context(value, fingerprint):
    return {'human_approval': 'present', 'approved_vault_id': value['vault_id'],
        'approved_entity': value['entity'], 'approval_scope': 'canonical-migration-recovery-branch-local',
        'approval_ref': 'synthetic-exact-ticket-approval', 'procedure_ref': 'synthetic-procedure',
        'ticket_id': value['ticket_id'], 'ticket_sha256': fingerprint}

def recover(root, value, fingerprint, context=None, semantic=None):
    crud = RecordCrud(ACTIVE_COLLECTIONS, persistence=MarkdownRecordStore(root))
    return crud.recover_migration(value['ticket_id'], expected_ticket_sha256=fingerprint,
        recovery_context=context or recovery_context(value, fingerprint),
        semantic_review=semantic or review(), actor='synthetic-operator', reason='synthetic exact recovery')

def main():
    folder = Path.cwd() / '.tmp' / ('v3-legacy-recovery-' + uuid.uuid4().hex)
    folder.mkdir(parents=True)
    checks = []
    root = folder / 'roundtrip'
    data = make(root)
    assert validate_execution_manifest(data) == 'ready'
    checks.append('explicit legacy contract accepts unknown without version promotion')
    snapshot = {p: p.read_bytes() for p in root.rglob('*') if p.is_file() and '.git' not in p.relative_to(root).parts}
    scanner = subprocess.run([sys.executable,'-B',str(Path(__file__).with_name('scan_v3_queues.py')),
        '--root',str(root),'--now','2026-10-06T00:00:00'],capture_output=True,check=True,timeout=30)
    assert int(re.search(rb'frontmatter=(\d+)', scanner.stdout).group(1)) > 0 and b'staleness=1' in scanner.stdout
    checks.append('scanner observes the vault inside Git-worktree ancestor directories')
    assert run(root, data, mode='dry-run')[0] == 0
    assert all(p.read_bytes() == raw for p, raw in snapshot.items()) and not list((root/'.git').glob('canonical-migration-recovery/*'))
    checks.append('dry run writes neither Record nor recovery ticket')
    for key, value in [('source_contract_status', 'proposed'), ('source_version', '2.2.0'), ('human_approval', 'missing'),
        ('privacy', 'unknown'), ('rollback', 'missing'), ('approval_scope', 'v2.2-to-v3-branch-local'),
        ('source_evidence_ref', ''), ('context_files', {})]:
        invalid = deepcopy(data)
        invalid[key] = value
        assert run(root, invalid, mode='apply')[0] != 0
        assert (root/'records/rec-migration-001.md').read_bytes() == SOURCE
        checks.append('blocked legacy gate ' + key)
    for field, changed in [('content', 'rewritten'), ('legacy_frontmatter', {'revision': 5}), ('legacy_source_sha256', '0'*64)]:
        invalid = deepcopy(data)
        invalid['records'][0]['record'][field] = changed
        assert run(root, invalid, mode='dry-run')[0] != 0
        checks.append('blocks changed legacy binding ' + field)
    policy = root/'policy.md'
    policy.write_bytes(b'changed context')
    assert run(root, data, mode='dry-run')[0] != 0
    policy.write_bytes(snapshot[policy])
    checks.append('blocks context drift')
    absent = deepcopy(data)
    absent['context_files']['profile.md']='absent'
    absent['records'][0]['source_context_sha256']=context_fingerprint(absent['context_files'])
    assert run(root,absent,mode='dry-run')[0] == 0
    checks.append('explicit missing profile is retained as absence without role inference')
    (root/'profile.md').write_bytes(b'new profile requires reconciliation')
    assert run(root,absent,mode='dry-run')[0] != 0
    (root/'profile.md').unlink()  # This synthetic test created and owns this file.
    checks.append('appearance of an absent profile invalidates its context binding')
    invalid = deepcopy(data)
    invalid['context_files']['policy.md']='absent'
    invalid['records'][0]['source_context_sha256']=context_fingerprint(invalid['context_files'])
    assert run(root,invalid,mode='dry-run')[0] != 0
    checks.append('absence sentinel does not bypass a policy fingerprint')
    assert run(root, data, mode='unrecognized')[0] != 0
    checks.append('blocks invalid mode')
    weak = deepcopy(data)
    weak['records'][0]['record']['visibility'] = 'public'
    assert run(root,weak,mode='dry-run')[0] != 0
    checks.append('cannot weaken observed legacy visibility')
    for unsafe in ('../outside.md','.git/record.md','.backup/record.md'):
        try:
            MarkdownRecordStore(root)._path(unsafe)
        except ContractError:
            pass
        else:
            raise AssertionError('protected or escaping path must fail')
    try:
        MarkdownRecordStore(root).validate_legacy_binding(data['records'][0]['record'],
            '.tmp/record.md',data['records'][0]['source_sha256'],data['context_files'])
    except ContractError:
        pass
    else:
        raise AssertionError('direct legacy route cannot use temporary artifacts')
    checks.append('cannot target Git administration backup or direct-route temporary sources')
    code, result = run(root, data, mode='apply')
    assert code == 0 and result['written'] == 1
    value, fingerprint, path = ticket(root)
    migrated = (root/'records/rec-migration-001.md').read_bytes()
    reloaded = RecordCrud(ACTIVE_COLLECTIONS, persistence=MarkdownRecordStore(root))
    rec = reloaded.read('rec-migration-001', authorized_vault_ids=['vault-fixture'])
    assert rec['content'] == data['records'][0]['record']['content'] and rec['legacy_frontmatter'] == data['records'][0]['record']['legacy_frontmatter']
    assert rec['legacy_source_sha256'] == hashlib.sha256(SOURCE).hexdigest()
    checks.append('CRUD migration and fresh gateway preserve Unicode CRLF body and all fields')
    assert (root/'records/image.png').read_bytes() == snapshot[root/'records/image.png']
    assert rec['legacy_frontmatter']['related'] == ['other.md'] and rec['legacy_frontmatter']['attachment'] == 'image.png'
    checks.append('attachment bytes and legacy relation provenance retained')
    for key, invalid in [('approved_vault_id','foreign'),('approved_entity','foreign'),('human_approval','absent'),
        ('ticket_id','0'*32),('ticket_sha256','0'*64),('approval_ref',''),('procedure_ref','')]:
        context = recovery_context(value, fingerprint)
        context[key] = invalid
        try:
            recover(root, value, fingerprint, context)
        except ContractError:
            pass
        else:
            raise AssertionError('recovery authorization must fail closed')
        assert (root/'records/rec-migration-001.md').read_bytes() == migrated
        checks.append('blocks recovery approval ' + key)
    try:
        recover(root, value, fingerprint, semantic=review(decision='rejected'))
    except ContractError:
        pass
    else:
        raise AssertionError('rejected review must block')
    checks.append('recovery requires accepted review')
    original_ticket = path.read_bytes()
    path.write_bytes(original_ticket+b' ')
    try:
        recover(root, value, fingerprint)
    except ContractError:
        pass
    else:
        raise AssertionError('ticket drift must block')
    path.write_bytes(original_ticket)
    checks.append('immutable ticket fingerprint drift blocked')
    git(root,'checkout','-b','migration/foreign')
    try:
        recover(root, value, fingerprint)
    except ContractError:
        pass
    else:
        raise AssertionError('foreign branch must block')
    git(root,'checkout','migration/legacy-recovery-fixture')
    checks.append('foreign migration branch blocked')
    lock = root/'records/.rec-migration-001.md.crud.lock'
    lock.write_bytes(b'synthetic uncertain lock')
    try:
        recover(root, value, fingerprint)
    except ContractError:
        pass
    else:
        raise AssertionError('existing lock must block')
    assert lock.read_bytes() == b'synthetic uncertain lock'
    lock.unlink()  # This test owns this synthetic lock; no real lock is removed.
    checks.append('foreign lock blocks recovery and stays unchanged')
    target = root/'records/rec-migration-001.md'
    target.write_bytes(migrated+b'edited')
    try:
        recover(root, value, fingerprint)
    except ContractError:
        pass
    else:
        raise AssertionError('target drift must block')
    target.write_bytes(migrated)
    checks.append('changed target blocks without overwrite')
    (root/'records/other.md').write_bytes(b'unrelated dirty content')
    worker = "import json,sys;from pathlib import Path;from validate_v3_legacy_recovery import recover;print(json.dumps(recover(Path(sys.argv[1]),json.loads(sys.argv[2]),sys.argv[3])))"
    process = subprocess.run([sys.executable, '-B', '-c', worker, str(root), json.dumps(value), fingerprint],
        capture_output=True, check=True, timeout=30, cwd=Path(__file__).resolve().parents[1],
        env=__import__('os').environ | {'PYTHONPATH': str(Path(__file__).resolve().parent)})
    assert json.loads(process.stdout)['status'] == 'restored' and target.read_bytes() == SOURCE
    assert (root/'records/other.md').read_bytes() == b'unrelated dirty content'
    checks.append('new process canonical recovery is byte exact and preserves unrelated changes')
    assert recover(root, value, fingerprint)['status'] == 'source_present_no_write'
    checks.append('repeat reconciles source-present without claiming another write')
    direct = RecordCrud(ACTIVE_COLLECTIONS, persistence=MarkdownRecordStore(root))
    item = data['records'][0]
    try:
        direct.migrate(item['record'], source_path=item['source_path'], expected_source_sha256=item['source_sha256'],
            semantic_review=item['semantic_review'], migration_context=data, actor='synthetic',reason='attempt repeat', idempotency_key=item['idempotency_key'])
    except ContractError:
        pass
    else:
        raise AssertionError('old approval must not restart restored attempt')
    checks.append('persistent attempt blocks same-manifest reapply after recovery')
    late = folder/'later-update'
    later_data = make(late)
    assert run(late,later_data,mode='apply')[0] == 0
    late_ticket,late_hash,_ = ticket(late)
    updated = RecordCrud(ACTIVE_COLLECTIONS,persistence=MarkdownRecordStore(late))
    updated.update('rec-migration-001',{'content':'Later governed change'},expected_version=1,
        semantic_review=review(),actor='synthetic',reason='synthetic later update')
    late_bytes = (late/'records/rec-migration-001.md').read_bytes()
    try:
        recover(late,late_ticket,late_hash)
    except ContractError:
        pass
    else:
        raise AssertionError('later update must block rollback')
    assert (late/'records/rec-migration-001.md').read_bytes() == late_bytes
    checks.append('later V3 version blocks recovery')
    interrupted = folder/'interruption'
    interrupted_data = make(interrupted)
    original = MarkdownRecordStore.migrate
    def after_write(self,*args):
        original(self,*args)
        raise OSError('synthetic interruption after atomic write')
    MarkdownRecordStore.migrate = after_write
    try:
        assert run(interrupted,interrupted_data,mode='apply')[0] == 3
    finally:
        MarkdownRecordStore.migrate = original
    interrupted_ticket,interrupted_hash,_=ticket(interrupted)
    assert recover(interrupted,interrupted_ticket,interrupted_hash)['written'] == 1
    assert (interrupted/'records/rec-migration-001.md').read_bytes() == SOURCE
    checks.append('interruption after write reconciles and restores through CRUD')
    before = folder/'interruption-before'
    before_data = make(before)
    MarkdownRecordStore.migrate = lambda *args: (_ for _ in ()).throw(OSError('synthetic interruption before atomic write'))
    try:
        assert run(before,before_data,mode='apply')[0] == 3
    finally:
        MarkdownRecordStore.migrate = original
    before_ticket,before_hash,_=ticket(before)
    assert recover(before,before_ticket,before_hash)['status'] == 'source_present_no_write'
    checks.append('interruption before write is observed without false recovery claim')
    print(json.dumps({'class':'synthetic_content_actual_git','checks':len(checks),'passed':len(checks),
        'assertions':checks,'fixture':str(folder),'real_Record_writes':0,'real_pilot':False},ensure_ascii=False))

if __name__ == '__main__':
    main()
