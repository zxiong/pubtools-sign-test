from __future__ import annotations
from abc import ABC, abstractmethod
import dataclasses
from typing import Dict, List, Any

from ..results.signing_results import SigningResults
from ..operations.base import SignOperation


@dataclasses.dataclass
class Signer(ABC):
    """Abstract Signer class."""

    @abstractmethod
    def load_config(self: Signer, config_data: Dict[str, Any]) -> None:
        """Load configuration to the Signer.

        :param config_data: Dict with configuration data.
        :type config_data: Dict[str, Any]
        """
        ...  # pragma: no cover

    @abstractmethod
    def operations(self: Signer) -> List[SignOperation]:
        """Return list of operations supported by the Signer.

        :return: List[SignOperation]
        """
        ...  # pragma: no cover

    @abstractmethod
    def sign(self: Signer, operation: SignOperation) -> SigningResults:
        """Run signing operation.

        :param operation: signing operation
        :type operation: SignOperation

        :return: SigningResults
        """
        ...  # pragma: no cover

    @classmethod
    def doc_arguments(cls: Signer) -> Dict[str, Any]:
        """Return dict with arguments decription for the signer.

        :return: Dict[str, Any]
        """
        doc_arguments = {}
        for fn, fv in cls.__dataclass_fields__.items():
            if fv.metadata.get("description"):
                doc_arguments[fn] = fv.metadata.get("description")
        return doc_arguments
