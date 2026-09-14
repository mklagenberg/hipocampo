#!/usr/bin/env python3
"""In-memory V3 Artifact and material-representation contract primitives."""
from __future__ import annotations

from copy import deepcopy
from hashlib import sha256


VISIBILITY_RANK = {"public": 0, "internal": 1, "confidential": 2, "restricted": 3}
ACCESSIBILITY = {"available", "unavailable", "restricted"}
REPRESENTATION_KINDS = {
    "summary", "excerpt", "transcription", "preview", "structured_description", "manifest"
}


class ArtifactContractError(ValueError):
    pass


def source_hash(content: str) -> str:
    return sha256(content.encode("utf-8")).hexdigest()


def _rank(value: str) -> int:
    if value not in VISIBILITY_RANK:
        raise ArtifactContractError(f"unknown visibility: {value}")
    return VISIBILITY_RANK[value]


def validate_artifact(artifact: dict) -> dict:
    required = {"artifact_id", "role", "version", "reference", "accessibility", "visibility"}
    missing = required - artifact.keys()
    if missing:
        raise ArtifactContractError(f"missing Artifact fields: {sorted(missing)}")
    if not artifact["artifact_id"] or artifact["version"] < 1 or not artifact["reference"]:
        raise ArtifactContractError("Artifact identity, version and reference are required")
    if artifact["accessibility"] not in ACCESSIBILITY:
        raise ArtifactContractError("unknown Artifact accessibility")
    _rank(artifact["visibility"])
    if artifact.get("source_hash") and len(artifact["source_hash"]) != 64:
        raise ArtifactContractError("source_hash must be a SHA-256 hexadecimal digest")
    destination = artifact.get("external_destination")
    if destination and (not destination.get("provider") or not destination.get("reference")):
        raise ArtifactContractError("external destination requires provider and reference")
    return deepcopy(artifact)


def validate_artifact_link(record: dict, artifact: dict, link: dict) -> dict:
    validate_artifact(artifact)
    if link.get("artifact_id") != artifact["artifact_id"]:
        raise ArtifactContractError("Artifact link identity does not match Artifact")
    if link.get("version") != artifact["version"]:
        raise ArtifactContractError("Artifact link version does not match Artifact")
    if link.get("source_hash") and artifact.get("source_hash") and link["source_hash"] != artifact["source_hash"]:
        raise ArtifactContractError("Artifact link hash does not match Artifact")
    if _rank(record["visibility"]) < _rank(artifact["visibility"]):
        raise ArtifactContractError("Record visibility is weaker than Artifact visibility")
    representation = link.get("representation")
    if link.get("semantic_required") and not representation:
        raise ArtifactContractError("semantic Artifact requires material representation")
    if representation:
        if not representation.get("content"):
            raise ArtifactContractError("material representation requires content")
        if representation.get("kind") not in REPRESENTATION_KINDS:
            raise ArtifactContractError("unknown material representation kind")
        if representation.get("artifact_version") != artifact["version"]:
            raise ArtifactContractError("representation version does not match Artifact")
        if artifact.get("source_hash") and representation.get("artifact_hash") != artifact["source_hash"]:
            raise ArtifactContractError("representation hash does not match Artifact")
        if _rank(representation.get("visibility", "public")) < _rank(record["visibility"]):
            raise ArtifactContractError("representation visibility weakens Record visibility")
        if _rank(representation.get("visibility", "public")) < _rank(artifact["visibility"]):
            raise ArtifactContractError("representation visibility weakens Artifact visibility")
    return deepcopy(link)


def validate_record_artifacts(record: dict, artifacts: dict[str, dict]) -> dict:
    updated = deepcopy(record)
    for link in updated.get("artifacts", []):
        artifact = artifacts.get(link.get("artifact_id"))
        if artifact is None:
            raise ArtifactContractError("Record references missing Artifact")
        validate_artifact_link(updated, artifact, link)
    return updated


def update_artifact(artifact: dict, *, version: int, content_hash: str | None = None, accessibility: str | None = None) -> dict:
    updated = deepcopy(artifact)
    if version <= artifact["version"]:
        raise ArtifactContractError("Artifact versions must increase monotonically")
    updated["version"] = version
    if content_hash is not None:
        updated["source_hash"] = content_hash
    if accessibility is not None:
        updated["accessibility"] = accessibility
    validate_artifact(updated)
    return updated


def mark_divergence(record: dict, artifact: dict) -> dict:
    updated = deepcopy(record)
    for link in updated.get("artifacts", []):
        if link.get("artifact_id") == artifact["artifact_id"]:
            link["review_required"] = link.get("version") != artifact["version"] or (
                link.get("source_hash") and artifact.get("source_hash") and link["source_hash"] != artifact["source_hash"]
            )
            link["available_version"] = artifact["version"]
            return updated
    raise ArtifactContractError("Artifact not linked by Record")


def reconstruct_used_version(record: dict, artifact_versions: dict[tuple[str, int], dict], artifact_id: str) -> dict:
    link = next((item for item in record.get("artifacts", []) if item.get("artifact_id") == artifact_id), None)
    if link is None:
        raise ArtifactContractError("Artifact is not linked by Record")
    versioned = artifact_versions.get((artifact_id, link.get("version")))
    if versioned is None or versioned.get("accessibility") != "available":
        raise ArtifactContractError("used Artifact version is unavailable")
    validate_artifact(versioned)
    if link.get("source_hash") and versioned.get("source_hash") != link["source_hash"]:
        raise ArtifactContractError("used Artifact version hash diverges")
    return deepcopy(versioned)
