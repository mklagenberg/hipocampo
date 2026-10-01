#!/usr/bin/env python3
"""Validate the V3 skill conformance suite and its release evidence envelope."""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import sys
from pathlib import Path

import yaml

from validate_compatibility import state as compatibility_state


def load_yaml(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a YAML mapping")
    return value


def parse_timestamp(value: object, label: str, errors: list[str]) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label} timestamp is required")
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"{label} timestamp must be ISO 8601")
        return None
    if parsed.tzinfo is None:
        errors.append(f"{label} timestamp must include a timezone")
        return None
    return parsed


def validate(root: Path, mode: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    blockers: list[str] = []
    cases_path = root / "docs" / "v3-skill-conformance-cases.yaml"
    review_path = root / "docs" / "v3-skill-conformance-ai-review.yaml"
    try:
        cases = load_yaml(cases_path)
        review = load_yaml(review_path)
        active_contract = load_yaml(root / "COMPATIBILITY.yaml")
    except (OSError, yaml.YAMLError, ValueError) as exc:
        return [f"cannot load conformance inputs: {exc}"], []

    review_target = review.get("review_target", {})
    package_root_value = review_target.get("package_root")
    if not isinstance(package_root_value, str) or not package_root_value:
        return ["review_target.package_root must identify the exact candidate package"], []
    package_root = (root / package_root_value).resolve()
    if root not in package_root.parents:
        return ["review_target.package_root must stay inside the repository"], []
    manifest_rel = review_target.get("skill_manifest", "manifest.yaml")
    lock_rel = review_target.get("package_lock", "package-lock.yaml")
    manifest_path = (package_root / manifest_rel).resolve()
    lock_path = (package_root / lock_rel).resolve()
    if package_root not in manifest_path.parents or package_root not in lock_path.parents:
        return ["candidate manifest and package lock must stay inside the candidate package"], []

    try:
        manifest = load_yaml(manifest_path)
        package_lock = load_yaml(lock_path)
    except (OSError, yaml.YAMLError, ValueError) as exc:
        return [f"cannot load candidate skill package: {exc}"], []

    if cases.get("schema_version") != "1.0" or cases.get("suite_id") != "v3-skill-conformance":
        errors.append("case suite has an unsupported schema or suite_id")
    if cases.get("target_methodology") != "3.0.0" or cases.get("baseline_contract") != "3.0.0":
        errors.append("case suite must target and preserve the V3.0.0 baseline")
    if cases.get("privacy") != "synthetic-only":
        errors.append("case suite must declare synthetic-only inputs")

    deterministic = cases.get("deterministic_cases", [])
    semantic = cases.get("semantic_cases", [])
    for section, items in (("deterministic", deterministic), ("semantic", semantic)):
        if not isinstance(items, list) or not items:
            errors.append(f"{section} cases must be a non-empty list")
            continue
        ids = [item.get("id") for item in items if isinstance(item, dict)]
        if len(ids) != len(items) or len(ids) != len(set(ids)) or any(not item for item in ids):
            errors.append(f"{section} case IDs must be present and unique")

    for case in deterministic:
        if not isinstance(case, dict) or not isinstance(case.get("input"), dict):
            errors.append("deterministic case must contain an input mapping")
            continue
        actual = compatibility_state(case["input"])
        if actual != case.get("expected_state"):
            errors.append(
                f"{case.get('id')}: expected {case.get('expected_state')}, got {actual}"
            )
        if not isinstance(case.get("expected_action"), str) or not case["expected_action"]:
            errors.append(f"{case.get('id')}: expected_action is required")

    for case in semantic:
        if not isinstance(case, dict) or not case.get("question") or not case.get("required_disposition"):
            errors.append("semantic case needs a question and required disposition")
            continue
        refs = case.get("contract_refs", [])
        if not refs:
            errors.append(f"{case.get('id')}: at least one contract reference is required")
        for ref in refs:
            if not (root / ref).is_file():
                errors.append(f"{case.get('id')}: missing contract reference {ref}")

    package_lock_sha256 = hashlib.sha256(lock_path.read_bytes()).hexdigest()

    skill = manifest.get("skill", {})
    skill_range = manifest.get("methodology", {}).get("compatibility", "")
    target = cases.get("target_methodology", "3.0.0")
    active_methodology_version = active_contract.get("methodology", {}).get("version")
    methodology_is_released = active_methodology_version == target
    candidate_is_released = skill.get("release_status") == "released" and bool(
        manifest.get("updates", {}).get("release_ref")
    )
    package_version = skill.get("version")
    expected_lock = review_target.get("package_lock_sha256")
    if expected_lock != package_lock_sha256:
        errors.append("AI review package-lock fingerprint is stale")
    if review_target.get("skill_version") != package_version:
        errors.append("AI review skill version does not match the candidate manifest")
    if review_target.get("methodology_compatibility") != skill_range:
        errors.append("AI review compatibility range does not match the candidate manifest")
    if str(skill.get("core_path", "")).rstrip("/\\") != package_root_value.rstrip("/\\"):
        errors.append("candidate manifest core_path does not match review_target.package_root")

    locked_package = package_lock.get("package", {})
    if locked_package.get("version") != package_version:
        errors.append("candidate package-lock version does not match the candidate manifest")
    locked_files = locked_package.get("files", [])
    expected_files: dict[str, str] = {}
    for item in locked_files:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str) or not isinstance(item.get("sha256"), str):
            errors.append("candidate package-lock entries need path and sha256")
            continue
        if Path(item["path"]).is_absolute() or ".." in Path(item["path"]).parts:
            errors.append(f"candidate package-lock path escapes candidate root: {item['path']}")
            continue
        expected_files[item["path"]] = item["sha256"]
    actual_files = {
        path.relative_to(package_root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in package_root.rglob("*")
        if path.is_file() and path != lock_path
    }
    if set(expected_files) != set(actual_files):
        errors.append("candidate package-lock file set differs from the candidate package")
    for relative, digest in actual_files.items():
        if expected_files.get(relative) != digest:
            errors.append(f"candidate package-lock hash mismatch for {relative}")

    covers_target = compatibility_state(
        {
            "sources_available": True,
            "package_integrity": True,
            "methodology_version": target,
            "skill_methodology_range": skill_range,
            "vault_range": f"^{target}",
        }
    ) == "compatible"
    readiness_review = review.get("ai_readiness_review", {})
    ai = review.get("ai_semantic_review", {})
    challenge = review.get("ai_challenge", {})
    human = review.get("human_review", {})
    semantic_ids = {item.get("id") for item in semantic if isinstance(item, dict)}
    reviewed_ids = set(ai.get("reviewed_semantic_case_ids", []))
    deterministic_observation = review.get("deterministic_observation", {})
    observed_state = compatibility_state(
        {
            "sources_available": True,
            "package_integrity": True,
            "methodology_version": target,
            "skill_methodology_range": skill_range,
            "vault_range": f"^{target}",
        }
    )
    if deterministic_observation.get("expected_compatibility_state") != observed_state:
        errors.append("recorded deterministic observation does not match the declared skill compatibility")
    if observed_state != "compatible" and deterministic_observation.get("action") != "block_durable_v3_operation":
        errors.append("incompatible skill must record the fail-closed V3 operation action")
    if observed_state == "compatible" and deterministic_observation.get("action") != "continue_subject_to_authority_and_privacy":
        errors.append("compatible tuple must preserve the separate authority and privacy gates")

    ai_reviewed_at = challenge_reviewed_at = human_reviewed_at = None
    if ai.get("status") in {"passed", "completed_with_findings"}:
        if not ai.get("review_id"):
            errors.append("completed AI semantic review must have a review_id")
        if not ai.get("reviewer_session_id"):
            errors.append("completed AI semantic review must have a reviewer_session_id")
        ai_reviewed_at = parse_timestamp(ai.get("reviewed_at"), "AI semantic review", errors)
        if ai.get("package_lock_sha256") != package_lock_sha256:
            errors.append("AI semantic review must bind to the current package-lock fingerprint")
        if reviewed_ids != semantic_ids:
            errors.append("AI semantic review must mark every semantic case as reviewed")
        dispositions = ai.get("case_dispositions", [])
        disposition_ids = [item.get("case_id") for item in dispositions if isinstance(item, dict)]
        if len(disposition_ids) != len(dispositions) or set(disposition_ids) != semantic_ids or len(disposition_ids) != len(set(disposition_ids)):
            errors.append("AI semantic review must record exactly one disposition for every semantic case")
        for item in dispositions:
            if not isinstance(item, dict):
                continue
            if not isinstance(item.get("disposition"), str) or not item["disposition"].strip():
                errors.append(f"{item.get('case_id')}: AI disposition is required")
            if not isinstance(item.get("rationale"), str) or not item["rationale"].strip():
                errors.append(f"{item.get('case_id')}: AI rationale is required")
            if not isinstance(item.get("evidence"), list) or not item["evidence"]:
                errors.append(f"{item.get('case_id')}: AI evidence references are required")
            if not isinstance(item.get("uncertainty"), str) or not item["uncertainty"].strip():
                errors.append(f"{item.get('case_id')}: AI uncertainty statement is required")
            evidence_refs = item.get("evidence")
            if isinstance(evidence_refs, list):
                for evidence_ref in evidence_refs:
                    if not isinstance(evidence_ref, str) or not evidence_ref.strip():
                        errors.append(f"{item.get('case_id')}: AI evidence references must be non-empty paths")
                        continue
                    evidence_path = evidence_ref.split("#", 1)[0]
                    if Path(evidence_path).is_absolute() or ".." in Path(evidence_path).parts:
                        errors.append(f"{item.get('case_id')}: AI evidence path escapes the repository")
                    elif not (root / evidence_path).is_file():
                        errors.append(f"{item.get('case_id')}: missing AI evidence reference {evidence_path}")
        if ai.get("status") == "passed" and ai.get("findings"):
            errors.append("AI semantic review cannot be passed while unresolved findings are recorded")
        if not ai.get("reviewer_type") == "AI":
            errors.append("semantic review must identify an AI reviewer")

    if challenge.get("status") in {"passed", "completed_with_findings"}:
        if not challenge.get("challenge_id"):
            errors.append("completed AI challenge must have a challenge_id")
        if not challenge.get("reviewer_session_id"):
            errors.append("completed AI challenge must have a reviewer_session_id")
        challenge_reviewed_at = parse_timestamp(challenge.get("reviewed_at"), "AI challenge", errors)
        if challenge.get("reviewed_ai_review_id") != ai.get("review_id") or not ai.get("review_id"):
            errors.append("AI challenge must identify the completed primary AI review")
        if challenge.get("package_lock_sha256") != package_lock_sha256:
            errors.append("AI challenge must bind to the current package-lock fingerprint")
        if challenge.get("reviewer_type") != "AI":
            errors.append("challenge must identify an AI reviewer")
        if challenge.get("reviewer_session_id") == ai.get("reviewer_session_id"):
            errors.append("AI challenge must use a separate reviewer session")
        if not isinstance(challenge.get("conclusion"), str) or not challenge["conclusion"].strip():
            errors.append("AI challenge conclusion is required")
        challenged_ids = set(challenge.get("challenged_semantic_case_ids", []))
        if challenged_ids != semantic_ids:
            errors.append("AI challenge must cover every semantic case")
        case_challenges = challenge.get("case_challenges", [])
        challenge_ids = [item.get("case_id") for item in case_challenges if isinstance(item, dict)]
        if len(challenge_ids) != len(case_challenges) or set(challenge_ids) != semantic_ids or len(challenge_ids) != len(set(challenge_ids)):
            errors.append("AI challenge must record exactly one challenge disposition for every semantic case")
        for item in case_challenges:
            if not isinstance(item, dict):
                continue
            if item.get("disposition") not in {"stands", "revise", "needs_human"}:
                errors.append(f"{item.get('case_id')}: invalid AI challenge disposition")
            if not isinstance(item.get("rationale"), str) or not item["rationale"].strip():
                errors.append(f"{item.get('case_id')}: AI challenge rationale is required")
            if not isinstance(item.get("evidence"), list) or not item["evidence"]:
                errors.append(f"{item.get('case_id')}: AI challenge evidence references are required")
            elif isinstance(item.get("evidence"), list):
                for evidence_ref in item["evidence"]:
                    if not isinstance(evidence_ref, str) or not evidence_ref.strip():
                        errors.append(f"{item.get('case_id')}: AI challenge evidence must be a non-empty path")
                        continue
                    evidence_path = evidence_ref.split("#", 1)[0]
                    if Path(evidence_path).is_absolute() or ".." in Path(evidence_path).parts:
                        errors.append(f"{item.get('case_id')}: AI challenge evidence path escapes the repository")
                    elif not (root / evidence_path).is_file():
                        errors.append(f"{item.get('case_id')}: missing AI challenge evidence reference {evidence_path}")
        if challenge.get("status") == "passed" and any(
            item.get("disposition") != "stands" for item in case_challenges if isinstance(item, dict)
        ):
            errors.append("AI challenge cannot pass while any case is marked revise or needs_human")
        if ai_reviewed_at and challenge_reviewed_at and challenge_reviewed_at <= ai_reviewed_at:
            errors.append("AI challenge timestamp must follow the primary AI semantic review")

    if human.get("status") == "approved":
        human_reviewed_at = parse_timestamp(human.get("reviewed_at"), "human review", errors)
        if not isinstance(human.get("reviewer"), str) or not human["reviewer"].strip():
            errors.append("human approval must identify the reviewer")
        if human.get("reviewed_ai_review_id") != ai.get("review_id") or not ai.get("review_id"):
            errors.append("human decision must identify the primary AI semantic review")
        if human.get("reviewed_ai_challenge_id") != challenge.get("challenge_id") or not challenge.get("challenge_id"):
            errors.append("human decision must identify the AI challenge review")
        if ai_reviewed_at and human_reviewed_at and human_reviewed_at <= ai_reviewed_at:
            errors.append("human review timestamp must follow the primary AI semantic review")
        if challenge_reviewed_at and human_reviewed_at and human_reviewed_at <= challenge_reviewed_at:
            errors.append("human review timestamp must follow the AI challenge")

    if mode == "release":
        if not methodology_is_released:
            blockers.append(f"methodology target {target} is not the active released version ({active_methodology_version})")
        if not candidate_is_released:
            blockers.append("candidate manifest does not identify an immutable released skill package")
        if not covers_target:
            blockers.append(f"skill compatibility {skill_range!r} does not cover V3.0.0")
        if ai.get("status") != "passed" or reviewed_ids != semantic_ids:
            blockers.append("AI semantic review must pass and cover every semantic case")
        if challenge.get("status") != "passed":
            blockers.append("AI challenge pass must pass after reviewing the primary AI assessment")
        if human.get("status") != "approved" or not human.get("decision"):
            blockers.append("human review must be recorded after the AI stages")
        if review.get("assessment_status") != "ready":
            blockers.append("AI review record does not declare release readiness")
    elif mode == "workflow":
        assessment = review.get("assessment_status")
        if assessment not in {"blocked", "ready"}:
            errors.append("assessment_status must be blocked or ready")
        if readiness_review.get("status") not in {"completed", "completed_with_blocker"}:
            errors.append("AI readiness review status must be recorded")
        if assessment == "ready" and not covers_target:
            errors.append("review says ready although the skill compatibility range excludes V3.0.0")
        if assessment == "ready" and (not methodology_is_released or not candidate_is_released or reviewed_ids != semantic_ids or ai.get("status") != "passed" or challenge.get("status") != "passed" or human.get("status") != "approved"):
            errors.append("ready assessment requires complete AI, challenge and human approval")
        if not methodology_is_released:
            blockers.append(f"methodology target {target} is not the active released version ({active_methodology_version})")
        if not candidate_is_released:
            blockers.append("candidate remains unreleased and cannot be installed")
        if not covers_target:
            blockers.append(f"skill compatibility {skill_range!r} does not cover V3.0.0")
        if ai.get("status") != "passed":
            blockers.append("AI semantic review is not passed for every semantic case")
        if challenge.get("status") != "passed":
            if challenge.get("status") == "not_run_pending_independent_ai_session":
                blockers.append("independent AI challenge session is pending")
            else:
                blockers.append("AI challenge is not passed")
        if human.get("status") != "approved":
            blockers.append("human review remains pending")
        if ai.get("status") == "not_run_no_v3_compatible_skill_candidate":
            if reviewed_ids:
                errors.append("semantic review marked not-run must not claim reviewed cases")
            if challenge.get("status") != "not_run_no_ai_semantic_review":
                errors.append("AI challenge must not be claimed before an AI semantic review")
            blockers.append("no V3-compatible skill candidate is available for semantic cases")
        elif ai.get("status") not in {"passed", "completed_with_findings"}:
            errors.append("AI semantic review must be completed or explicitly not run")
        elif challenge.get("status") not in {"passed", "completed_with_findings", "not_run_pending_independent_ai_session"}:
            errors.append("AI challenge must complete after the AI semantic review")
        if human.get("status") not in {"pending", "approved"}:
            errors.append("human review status must be pending or approved")

    return errors, blockers


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--mode", choices=("workflow", "release"), default="workflow")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    errors, blockers = validate(root, args.mode)

    if errors:
        print(f"validate_v3_skill_conformance: FAILED — {len(errors)} error(s)")
        for error in errors:
            print(f"  [FAIL] {error}")
        return 1
    if args.mode == "release" and blockers:
        print(f"validate_v3_skill_conformance: BLOCKED — {len(blockers)} release blocker(s)")
        for blocker in blockers:
            print(f"  [BLOCK] {blocker}")
        return 2
    if blockers:
        print(f"validate_v3_skill_conformance: OK — suite and evidence envelope valid; {len(blockers)} release blocker(s) remain")
    else:
        print("validate_v3_skill_conformance: OK — suite and review evidence are complete")
    print("  Semantic conclusions remain subject to human review.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
