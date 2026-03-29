class ImmutableError(TypeError):
    def __init__(self, field):
        self.message = f"Field '{field}' is immutable"
        super().__init__(self.message)

class TaskException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class NotCreatedError(TaskException, RuntimeError): ...

class InvalidPriorityError(TaskException, TypeError): ...

class InvalidStatusError(TaskException, ValueError): ...

class ExpiredError(TaskException, RuntimeError): ...

class CancelledError(TaskException, RuntimeError): ...