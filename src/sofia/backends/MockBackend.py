from sofia.backends.Backend import Backend

class MockBackend(Backend):

    def execute(self, task):
        if task.intent == "summarize":
            return task.payload.get("text")
        else:
            return "error"