#!/usr/bin/env python3
"""Exercise the V3 Artifact, representation and provenance contract."""
from __future__ import annotations

import argparse
from copy import deepcopy
from pathlib import Path

import yaml

from v3_artifact_engine import (
    ArtifactContractError,
    mark_divergence,
    reconstruct_used_version,
    read_record_prose,
    source_hash,
    update_artifact,
    validate_record_artifacts,
)


def expect_block(callback, label: str, errors: list[str]) -> None:
    try:
        callback()
    except ArtifactContractError:
        return
    errors.append(f"{label}: expected contract block")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    fixture = yaml.safe_load((root / "docs/v3-artifact-fixtures.yaml").read_text(encoding="utf-8"))
    errors: list[str] = []
    if len(fixture.get("cases", [])) != 11:
        errors.append("expected eleven Artifact fixtures")

    digest = source_hash("sanitized artifact version one")
    artifact = {
        "artifact_id": "art-001", "role": "evidence", "version": 1,
        "reference": "liferay://sanitized/reference", "source_kind": "external-storage",
        "source_hash": digest, "accessibility": "available", "visibility": "internal",
        "external_destination": {"provider": "s3", "reference": "bucket/key-placeholder"},
    }
    record = {
        "record_id": "rec-001", "visibility": "internal",
        "content": "The sanitized Record preserves the Artifact contribution in prose.",
        "artifacts": [{
            "artifact_id": "art-001", "role": "evidence", "version": 1,
            "source_hash": digest,
            "representation": {
                "kind": "summary", "format": "prose", "content": "Sanitized representation only.",
                "artifact_version": 1, "artifact_hash": digest,
                "generated_at": "2026-09-05T12:00:00Z", "visibility": "internal",
            },
            "limitation": "Original bytes are not stored here.",
        }],
    }
    try:
        validate_record_artifacts(record, {"art-001": artifact})
    except ArtifactContractError as exc:
        errors.append(f"valid represented Artifact was blocked: {exc}")

    reference_only = deepcopy(record)
    reference_only["artifacts"][0].pop("representation")
    expect_block(lambda: validate_record_artifacts(reference_only, {"art-001": artifact}), "semantic reference only", errors)

    missing = deepcopy(record)
    expect_block(lambda: validate_record_artifacts(missing, {}), "missing Artifact", errors)
    try:
        if read_record_prose(missing) != record["content"]:
            errors.append("Record prose changed while Artifact resolution was unavailable")
    except ArtifactContractError as exc:
        errors.append(f"Record prose was incorrectly coupled to Artifact resolution: {exc}")

    artifact_v2 = update_artifact(artifact, version=2, content_hash=source_hash("sanitized artifact version two"))
    diverged = mark_divergence(record, artifact_v2)
    if not diverged["artifacts"][0].get("review_required") or diverged["artifacts"][0]["version"] != 1:
        errors.append("Artifact divergence did not preserve used version and review flag")

    versions = {("art-001", 1): artifact, ("art-001", 2): artifact_v2}
    try:
        reconstructed = reconstruct_used_version(record, versions, "art-001")
        if reconstructed["version"] != 1 or reconstructed["source_hash"] != digest:
            errors.append("reconstruction returned the wrong Artifact version")
    except ArtifactContractError as exc:
        errors.append(f"used Artifact reconstruction failed: {exc}")

    unavailable = deepcopy(artifact)
    unavailable["accessibility"] = "restricted"
    try:
        validate_record_artifacts(record, {"art-001": unavailable})
    except ArtifactContractError:
        errors.append("restricted Artifact should remain representable with explicit limitation")

    weak_representation = deepcopy(record)
    weak_representation["artifacts"][0]["representation"]["visibility"] = "public"
    expect_block(lambda: validate_record_artifacts(weak_representation, {"art-001": artifact}), "weaker representation visibility", errors)

    public_record = deepcopy(record)
    public_record["visibility"] = "public"
    expect_block(lambda: validate_record_artifacts(public_record, {"art-001": artifact}), "weaker Record visibility", errors)

    unavailable_versions = {("art-001", 1): unavailable}
    expect_block(lambda: reconstruct_used_version(record, unavailable_versions, "art-001"), "unavailable reconstruction", errors)

    if diverged["artifacts"][0]["representation"]["artifact_version"] != 1:
        errors.append("Artifact update silently rewrote Record representation")

    mismatched = deepcopy(record)
    mismatched["artifacts"][0]["source_hash"] = source_hash("different")
    expect_block(lambda: validate_record_artifacts(mismatched, {"art-001": artifact}), "divergent hash", errors)

    no_format = deepcopy(record)
    no_format["artifacts"][0]["representation"].pop("format")
    expect_block(lambda: validate_record_artifacts(no_format, {"art-001": artifact}), "non-prose representation", errors)

    if errors:
        print(f"validate_v3_artifacts: FAILED — {len(errors)} error(s)")
        for error in errors:
            print(f"  [FAIL] {error}")
        return 1
    print("validate_v3_artifacts: OK — prose Record content, Artifact limits, hashes, version drift, and audit reconstruction")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
