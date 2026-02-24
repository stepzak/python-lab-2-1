from dataclasses import dataclass

@dataclass(frozen=True)
class Task:
    __slots__ = ("id", "payload")
    id: int
    payload: dict

    def __eq__(self, other):
        if isinstance(other, Task):
            return other.id == self.id and other.payload == self.payload
        raise TypeError(f"Unable to compare Task with other {type(other)}")
