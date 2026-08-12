from datetime import datetime

class Audit:
    def __init__(self):
        self.records = []

    def log(self, task, routing_decision, selected_backend,
             policy_decision, execution_status, error_or_limitation):

        result = {
            "task_id": task.task_id,
            "routing_decision": routing_decision,
            "selected_backend": selected_backend,
            "policy_decision": policy_decision,
            "execution_status": execution_status,
            "error_or_limitation": error_or_limitation,
            "timestamp": datetime.now()
        }

        self.records.append(result)
        