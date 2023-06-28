from pubtools.sign.operations import (
    ClearSignOperation,
    ContainerSignOperation,
)


def test_containersign_operation_doc_argument():
    assert ContainerSignOperation.doc_arguments() == {
        "options": {
            "digests": {"description": "List of digest to sign"},
            "references": {"description": "List of references to sign"},
            "signing_key": {"description": "Signing key short id which should be used for signing"},
            "task_id": {
                "description": "Usually pub task id, serves as identifier for in signing request"
            },
        },
        "examples": {"digests": "", "references": "", "signing_key": "", "task_id": ""},
    }


def test_clearsign_operation_doc_argument():
    assert ClearSignOperation.doc_arguments() == {
        "options": {
            "inputs": {"type": "list", "description": "Signing data", "required": "true"},
            "signing_key": {
                "type": "str",
                "description": "Signing key short id which should be used for signing",
                "required": "true",
            },
            "task_id": {
                "type": "str",
                "description": "Usually pub task id, serves as identifier for in signing request",
                "required": "true",
            },
        },
        "examples": {"inputs": ["input1", "input2"], "signing_key": "123", "task_id": "1"},
    }
