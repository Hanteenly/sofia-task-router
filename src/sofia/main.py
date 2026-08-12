from sofia.models.task import Task
from sofia.router.router import Router

if __name__ == "__main__":
    
    router = Router()
    
    task = Task(
        task_id="task-001",
        intent="summarize",
        data_sensitivity="internal",
        risk_class="read-safe",
        allowed_backends=["local", "cloud"],
        requires_human_approval=False,
        payload={"text": "Example document content"}
    )
    print(task.task_id, "->", router.route(task, ["local"]))

    task = Task(
        task_id="task-002",
        intent="summarize",
        data_sensitivity="internal",
        risk_class="read-safe",
        allowed_backends=["cloud"],
        requires_human_approval=False,
        payload={"text": "Example document content"}
    )
    print(task.task_id, "->", router.route(task, ["local"]))


    task = Task(
        task_id="task-003",
        intent="summarize",
        data_sensitivity="restricted",
        risk_class="read-safe",
        allowed_backends=["cloud"],
        requires_human_approval=False,
        payload={"text": "Sensitive document"}
    )
    print(task.task_id, "->", router.route(task, ["cloud"]))

    print(router.audit.records)
