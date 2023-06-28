from typing import List
from typing_extensions import Self

from .operation_result import OperationResult

from typing import Dict, Any

import dataclasses


@dataclasses.dataclass()
class ClearSignResult(OperationResult):
    """ClearOperationResult model."""

    outputs: List[str]
    signing_key: str

    def to_dict(self: Self):
        """Return dict representation of ClearOperationResult."""
        return {"outputs": self.outputs, "signing_key": self.signing_key}

    @classmethod
    def doc_arguments(cls: OperationResult) -> Dict[str, Any]:
        """Return dictionary with arguments description of the operation."""
        doc_arguments = {
            "operation_results": {
                "type": "list",
                "description": "Signing result output",
                "returned": "always",
                "sample": ["signed:'hello world'"],
            },
            "signing_key": {
                "type": "str",
                "description": "The signing key which is used during signing.",
                "returned": "always",
                "sample": "123",
            },
        }

        return doc_arguments
