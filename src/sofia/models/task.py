from dataclasses import dataclass

@dataclass
class Task:
    task_id: str
    intent: str
    data_sensitivity: str
    risk_class: str
    allowed_backends: list[str]
    requires_human_approval: bool
    payload: dict