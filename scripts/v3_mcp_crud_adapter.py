#!/usr/bin/env python3
"""Logical MCP adapter for the V3 canonical Record CRUD gateway."""
from __future__ import annotations

from copy import deepcopy

from v3_crud_engine import ContractError, RecordCrud


class McpCrudError(ValueError):
    pass


class McpCrudAdapter:
    """Expose only CRUD operations to an MCP caller.

    This is a transport-shaped test adapter, not a GitHub connector. The
    important property is that an MCP request cannot obtain a direct write
    handle or bypass RecordCrud.
    """

    ALLOWED_OPERATIONS = {"create", "read", "update", "delete"}

    def __init__(self, crud: RecordCrud):
        self.crud = crud

    def call(self, request: dict) -> dict:
        operation = request.get("operation")
        if operation not in self.ALLOWED_OPERATIONS:
            raise McpCrudError("MCP exposes only canonical CRUD operations")
        try:
            result = self.crud.apply(deepcopy(request))
        except (ContractError, TypeError, KeyError) as exc:
            raise McpCrudError(str(exc)) from exc
        result["transport"] = "mcp"
        result["crud_boundary"] = True
        return result
