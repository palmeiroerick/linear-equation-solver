import re
from dataclasses import dataclass
from enum import IntEnum
from typing import List


class TokenType(IntEnum):
    EQUAL = 0
    PLUS = 1
    MINUS = 2
    MULTIPLY = 3
    DIVIDE = 4
    LPAREN = 5
    RPAREN = 6
    DIGIT = 7
    DOT = 8
    LETTER = 9


@dataclass(frozen=True)
class Token:
    type: TokenType
    value: str

    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r})"

    def __eq__(self, other: object):
        if not isinstance(other, Token):
            return False
        return self.type == other.type and self.value == other.value


def lexer(text: str) -> List[Token]:
    text = re.sub(r"\s+", "", text)
    tokens: List[Token] = []

    if len(text) == 0:
        raise ValueError("Empty input text")

    for char in text:
        if char == "=":
            tokens.append(Token(TokenType.EQUAL, char))
        elif char == "+":
            tokens.append(Token(TokenType.PLUS, char))
        elif char == "-":
            tokens.append(Token(TokenType.MINUS, char))
        elif char == "*":
            tokens.append(Token(TokenType.MULTIPLY, char))
        elif char == "/":
            tokens.append(Token(TokenType.DIVIDE, char))
        elif char == "(":
            tokens.append(Token(TokenType.LPAREN, char))
        elif char == ")":
            tokens.append(Token(TokenType.RPAREN, char))
        elif char.isdigit():
            tokens.append(Token(TokenType.DIGIT, char))
        elif char == ".":
            tokens.append(Token(TokenType.DOT, char))
        elif char.isalpha():
            tokens.append(Token(TokenType.LETTER, char))
        else:
            raise ValueError(f"Invalid character: {char}")

    return tokens
