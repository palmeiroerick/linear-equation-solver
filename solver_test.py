import pytest
from nodes import Root, Literal, Variable, BinaryOp
from solver import solver
from fractions import Fraction

# s = 5 -> s = 5
# 2 = u -> u = 2
# 2k = 10 -> k = 5
# 10 = 2p -> p = 5
# 5/10 + 3/2 = e/3 -> e = 6
# (g - 2) / 3 = 4 -> g = 14
# 2(j + 3) = 4j - 2 -> j = 2
# 2y = y + 3 -> y = 3
# (1/2)b + (1/3)b = 5 -> b = 6
# 1 = -w / (-2) -> w = 2
# -i = -3 -> i = 3
# v + 2 = 2 -> v = 0
# 1 / q = 2 -> q = 1/2
# 5x / 2 = 10 -> t = 4
# -3m + 2 = 5 * (-2) -> m = 4
# 3 * (2 + r) = 15 -> r = 3
# 2 - 2 - 3 = -z -> z = 3
# 2 - (2 - 3) = -a -> a = -3
# 2 - (3 - c) = 1 -> c = 2
# 2 + (-(-3 + 5 * x)) = 11 -> x = -6/5
# h = (1 + 2) / (3 - 4) * (5 - 2) -> h = -9
# l = (1 + 2) / ((3 - 4) * (5 - 2)) -> l = -1


@pytest.mark.parametrize("eq, solution", [
    # s = 5 -> s = 5
    (Root(Variable("s"), Literal(5)), Root(Variable("s"), Literal(5))),

    # 2 = u -> u = 2
    (Root(Literal(2), Variable("u")), Root(Variable("u"), Literal(2))),

    # 2k = 10 -> k = 5
    (Root(BinaryOp("*", Literal(2), Variable("k")),
     Literal(10)), Root(Variable("k"), Literal(5))),

    # 10 = 2p -> p = 5
    (Root(Literal(10), BinaryOp("*", Literal(2), Variable("p"))),
     Root(Variable("p"), Literal(5))),

    # 5/10 + 3/2 = e/3 -> e = 6
    (Root(
        BinaryOp("+", BinaryOp("/", Literal(5), Literal(10)),
                 BinaryOp("/", Literal(3), Literal(2))),
        BinaryOp("/", Variable("e"), Literal(3))
    ), Root(Variable("e"), Literal(6))),

    # (g - 2) / 3 = 4 -> g = 14
    (Root(
        BinaryOp("/", BinaryOp("-", Variable("g"), Literal(2)), Literal(3)),
        Literal(4)
    ), Root(Variable("g"), Literal(14))),

    # 2(j + 3) = 4j - 2 -> j = 2
    (Root(
        BinaryOp("*", Literal(2), BinaryOp("+", Variable("j"), Literal(3))),
        BinaryOp("-", BinaryOp("*", Literal(4), Variable("j")), Literal(2))
    ), Root(Variable("j"), Literal(2))),

    # 2y = y + 3 -> y = 3
    (Root(
        BinaryOp("*", Literal(2), Variable("y")),
        BinaryOp("+", Variable("y"), Literal(3))
    ), Root(Variable("y"), Literal(3))),

    # (1/2)b + (1/3)b = 5 -> b = 6
    (Root(
        BinaryOp("+",
                 BinaryOp("*", Literal(Fraction(1, 2)), Variable("b")),
                 BinaryOp("*", Literal(Fraction(1, 3)), Variable("b"))),
        Literal(5)
    ), Root(Variable("b"), Literal(6))),

    # 1 = -w / (-2) -> w = 2
    (Root(
        Literal(1),
        BinaryOp("/", Variable("w", -1), Literal(-2))
    ), Root(Variable("w"), Literal(2))),

    # -i = -3 -> i = 3
    (Root(
        Variable("i", -1),
        Literal(-3)
    ), Root(Variable("i"), Literal(3))),

    # v + 2 = 2 -> v = 0
    (Root(
        BinaryOp("+", Variable("v"), Literal(2)),
        Literal(2)
    ), Root(Variable("v"), Literal(0))),

    # 1 / q = 2 -> q = 1/2
    (Root(
        BinaryOp("/", Literal(1), Variable("q")),
        Literal(2)
    ), Root(Variable("q"), Literal(Fraction(1, 2)))),

    # 5x / 2 = 10 -> x = 4
    (Root(
        BinaryOp("/", BinaryOp("*", Literal(5), Variable("x")), Literal(2)),
        Literal(10)
    ), Root(Variable("x"), Literal(4))),

    # -3m + 2 = 5 * (-2) -> m = 4
    (Root(
        BinaryOp("+", Variable("m", -3), Literal(2)),
        BinaryOp("*", Literal(5), Literal(-2))
    ), Root(Variable("m"), Literal(4))),

    # 3 * (2 + r) = 15 -> r = 3
    (Root(
        BinaryOp("*", Literal(3), BinaryOp("+", Literal(2), Variable("r"))),
        Literal(15)
    ), Root(Variable("r"), Literal(3))),

    # 2 - 2 - 3 = -z -> z = 3
    (Root(
        BinaryOp("-", BinaryOp("-", Literal(2), Literal(2)), Literal(3)),
        Variable("z", -1)
    ), Root(Variable("z"), Literal(3))),

    # 2 - (2 - 3) = -a -> a = -3
    (Root(
        BinaryOp("-", Literal(2), BinaryOp("-", Literal(2), Literal(3))),
        Variable("a", -1)
    ), Root(Variable("a"), Literal(-3))),

    # 2 - (3 - x) = 1 -> x = 2
    (Root(BinaryOp("-", Literal(2), BinaryOp("-", Literal(3), Variable("x"))), Literal(1)),
     Root(Variable("x"), Literal(2))),


    # 2 + (-(-3 + 5 * x)) = 11 -> x = -6/5
    (Root(
        BinaryOp("+", Literal(2), BinaryOp("*", Literal(-1),
                                           BinaryOp("+", Literal(-3), BinaryOp("*", Literal(5), Variable("x"))))),
        Literal(11)
    ), Root(Variable("x"), Literal(Fraction(-6, 5)))),

    # h = (1 + 2) / (3 - 4) * (5 - 2) -> h = -9
    (Root(
        Variable("h"),
        BinaryOp("*",
                 BinaryOp("/",
                          BinaryOp("+", Literal(1), Literal(2)),
                          BinaryOp("-", Literal(3), Literal(4))
                          ),
                 BinaryOp("-", Literal(5), Literal(2))
                 )
    ), Root(Variable("h"), Literal(-9))),

    # l = (1 + 2) / ((3 - 4) * (5 - 2)) -> l = -1
    (Root(
        Variable("l"),
        BinaryOp("/",
                 BinaryOp("+", Literal(1), Literal(2)),
                 BinaryOp("*",
                          BinaryOp("-", Literal(3), Literal(4)),
                          BinaryOp("-", Literal(5), Literal(2))
                          )
                 )
    ), Root(Variable("l"), Literal(-1))),
])
def test_solver(eq: Root, solution: Root) -> None:
    assert solver(eq) == solution
