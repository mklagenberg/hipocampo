#!/usr/bin/env python3
"""Distributed privacy gates before information passages for V3 X4.4."""
from __future__ import annotations


PASSAGES = {"retrieval", "compilation", "injection", "export", "cache", "embedding", "telemetry", "external_processing"}


def evaluate_privacy_gate(context: dict) -> dict:
    passage = context.get("passage")
    if passage not in PASSAGES:
        return _block("unknown_passage")
    if not context.get("identity") or not context.get("destination") or not context.get("purpose"):
        return _block("missing_boundary_context")
    if not context.get("boundary_evaluable", True):
        return _block("boundary_not_evaluable")
    if context.get("contains_secret") and not context.get("secret_authorized", False):
        return _block("secret_not_authorized")
    if context.get("derived_restricted") and not context.get("derived_authorized", False):
        return _block("derived_restriction")
    if context.get("revealing_metadata") and not context.get("metadata_authorized", False):
        return _block("revealing_metadata")
    if context.get("minimized") is not True:
        return _block("minimization_missing")
    if passage == "external_processing" and not context.get("environment_authorized", False):
        return _block("external_environment_unauthorized")
    return {
        "outcome": "permitido",
        "allowed": True,
        "passage": passage,
        "trace": {"identity": context["identity"], "destination": context["destination"], "purpose": context["purpose"]},
        "content_disclosed": False,
    }


def evaluate_pipeline(context: dict, passages: list[str]) -> dict:
    results = [evaluate_privacy_gate({**context, "passage": passage}) for passage in passages]
    return {"allowed": all(item["allowed"] for item in results), "results": results}


def _block(rule: str) -> dict:
    return {"outcome": "bloqueado", "allowed": False, "rule": rule, "content_disclosed": False}
