import re
import pytest
from lexer import Token, TokenType, lexer
from typing import List


@pytest.mark.parametrize("text, tokens", [
    ("x * 3 - 3x   ", [
        Token(TokenType.LETTER, "x"),
        Token(TokenType.MULTIPLY, "*"),
        Token(TokenType.DIGIT, "3"),
        Token(TokenType.MINUS, "-"),
        Token(TokenType.DIGIT, "3"),
        Token(TokenType.LETTER, "x"),
    ]),
    ("(x -    2)\t / 5", [
        Token(TokenType.LPAREN, "("),
        Token(TokenType.LETTER, "x"),
        Token(TokenType.MINUS, "-"),
        Token(TokenType.DIGIT, "2"),
        Token(TokenType.RPAREN, ")"),
        Token(TokenType.DIVIDE, "/"),
        Token(TokenType.DIGIT, "5")
    ]),
    ("   -3x + 2=5", [
        Token(TokenType.MINUS, "-"),
        Token(TokenType.DIGIT, "3"),
        Token(TokenType.LETTER, "x"),
        Token(TokenType.PLUS, "+"),
        Token(TokenType.DIGIT, "2"),
        Token(TokenType.EQUAL, "="),
        Token(TokenType.DIGIT, "5")
    ]),
    ("-.5 + 5.25\r\n/5", [
        Token(TokenType.MINUS, "-"),
        Token(TokenType.DOT, "."),
        Token(TokenType.DIGIT, "5"),
        Token(TokenType.PLUS, "+"),
        Token(TokenType.DIGIT, "5"),
        Token(TokenType.DOT, "."),
        Token(TokenType.DIGIT, "2"),
        Token(TokenType.DIGIT, "5"),
        Token(TokenType.DIVIDE, "/"),
        Token(TokenType.DIGIT, "5"),
    ])
])
def test_lexer(text: str, tokens: List[Token]) -> None:
    assert lexer(text) == tokens


@pytest.mark.parametrize("text, error_msg", [
    ("", "Empty input text"),
    ("  \r\n \t", "Empty input text"),
    ("a + b # 3", "Invalid character: #"),
    ("2x + 4$ = 10", "Invalid character: $"),
    ("x @ 3 = 7", "Invalid character: @"),
    ("5x + 3 = ?10", "Invalid character: ?"),
    ("4x + %2 = 8", "Invalid character: %"),
    ("a + b = c!", "Invalid character: !"),
    ("4x[ + 2 = 8", "Invalid character: ["),
    ("x^2 + 3 = 9", "Invalid character: ^"),
])
def test_lexer_invalid(text: str, error_msg: str) -> None:
    with pytest.raises(ValueError, match=re.escape(error_msg)):
        lexer(text)
