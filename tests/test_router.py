from sofia.models import task
from sofia.models.task import Task
from sofia.router import router
from sofia.router.router import Router
from sofia.backends.LocalBackend import LocalBackend
from sofia.backends.CloudBackend import CloudBackend
from sofia.backends.MockBackend import MockBackend
from unittest.mock import patch

def test_local_first():
    task = Task(
        task_id = "task",
        intent = "summarize",
        data_sensitivity="internal",
        risk_class="read-safe",
        allowed_backends = ["mock", "cloud", "local"],
        requires_human_approval = False,
        payload = {"text": "Example document content"}
    )
    local = LocalBackend()
    router = Router()
    assert router.route(task, ["mock","local"]) == local.execute(task)

def test_restricted_blocks_cloud():
    task1 = Task(
        task_id = "task",
        intent = "summarize",
        data_sensitivity="restricted",
        risk_class="read-safe",
        allowed_backends = ["cloud"],
        requires_human_approval = False,
        payload = {"text": "Example document content"}
        )
    task2 = Task(
        task_id = "task",
        intent = "summarize",
        data_sensitivity="sealed",
        risk_class="read-safe",
        allowed_backends = ["cloud"],
        requires_human_approval = False,
        payload = {"text": "Example document content"}
        )
    router = Router()
    assert router.route(task1, ["cloud"]) == "no-backend"
    assert router.route(task2, ["cloud"]) == "no-backend"

def test_high_stakes_requires_approval():
    task1 = Task(
        task_id = "task",
        intent = "summarize",
        data_sensitivity="restricted",
        risk_class="write-risk",
        allowed_backends = ["cloud"],
        requires_human_approval = False,
        payload = {"text": "Example document content"}
        )
    task2 = Task(
        task_id = "task",
        intent = "summarize",
        data_sensitivity="sealed",
        risk_class="high-stakes",
        allowed_backends = ["cloud"],
        requires_human_approval = False,
        payload = {"text": "Example document content"}
        )
    router = Router()
    assert router.route(task1, ["cloud"]) == "no-backend"
    assert router.route(task2, ["cloud"]) == "no-backend"



def test_local_failure_no_cloud_fallback():
    task = Task(
        task_id = "task",
        intent = "summarize",
        data_sensitivity="restricted",
        risk_class="read-safe",
        allowed_backends = ["local","cloud"],
        requires_human_approval = False,
        payload = {"text": "Example document content"}
        )
    router = Router()
    with patch.object(LocalBackend, "execute", return_value="error"):
        assert router.route(task, ["local", "cloud"]) == "fallback-required"
    
def test_backend_switching():
    task1 = Task(
        task_id = "task",
        intent = "summarize",
        data_sensitivity="restricted",
        risk_class="read-safe",
        allowed_backends = ["local"],
        requires_human_approval = False,
        payload = {"text": "Example document content"}
        )
    
    task2 = Task(
        task_id = "task",
        intent = "summarize",
        data_sensitivity="internal",
        risk_class="read-safe",
        allowed_backends = ["cloud"],
        requires_human_approval = False,
        payload = {"text": "Example document content"}
        )
    
    task3 = Task(
        task_id = "task",
        intent = "summarize",
        data_sensitivity="restricted",
        risk_class="read-safe",
        allowed_backends = ["mock"],
        requires_human_approval = False,
        payload = {"text": "Example document content"}
        )
    
    local = LocalBackend()
    cloud = CloudBackend()
    mock = MockBackend()
    router = Router()

    assert router.route(task1, ["local"]) == local.execute(task1)
    assert router.route(task2, ["cloud"]) == cloud.execute(task2)
    assert router.route(task3, ["mock"]) == mock.execute(task3)
    