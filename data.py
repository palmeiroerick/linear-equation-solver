from dataclasses import dataclass
from fractions import Fraction
from typing import Union, Literal as Literal_t


@dataclass
class Node:
    def __str__(self) -> str:
        raise NotImplementedError()

    def __eq__(self, other: object) -> bool:
        return type(self) == type(other) and self.__dict__ == other.__dict__


@dataclass
class Root(Node):
    left: Node
    right: Node

    def __str__(self) -> str:
        return f"{self.left} = {self.right}"


@dataclass
class Literal(Node):
    value: Union[int, float, Fraction]

    def __post_init__(self):
        self.value = Fraction(self.value)

    def __str__(self) -> str:
        if self.value < 0:
            return f"({self.value})"
        return str(self.value)


@dataclass
class Variable(Node):
    name: str = "x"
    coef: Union[int, float, Fraction] = 1

    def __post_init__(self):
        self.coef = Fraction(self.coef)

    def __str__(self) -> str:
        return f"{self.coef}{self.name}" if self.coef != 1 else self.name


_PRECEDENCE = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
}


@dataclass
class BinaryOp(Node):
    op: Literal_t["+", "-", "*", "/"]
    left: Node
    right: Node

    def __str__(self) -> str:
        def wrap(child: Node, is_left: bool) -> str:
            if not isinstance(child, BinaryOp):
                return str(child)

            my_prec = _PRECEDENCE[self.op]
            child_prec = _PRECEDENCE[child.op]

            if child_prec < my_prec:
                return f"({child})"
            if child_prec == my_prec:
                if self.op in {"-", "/"} and not is_left:
                    return f"({child})"
            return str(child)

        return f"{wrap(self.left, True)} {self.op} {wrap(self.right, False)}"
