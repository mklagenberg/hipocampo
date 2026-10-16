#!/usr/bin/env python3
"""Meaningful package integrity and nested-worktree link regressions; synthetic only."""
from pathlib import Path
import argparse, copy, hashlib, json, uuid
import subprocess
from datetime import datetime, timedelta, timezone
from unittest.mock import patch
import yaml
from validate_skill_package import validate
from validate_hipocampo import check_internal_links


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',default='.')
    args=parser.parse_args();root=Path(args.root).resolve();results=[]
    tmp_root=root/'.tmp';tmp_root.mkdir(exist_ok=True)
    temp=tmp_root/('v3-release-regression-'+uuid.uuid4().hex)
    temp.mkdir()
    # Preserve these synthetic fixtures; do not edit ACLs or delete failed
    # TemporaryDirectory instances whose Windows permissions were inaccessible.
    # Verify the absolute cleanup target before any recursive cleanup.
    if Path(temp).resolve().parent != tmp_root.resolve():
        raise ValueError('fixture cleanup boundary mismatch')
    # Reuse the actual enclosing .git boundary when this is a managed
    # worktree. Else create the synthetic Git administration via Git itself.
    if '.git' in root.parts:
        target=Path(temp)/'fixture'
    else:
        subprocess.run(['git','init','--quiet',temp],check=True,capture_output=True)
        target=Path(temp)/'.git'/'worktrees'/'fixture'
    skill=target/'skill';skill.mkdir(parents=True)
    (skill/'SKILL.md').write_bytes(b'# Synthetic skill\n')
    manifest={'skill':{'name':'hipocampo','version':'2.0.0','core_path':'skill/'}}
    contract={'skill':{'required_version':'2.0.0'}}
    lock={'package':{'version':'2.0.0','hash_algorithm':'sha256','files':[
        {'path':'SKILL.md','sha256':hashlib.sha256((skill/'SKILL.md').read_bytes()).hexdigest()},
        {'path':'manifest.yaml','sha256':''}]}}
    def reset():
        (skill/'manifest.yaml').write_text(yaml.safe_dump(manifest),encoding='utf-8')
        (target/'COMPATIBILITY.yaml').write_text(yaml.safe_dump(contract),encoding='utf-8')
        fresh=copy.deepcopy(lock);fresh['package']['files'][1]['sha256']=hashlib.sha256((skill/'manifest.yaml').read_bytes()).hexdigest()
        (skill/'package-lock.yaml').write_text(yaml.safe_dump(fresh),encoding='utf-8');return fresh
    def check(name, expected_invalid):
        errors=validate(target)
        if bool(errors)!=expected_invalid:raise AssertionError((name,errors))
        results.append({'case':name,'passed':True})
    reset();check('valid stable V3 package',False)
    for name, mutate in [
        ('lock version drift',lambda x:x['package'].update(version='1.3.0')),
        ('duplicate locked path',lambda x:x['package']['files'].append(copy.deepcopy(x['package']['files'][0]))),
        ('parent traversal',lambda x:x['package']['files'][0].update(path='../secret.md')),
        ('Windows path traversal',lambda x:x['package']['files'][0].update(path='..\\secret.md')),
        ('absolute Windows path',lambda x:x['package']['files'][0].update(path='C:/secret.md')),
        ('empty inventory',lambda x:x['package'].update(files=[])),
        ('bad digest',lambda x:x['package']['files'][0].update(sha256='invalid')),
        ('undeclared omission',lambda x:x['package']['files'].pop()),
    ]:
        fresh=reset();mutate(fresh);(skill/'package-lock.yaml').write_text(yaml.safe_dump(fresh),encoding='utf-8');check(name,True)
    reset();(skill/'SKILL.md').write_bytes(b'# Changed without relock\n');check('content drift',True)
    (skill/'SKILL.md').write_bytes(b'# Synthetic skill\n');reset()
    (skill/'unlisted.md').write_bytes(b'unlisted');check('unlisted file',True);(skill/'unlisted.md').unlink()
    reset();(skill/'manifest.yaml').write_text('skill: []\n',encoding='utf-8');check('malformed manifest rejected without crash',True)
    reset();(target/'COMPATIBILITY.yaml').write_text('skill:\n  required_version: 2.1.0\n',encoding='utf-8');check('tuple version mismatch',True)
    # The former absolute .git path filter silently skipped every file.
    (target/'README.md').write_text('[missing](missing.md)\n',encoding='utf-8')
    errors=[];warnings=[];check_internal_links(target,errors,warnings)
    assert any('missing.md' in error for error in errors),errors
    results.append({'case':'nested .git working-copy missing link detected','passed':True})
    (target/'missing.md').write_text('# Present\n',encoding='utf-8');errors=[];warnings=[];check_internal_links(target,errors,warnings);assert not errors,errors
    results.append({'case':'nested .git working-copy valid link accepted','passed':True})
    (target/'.tmp').mkdir();(target/'.tmp/ignored.md').write_text('[fixture](absent.md)\n',encoding='utf-8')
    errors=[];warnings=[];check_internal_links(target,errors,warnings);assert not errors,errors
    results.append({'case':'temporary fixture boundary excluded, source still checked','passed':True})
    # Use the actual completed AI envelopes; human approvals below exist only
    # as in-memory synthetic inputs, never as a repository or chat decision.
    import validate_v3_skill_conformance as gate
    review_path=root/'docs/v3-skill-conformance-ai-review.yaml'
    actual=yaml.safe_load(review_path.read_text(encoding='utf-8'))
    if actual.get('schema_version') == '2.0':
        from v3_distribution import make_inventory
        now=datetime.now(timezone.utc)
        payload=make_inventory(root)['payload_sha256']
        ids=[item['id'] for item in yaml.safe_load((root/'docs/v3-skill-conformance-cases.yaml').read_text(encoding='utf-8'))['semantic_cases']]
        required=yaml.safe_load((root/'skill/manifest.yaml').read_text(encoding='utf-8'))['runtime']['required_host_modes']
        receipt={'payload_sha256':payload,'host_observations':[{'mode':mode,'status':'passed','payload_sha256':payload,'evidence':'synthetic fixture only'} for mode in required]}
        for i,role in enumerate(('ai_review','independent_challenge','human_approval')):
            receipt[role]={'status':'approved' if role=='human_approval' else 'passed','identity':'synthetic-only',
                'session':role+'-synthetic-session','evidence':'synthetic fixture; not actual approval',
                'payload_sha256':payload,'at':(now+timedelta(seconds=i)).isoformat(),'semantic_case_ids':ids}
        errors,blockers=gate.validate(root,'release')
        assert not errors and blockers,(errors,blockers)
        results.append({'case':'current source routes final review externally without claiming approval','passed':True})
        errors,blockers=gate.validate(root,'release',receipt)
        assert not errors and not blockers,(errors,blockers)
        results.append({'case':'complete synthetic external receipt passes before tag exists','passed':True})
        for label,mutate in [
            ('wrong full payload',lambda v:v.update(payload_sha256='0'*64)),
            ('missing final human approval',lambda v:v.pop('human_approval')),
            ('stale human payload',lambda v:v['human_approval'].update(payload_sha256='0'*64)),
            ('human before challenge',lambda v:v['human_approval'].update(at=v['ai_review']['at'])),
            ('same AI session',lambda v:v['independent_challenge'].update(session=v['ai_review']['session'])),
            ('missing evidence',lambda v:v['human_approval'].pop('evidence')),
            ('missing semantic coverage',lambda v:v['independent_challenge'].update(semantic_case_ids=[])),
            ('missing declared host',lambda v:v.update(host_observations=v['host_observations'][:-1])),
        ]:
            changed=copy.deepcopy(receipt);mutate(changed);errors,blockers=gate.validate(root,'release',changed)
            assert errors or blockers,label
            results.append({'case':label,'passed':True})
        print(json.dumps({'suite':'v3-release-regressions','privacy':'synthetic-only','passed':len(results),'cases':results},ensure_ascii=False))
        return 0
    real_loader=gate.load_yaml
    def gate_fixture(value):
        with patch.object(gate,'load_yaml',side_effect=lambda p: value if p==review_path else real_loader(p)):
            return gate.validate(root,'release')
    errors,blockers=gate_fixture(actual)
    assert not errors,(errors,blockers)
    if actual.get('human_review',{}).get('status')=='approved':
        assert not blockers,blockers
    else:
        assert any('human' in item for item in blockers),blockers
    results.append({'case':'actual envelope respects its recorded human decision','passed':True})
    pending=copy.deepcopy(actual);pending['assessment_status']='blocked'
    pending['human_review']={'status':'pending','decision':None,
        'package_lock_sha256':actual['review_target']['package_lock_sha256']}
    errors,blockers=gate_fixture(pending)
    assert not errors and any('human' in item for item in blockers),(errors,blockers)
    results.append({'case':'synthetic pending human decision remains blocked after real acceptance','passed':True})
    fixture=copy.deepcopy(actual);fixture['assessment_status']='ready'
    challenge=fixture['ai_challenge']
    challenge['status']='passed'
    challenge['reviewer_session_id']='synthetic-challenge-session'
    challenge['reviewed_at']=datetime.now(timezone.utc).isoformat()
    challenge['reviewed_ai_review_id']=fixture['ai_semantic_review']['review_id']
    challenge['package_lock_sha256']=fixture['review_target']['package_lock_sha256']
    challenge['reviewer_type']='AI'
    challenge['conclusion']='Synthetic validator fixture only; not an actual challenge approval.'
    challenge['challenged_semantic_case_ids']=list(fixture['ai_semantic_review']['reviewed_semantic_case_ids'])
    challenge['case_challenges']=[
        {'case_id':case_id,'disposition':'stands','rationale':'Synthetic validator input only.',
         'evidence':['skill/references/v3-operation.md']}
        for case_id in challenge['challenged_semantic_case_ids']
    ]
    fixture['human_review']={
        'status':'approved','reviewer':'synthetic fixture only',
        'decision':'synthetic validator input, not a real approval',
        'reviewed_at':(datetime.now(timezone.utc)+timedelta(seconds=2)).isoformat(),
        'reviewed_ai_review_id':fixture['ai_semantic_review']['review_id'],
        'reviewed_ai_challenge_id':fixture['ai_challenge']['challenge_id'],
        'package_lock_sha256':fixture['review_target']['package_lock_sha256']}
    errors,blockers=gate_fixture(fixture);assert not errors and not blockers,(errors,blockers)
    results.append({'case':'complete synthetic review envelope validates without publication claim','passed':True})
    for name,mutate in [
        ('missing human package binding',lambda v:v['human_review'].pop('package_lock_sha256')),
        ('stale human package binding',lambda v:v['human_review'].update(package_lock_sha256='0'*64)),
        ('human before independent challenge',lambda v:v['human_review'].update(reviewed_at=v['ai_semantic_review']['reviewed_at'])),
        ('same AI reviewer session',lambda v:v['ai_challenge'].update(reviewer_session_id=v['ai_semantic_review']['reviewer_session_id'])),
        ('missing human decision',lambda v:v['human_review'].update(decision=None)),
        ('stale AI package binding',lambda v:v['ai_semantic_review'].update(package_lock_sha256='0'*64)),
    ]:
        altered=copy.deepcopy(fixture);mutate(altered);errors,blockers=gate_fixture(altered)
        assert errors or blockers,name
        results.append({'case':name,'passed':True})
    for proposed_version, expected_blocked in [('3.1.0',False),('3.0.1',False),('4.0.0',True)]:
        contract_path=root/'COMPATIBILITY.yaml';altered_contract=real_loader(contract_path)
        altered_contract['methodology']['version']=proposed_version
        with patch.object(gate,'load_yaml',side_effect=lambda p: fixture if p==review_path else altered_contract if p==contract_path else real_loader(p)):
            errors,blockers=gate.validate(root,'release')
        assert not errors and bool(blockers)==expected_blocked,(proposed_version,errors,blockers)
        results.append({'case':'synthetic methodology '+proposed_version+' preserves or rejects V3 baseline','passed':True})
    print(json.dumps({'suite':'v3-release-regressions','privacy':'synthetic-only','passed':len(results),'cases':results},ensure_ascii=False))
    return 0

if __name__=='__main__':raise SystemExit(main())
