# Codex adapter

Use the portable `SKILL.md` and the repository as the operational source of truth. This adapter declares only Codex-specific local state and tool boundaries.

## Local state

Store the single bootstrap pointer outside the packaged source in `hipocampo.local.yaml` beside the installed skill:

```yaml
anchor_repository: "owner/private-personal-anchor"
```

This file is client-local, contains no router or identity table, and must never be committed to an instance repository. If it is absent, run Bootstrap; if the anchor repository is unreachable, report the failure and do not overwrite the pointer.

## GitHub operations

Read the target repository's `AGENTS.md` and `hipocampo.yaml` before content operations. Use GitHub-aware tools for remote changes; do not infer that local validation proves remote publication. Repository content overrides this adapter and every locally cached value.

## Updates

On first activation, read the canonical `skill/manifest.yaml`. Reuse a successful normal check for at most `P7D` and a security check for at most `P1D`; when unavailable, report `offline` and continue only with safe repository reads. The manifest's skill version is independent from the methodology version. For an offered update, compare the installed package against `skill/package-lock.yaml` from the immutable `updates.release_ref` tag; do not treat `source_commit` as a self-referential update hash and do not install from unverified `main` content. Store only `installed_skill_version`, `installed_package_hash`, and `last_checked` beside the local anchor pointer. Notify, present the change, and wait for confirmation. Never self-update or overwrite the local-state file.
