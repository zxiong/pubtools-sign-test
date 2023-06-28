from __future__ import annotations

from abc import ABC

from dataclasses import dataclass
from typing import ClassVar, Dict, Any

from ..results.operation_result import OperationResult


@dataclass
class SignOperation(ABC):
    """SignOperation Abstract class."""

    ResultType: ClassVar[OperationResult]

    @classmethod
    def doc_arguments(cls: SignOperation) -> Dict[str, Any]:
        """Return dictionary with arguments description of the operation."""
        doc_arguments = {}
        options_arguments_doc = {}
        exmaple_arguments_doc = {}

        for fn, fv in cls.__dataclass_fields__.items():
            if fv.metadata.get("description"):
                options_arguments_doc[fn] = {
                    field: fv.metadata[field] for field in fv.metadata if field != "sample"
                }
                exmaple_arguments_doc[fn] = fv.metadata.get("sample", "")
        doc_arguments["options"] = options_arguments_doc
        doc_arguments["examples"] = exmaple_arguments_doc

        return doc_arguments
