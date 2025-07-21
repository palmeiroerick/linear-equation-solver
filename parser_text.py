import re
import pytest
from lexer import Token, TokenType
from typing import List
from nodes import Node, Root, Literal, Variable, BinaryOp
from parser import parser
from fractions import Fraction


@pytest.mark.parametrize("tokens, eq", [
    # 5x / 2 = 10
    (
        [
            Token(TokenType.DIGIT, "5"),
            Token(TokenType.LETTER, "x"),
            Token(TokenType.DIVIDE, "/"),
            Token(TokenType.DIGIT, "2"),
            Token(TokenType.EQUAL, "="),
            Token(TokenType.DIGIT, "10"),
        ],
        Root(
            left=BinaryOp(
                op="/",
                left=Variable(name="x", coef=Fraction(5)),
                right=Literal(Fraction(2))
            ),
            right=Literal(Fraction(10))
        )
    ),

    # -3m + 2 = 5 * (-2)
    (
        [
            Token(TokenType.MINUS, "-"),
            Token(TokenType.DIGIT, "3"),
            Token(TokenType.LETTER, "m"),
            Token(TokenType.PLUS, "+"),
            Token(TokenType.DIGIT, "2"),
            Token(TokenType.EQUAL, "="),
            Token(TokenType.DIGIT, "5"),
            Token(TokenType.MULTIPLY, "*"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.MINUS, "-"),
            Token(TokenType.DIGIT, "2"),
            Token(TokenType.RPAREN, ")"),
        ],
        Root(
            left=BinaryOp(
                op="+",
                left=Variable(name="m", coef=Fraction(-3)),
                right=Literal(Fraction(2))
            ),
            right=BinaryOp(
                op="*",
                left=Literal(Fraction(5)),
                right=Literal(Fraction(-2))
            )
        )
    ),

    # 3 * (2 + r) = 15
    (
        [
            Token(TokenType.DIGIT, "3"),
            Token(TokenType.MULTIPLY, "*"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.DIGIT, "2"),
            Token(TokenType.PLUS, "+"),
            Token(TokenType.LETTER, "r"),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.EQUAL, "="),
            Token(TokenType.DIGIT, "15"),
        ],
        Root(
            left=BinaryOp(
                op="*",
                left=Literal(Fraction(3)),
                right=BinaryOp(
                    op="+",
                    left=Literal(Fraction(2)),
                    right=Variable(name="r", coef=Fraction(1))
                )
            ),
            right=Literal(Fraction(15))
        )
    ),

    # 2 - 2 - 3 = -z
    (
        [
            Token(TokenType.DIGIT, "2"),
            Token(TokenType.MINUS, "-"),
            Token(TokenType.DIGIT, "2"),
            Token(TokenType.MINUS, "-"),
            Token(TokenType.DIGIT, "3"),
            Token(TokenType.EQUAL, "="),
            Token(TokenType.MINUS, "-"),
            Token(TokenType.LETTER, "z"),
        ],
        Root(
            left=BinaryOp(
                op="-",
                left=BinaryOp(
                    op="-",
                    left=Literal(Fraction(2)),
                    right=Literal(Fraction(2))
                ),
                right=Literal(Fraction(3))
            ),
            right=Variable(name="z", coef=Fraction(-1))
        )
    ),

    # 2 - (2 - 3) = -a
    (
        [
            Token(TokenType.DIGIT, "2"),
            Token(TokenType.MINUS, "-"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.DIGIT, "2"),
            Token(TokenType.MINUS, "-"),
            Token(TokenType.DIGIT, "3"),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.EQUAL, "="),
            Token(TokenType.MINUS, "-"),
            Token(TokenType.LETTER, "a"),
        ],
        Root(
            left=BinaryOp(
                op="-",
                left=Literal(Fraction(2)),
                right=BinaryOp(
                    op="-",
                    left=Literal(Fraction(2)),
                    right=Literal(Fraction(3))
                )
            ),
            right=Variable(name="a", coef=Fraction(-1))
        )
    ),

    # +.4c + (-.2c) = 5
    (
        [
            Token(TokenType.PLUS, "+"),
            Token(TokenType.DOT, "."),
            Token(TokenType.DIGIT, "4"),
            Token(TokenType.LETTER, "c"),
            Token(TokenType.PLUS, "+"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.MINUS, "-"),
            Token(TokenType.DOT, "."),
            Token(TokenType.DIGIT, "2"),
            Token(TokenType.LETTER, "c"),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.EQUAL, "="),
            Token(TokenType.DIGIT, "5"),
        ],
        Root(
            left=BinaryOp(
                op="+",
                left=Variable(name="c", coef=Fraction("0.4")),
                right=Variable(name="c", coef=Fraction("-0.2"))
            ),
            right=Literal(Fraction(5))
        )
    ),

    # 2 + (-(-3 * x)) = 11
    (
        [
            Token(TokenType.DIGIT, "2"),
            Token(TokenType.PLUS, "+"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.MINUS, "-"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.MINUS, "-"),
            Token(TokenType.DIGIT, "3"),
            Token(TokenType.MULTIPLY, "*"),
            Token(TokenType.LETTER, "x"),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.EQUAL, "="),
            Token(TokenType.DIGIT, "11"),
        ],
        Root(
            left=BinaryOp(
                op="+",
                left=Literal(Fraction(2)),
                right=BinaryOp(
                    op="*",
                    left=Literal(Fraction(-1)),
                    right=BinaryOp(
                        op="*",
                        left=Literal(Fraction(-3)),
                        right=Variable(name="x", coef=Fraction(1))
                    )
                )
            ),
            right=Literal(Fraction(11))
        )
    ),

    # h = (1 + 2) / (3 - 4) * (5 - 2)
    (
        [
            Token(TokenType.LETTER, "h"),
            Token(TokenType.EQUAL, "="),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.DIGIT, "1"),
            Token(TokenType.PLUS, "+"),
            Token(TokenType.DIGIT, "2"),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.DIVIDE, "/"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.DIGIT, "3"),
            Token(TokenType.MINUS, "-"),
            Token(TokenType.DIGIT, "4"),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.MULTIPLY, "*"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.DIGIT, "5"),
            Token(TokenType.MINUS, "-"),
            Token(TokenType.DIGIT, "2"),
            Token(TokenType.RPAREN, ")"),
        ],
        Root(
            left=Variable(name="h", coef=Fraction(1)),
            right=BinaryOp(
                op="*",
                left=BinaryOp(
                    op="/",
                    left=BinaryOp(
                        op="+",
                        left=Literal(Fraction(1)),
                        right=Literal(Fraction(2))
                    ),
                    right=BinaryOp(
                        op="-",
                        left=Literal(Fraction(3)),
                        right=Literal(Fraction(4))
                    )
                ),
                right=BinaryOp(
                    op="-",
                    left=Literal(Fraction(5)),
                    right=Literal(Fraction(2))
                )
            )
        )
    ),

    # l = (1 + 2) / ((3 - 4) * (5 - 2))
    (
        [
            Token(TokenType.LETTER, "l"),
            Token(TokenType.EQUAL, "="),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.DIGIT, "1"),
            Token(TokenType.PLUS, "+"),
            Token(TokenType.DIGIT, "2"),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.DIVIDE, "/"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.DIGIT, "3"),
            Token(TokenType.MINUS, "-"),
            Token(TokenType.DIGIT, "4"),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.MULTIPLY, "*"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.DIGIT, "5"),
            Token(TokenType.MINUS, "-"),
            Token(TokenType.DIGIT, "2"),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.RPAREN, ")"),
        ],
        Root(
            left=Variable(name="l", coef=Fraction(1)),
            right=BinaryOp(
                op="/",
                left=BinaryOp(
                    op="+",
                    left=Literal(Fraction(1)),
                    right=Literal(Fraction(2))
                ),
                right=BinaryOp(
                    op="*",
                    left=BinaryOp(
                        op="-",
                        left=Literal(Fraction(3)),
                        right=Literal(Fraction(4))
                    ),
                    right=BinaryOp(
                        op="-",
                        left=Literal(Fraction(5)),
                        right=Literal(Fraction(2))
                    )
                )
            )
        )
    ),
])
def test_parser(tokens: List[Token], eq: Node) -> None:
    assert parser(tokens) == eq


@pytest.mark.parametrize("tokens, error_msg", [
    ([], "Empty tokens"),

    ([Token(TokenType.DIGIT, "2"), Token(TokenType.PLUS, "+"), Token(TokenType.DIGIT, "2")],
     "The equation must have exactly one '=' sign."),

    ([Token(TokenType.DIGIT, "1"), Token(TokenType.EQUAL, "="), Token(TokenType.DIGIT, "2"), Token(TokenType.EQUAL, "="), Token(TokenType.DIGIT, "3"),],
     "The equation must have exactly one '=' sign."),

    (
        [
            Token(TokenType.DIGIT, "2"),
            Token(TokenType.PLUS, "+"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.DIGIT, "3"),
            Token(TokenType.MULTIPLY, "*"),
            Token(TokenType.DIGIT, "4"),
            Token(TokenType.EQUAL, "="),
            Token(TokenType.DIGIT, "14"),
        ],
        "Expected ')'"
    ),

    # (
    #     [
    #         Token(TokenType.DIGIT, "2"),
    #         Token(TokenType.PLUS, "+"),
    #         Token(TokenType.DIGIT, "3"),
    #         Token(TokenType.RPAREN, ")"),
    #         Token(TokenType.EQUAL, "="),
    #         Token(TokenType.DIGIT, "5"),
    #     ],
    #     "Unexpected token"
    # ),
    (
        [
            Token(TokenType.DIGIT, "2"),
            Token(TokenType.MULTIPLY, "*"),
            Token(TokenType.LETTER, "a"),
            Token(TokenType.LETTER, "b"),
            Token(TokenType.EQUAL, "="),
            Token(TokenType.DIGIT, "4"),
        ],
        "Variables must have exactly only one letter"
    ),
    (
        [
            Token(TokenType.MULTIPLY, "*"),
            Token(TokenType.DIGIT, "3"),
            Token(TokenType.EQUAL, "="),
            Token(TokenType.DIGIT, "3"),
        ],
        "Unexpected token: Token(MULTIPLY, '*')"
    ),
    (
        [Token(TokenType.MINUS, "-"),
         # Token(TokenType.MINUS, "-"),
         Token(TokenType.MINUS, "-"),
         Token(TokenType.LETTER, "x"),
         Token(TokenType.EQUAL, "="),
         Token(TokenType.DIGIT, "1")],
        "Unexpected token: Token(MINUS, '-')"
    ),
    # (
    #     [
    #         Token(TokenType.MINUS, "-"),
    #         Token(TokenType.DIGIT, "1"),
    #         Token(TokenType.EQUAL, "="),
    #         Token(TokenType.DIGIT, "1"),
    #         Token(TokenType.MINUS, "-"),
    #         Token(TokenType.MINUS, "-"),
    #         Token(TokenType.DIGIT, "1"),
    #     ],
    #     "Unexpected token: Token(MINUS, '-')"
    # ),
    (
        [Token(TokenType.DOT, "."),
         Token(TokenType.EQUAL, "="),
         Token(TokenType.DIGIT, "1")],
        "Invalid number"
    ),
    # (
    #     [Token(TokenType.DIGIT, "3"),
    #      Token(TokenType.DOT, "."),
    #      Token(TokenType.EQUAL, "="),
    #      Token(TokenType.DIGIT, "3")],
    #     "Invalid number"
    # ),
    # (
    #     [Token(TokenType.DIGIT, "3"),
    #      Token(TokenType.PLUS, "+"),
    #      Token(TokenType.EQUAL, "="),
    #      Token(TokenType.DIGIT, "3")],
    #     "Unexpected token"
    # ),

])
def test_parser_invalid(tokens: List[Token], error_msg: str):
    with pytest.raises(ValueError, match=re.escape(error_msg)):
        parser(tokens)
