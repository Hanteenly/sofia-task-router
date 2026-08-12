from sofia.backends.CloudBackend import CloudBackend
from sofia.backends.LocalBackend import LocalBackend
from sofia.backends.MockBackend import MockBackend
from sofia.policy.evaluation import Policy
from sofia.audit.Audit import Audit
class Router:

    def __init__(self):
        self.audit = Audit()

    def route(self, task, available_backends):
        cloud = CloudBackend()
        local = LocalBackend()
        mock = MockBackend()
        policy = Policy()
        cloud_block = False
        policy_result = policy.evaluate(task)

        if policy_result == "approval-required":
            self.audit.log(task, "approval-required", None, policy_result, "blocked", None)
            return "no-backend"

        elif policy_result == "cloud forbidden":
            cloud_block = True

        is_local = False
        is_cloud = False
        is_mock = False

        for backend in task.allowed_backends:
            if backend in available_backends:
                if backend == "local":
                    is_local = True
                elif backend == "cloud":
                    is_cloud = True
                elif backend == "mock":
                    is_mock = True

        if is_local == True:
            execution_result = local.execute(task)
            if execution_result == "error":
                self.audit.log(task, "local-failed", "local", policy_result, "error", "local backend execution failed")
                return "fallback-required"
            self.audit.log(task, "local-selected", "local", policy_result, "success", None)
            return execution_result

        elif is_cloud == True and cloud_block != True:
            execution_result = cloud.execute(task)
            if execution_result == "error":
                self.audit.log(task, "cloud-failed", "cloud", policy_result, "error", "cloud backend execution failed")
                return "error"
            self.audit.log(task, "cloud-selected", "cloud", policy_result, "success", None)
            return execution_result

        elif is_mock == True:
            execution_result = mock.execute(task)
            if execution_result == "error":
                self.audit.log(task, "mock-failed", "mock", policy_result, "error", "mock backend execution failed")
                return "error"
            self.audit.log(task, "mock-selected", "mock", policy_result, "success", None)
            return execution_result

        self.audit.log(task, "no-backend", None, policy_result, "blocked", "no suitable backend available")
        return "no-backend"