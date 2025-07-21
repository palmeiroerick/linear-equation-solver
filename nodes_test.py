import pytest
from fractions import Fraction
from nodes import Node, Literal, Variable, BinaryOp, Root


@pytest.mark.parametrize("node, expected", [
    # (Root(BinaryOp("-", Literal(-2), BinaryOp("*", Literal(-3), Variable("x", Fraction(3, 5)))), BinaryOp("*", Variable("x", -2), Literal(3))),
    #  "-2 - (-3) * 3/5x = -2x * 3"),
    # (Root(BinaryOp("/", Literal(Fraction(-3, 4)), Literal(5)), BinaryOp("*", BinaryOp("+", Literal(1), Variable("z")), Literal(3))),
    #  "-3/4 / 5 = (1 + z) * 3"),
    (Root(BinaryOp("-", BinaryOp("-", Literal(1), Literal(2)), Literal(3)), BinaryOp("/", Variable("l", 2), Literal(-5))),
     "1 - 2 - 3 = 2l / (-5)"),
    (Root(BinaryOp("-", Literal(1), BinaryOp("-", Literal(3), Variable())), BinaryOp("+", BinaryOp("+", Literal(3), Literal(5)), Literal(4))),
     "1 - (3 - x) = 3 + 5 + 4"),
    (Root(BinaryOp("+", Literal(Fraction(4, 3)), Variable("y", -3)), BinaryOp("/", BinaryOp("*", Literal(4), Variable("y", -3)), Literal(2))),
     "4/3 + (-3y) = 4 * (-3y) / 2"),
    (BinaryOp("*", BinaryOp("/", BinaryOp("+", Literal(1), Literal(2)), BinaryOp("-", Literal(3), Literal(4)),), BinaryOp("-", Literal(5), Literal(2)),),
     "(1 + 2) / (3 - 4) * (5 - 2)"),
])
def test_nodes_str(node: Node, expected: str) -> None:
    assert str(node) == expected
