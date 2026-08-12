
class Policy:
    def evaluate(self, task):

        if task.requires_human_approval == True:
            return "approval-required"
        elif task.risk_class == "write-risk" or task.risk_class == "high-stakes":
            return "approval-required"
        elif task.data_sensitivity == "restricted" or task.data_sensitivity == "sealed":
            return "cloud forbidden"
        else:
            return "execution allowed"


