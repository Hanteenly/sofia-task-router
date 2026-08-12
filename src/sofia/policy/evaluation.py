
class Policy:
    def evaluate(self, task):
        
        valid_risk_classes = {"read-safe", "write-risk", "high-stakes"}
        valid_data_sensitivities = {"public", "internal", "restricted", "sealed"}

        if task.risk_class not in valid_risk_classes:
            return "invalid-task"

        if task.data_sensitivity not in valid_data_sensitivities:
            return "invalid-task"

        if task.requires_human_approval:
            return "approval-required"

        if task.risk_class in {"write-risk", "high-stakes"}:
            return "approval-required"

        if task.data_sensitivity in {"restricted", "sealed"}:
            return "cloud forbidden"

        return "execution allowed"
    