class ImmutableError(TypeError):
    def __init__(self, field):
        self.message = f"Field '{field}' is immutable"
        super().__init__(self.message)


class NotCreatedError(RuntimeError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class InvalidPriorityError(TypeError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class InvalidStatusError(ValueError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
