from dataclasses import dataclass

@dataclass
class Task:
    id: int
    payload: dict
