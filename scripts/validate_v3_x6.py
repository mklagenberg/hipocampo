#!/usr/bin/env python3
"""Integrated deterministic checks for the unreleased V3 X6 candidate."""
from __future__ import annotations

from pathlib import Path

from v3_event_engine import (
    EventError,
    assert_safe_event,
    build_capability_matrix,
    build_correlation,
    build_event,
    build_revocation_event,
    session_disposition,
)


ROOT = Path(__file__).resolve().parents[1]


def require(path: str, needles: list[str], errors: list[str]) -> None:
    target = ROOT / path
    if not target.exists():
        errors.append(f"missing {path}")
        return
    text = target.read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            errors.append(f"{path} is missing {needle!r}")


def main() -> int:
    errors: list[str] = []
    event = build_event(
        "validation_run",
        "durable_operational",
        actor={"executor": "local-agent", "approver": "operator"},
        target={"target_id": "fixture-001", "entity": "Gauge", "scope": "methodology"},
        payload={"result": "completed", "source_body": "private body", "token": "secret"},
        rule_revision="v3.0.0-x6.1",
        proof_scope="local-fixture",
        limits=["does not prove semantic truth"],
        retention="operational-policy",
    )
    assert_safe_event(event)
    if event["payload"]["source_body"] != "[REDACTED]" or event["payload"]["token"] != "[REDACTED]":
        errors.append("sensitive event payload was not redacted")
    if event["layer"] != "durable_operational":
        errors.append("durable event layer missing")

    discarded = session_disposition(capture_requested=False, capture_authorized=False, interrupted=True)
    if discarded["disposition"] != "discard_transient_context" or discarded["durable_log_allowed"]:
        errors.append("unauthorized session context was not discarded")
    captured = session_disposition(capture_requested=True, capture_authorized=True)
    if captured["disposition"] != "capture_authorized":
        errors.append("authorized capture was not recognized")

    correlation = build_correlation(
        correlation_id="corr-001",
        causation_id="evt-parent",
        targets=[{"kind": "Package", "id": "PKG-001"}, {"kind": "Record", "id": "REC-001"}],
        fingerprints=["sha256:package"],
        evidence_refs=["EVD-0039"],
        rule_revision="v3.0.0-x6.3",
        state="inaccessible_frontier",
        inaccessible_frontiers=[{"vault_id": "pearson-vault", "reason": "access_unavailable"}],
    )
    if not correlation["inaccessible_frontiers"] or "fingerprints" not in correlation:
        errors.append("correlation envelope is incomplete")

    matrix = build_capability_matrix([
        {"capability": "local-event-write", "state": "proven", "evidence": "git"},
        {"capability": "remote-cache-invalidation", "state": "unavailable"},
        {"capability": "external-backup-revocation", "state": "observational"},
    ])
    if len(matrix["capabilities"]) != 3:
        errors.append("capability matrix is incomplete")

    revocation = build_revocation_event(
        target_id="PKG-001",
        requester_id="mauricio",
        approver_id="mauricio",
        scope="Gauge/Liferay",
        reason_class="privacy_retraction",
        surfaces=[
            {"surface": "destination-ledger", "reachable": True, "evidence": "local-git"},
            {"surface": "remote-cache", "reachable": False, "requires_block": True},
        ],
    )
    if revocation["result"] != "partially_completed" or not any(item["blocked"] for item in revocation["reach"]):
        errors.append("partial revocation did not disclose and block unreachable use")

    require("docs/v3-operational-events-contract.md", ["durable_operational", "not a content mirror", "Redaction"], errors)
    require("docs/v3-session-cache-contract.md", ["discard_transient_context", "explicit authorization"], errors)
    require("docs/v3-crud-events-contract.md", ["CRUD", "does not contain a Record"], errors)
    require("docs/v3-correlation-contract.md", ["correlation_id", "inaccessible_frontier"], errors)
    require("docs/v3-host-capability-matrix.yaml", ["proven", "observational", "unavailable"], errors)
    require("docs/v3-revocation-contract.md", ["reach matrix", "TTL is not proof"], errors)
    require("docs/v3-x6-fixtures.yaml", ["event-sensitive-payload", "capability-unavailable", "revocation-partial-reach"], errors)
    if errors:
        print(f"validate_v3_x6: FAILED — {len(errors)} error(s)")
        for error in errors:
            print(f"  [FAIL] {error}")
        return 1
    print("validate_v3_x6: OK — events, sessions, CRUD, correlation, capabilities, redaction and revocation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
