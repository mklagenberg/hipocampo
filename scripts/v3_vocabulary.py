"""Candidate V3 canonical vocabulary and conversational alias resolver."""
from __future__ import annotations

ALIASES = {
    "note": "Record",
    "nota": "Record",
    "record": "Record",
    "source": "Source",
    "fonte": "Source",
    "second brain": "Hipocampo",
    "hipocampo": "Hipocampo",
    "personal vault": "Personal Vault",
    "vault pessoal": "Personal Vault",
    "company vault": "Company Vault",
    "vault da empresa": "Company Vault",
}


def resolve_alias(utterance: str, *, context: str | None = None) -> dict[str, object]:
    normalized = " ".join(utterance.lower().strip().split())
    if normalized in {"save this in the vault", "salva isso no vault"} and not context:
        return {
            "status": "clarification_required",
            "canonical": None,
            "question": "Você quer o personal vault (vault pessoal) ou o company vault (vault da empresa)? A escolha altera entity, privacidade e destino.",
        }
    intent_aliases = {
        "create a note": "Record",
        "use the fonte": "Source",
        "send this to the second brain": "Hipocampo",
    }
    if normalized in intent_aliases:
        return {"status": "resolved", "canonical": intent_aliases[normalized], "question": None}
    canonical = ALIASES.get(normalized)
    if canonical is None:
        return {"status": "unknown", "canonical": None, "question": None}
    return {"status": "resolved", "canonical": canonical, "question": None}


def persisted_type(result: dict[str, object]) -> str | None:
    canonical = result.get("canonical")
    return str(canonical) if canonical in {"Record", "Source"} else None
