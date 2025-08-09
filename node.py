from typing import Self


class UoTNode:
    children: list[tuple[Self, Self]]
    question: str
    answer: bool  # True for "YES" and False for "NO"
    items: list[str]
    parent: None | Self

    def is_terminal(self):
        return len(self.items) <= 2

    def _create_children_nodes(self, task, items, n, previous_questions):
        if self.is_terminal():
            return
        questions = 

