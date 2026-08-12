from sofia.models.task import Task
from sofia.router.router import Router


def main():
    router = Router()
    
    task1 = Task(
        task_id="task-001",
        intent="summarize",
        data_sensitivity="internal",
        risk_class="read-safe",
        allowed_backends=["local", "cloud"],
        requires_human_approval=False,
        payload={"text": "Example document content"}
    )
    print(task1.task_id, "->", router.route(task1, ["local"]))

    task2 = Task(
        task_id="task-002",
        intent="summarize",
        data_sensitivity="internal",
        risk_class="read-safe",
        allowed_backends=["cloud"],
        requires_human_approval=False,
        payload={"text": "Example document content"}
    )
    print(task2.task_id, "->", router.route(task2, ["local"]))


    task3 = Task(
        task_id="task",
        intent="summarize",
        data_sensitivity="internal",
        risk_class="read-safe",
        allowed_backends=["cloud"],
        requires_human_approval=False,
        payload={"text": "Example document content. Something is good"}
        )
    print(task3.task_id, "->", router.route(task3, ["cloud"]))

    print(router.audit.records)

if __name__ == "__main__":
    main()