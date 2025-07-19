from fractions import Fraction
from typing import List, Tuple
from lexer import Token, TokenType
from data import Node, Root, Literal, Variable, BinaryOp

"""
<equation>   = <expression> EQUAL <expression>

<expression> = <term> { (PLUS | MINUS) <term> }

<term>       = <factor> { (MULTIPLY | DIVIDE) <factor> }

<factor>     = [ (PLUS | MINUS) ] (<foo> | LPAREN <expression> RPAREN)

<foo>        = <number>
             | [ <number> ] <variable>

<number>     = DOT DIGIT {DIGIT}
             | DIGIT {DIGIT} [ DOT DIGIT {DIGIT} ]

<variable>   = LETTER
"""


def parser(tokens: List[Token]) -> Root:
    if len(tokens) == 0:
        raise ValueError("Empty tokens.")

    if tokens.count(Token(TokenType.EQUAL, "=")) != 1:
        raise ValueError("The equation must have exactly one '=' sign.")

    i = tokens.index(Token(TokenType.EQUAL, "="))

    left, _ = parse_expr(tokens[:i], 0)
    right, _ = parse_expr(tokens[i+1:], 0)

    return Root(left, right)


def parse_expr(tokens: List[Token], i: int) -> Tuple[Node, int]:
    node, i = parse_term(tokens, i)
    while i < len(tokens) and tokens[i].type in {TokenType.PLUS, TokenType.MINUS}:
        op = tokens[i].value
        right, i = parse_term(tokens, i + 1)
        node = BinaryOp(op, node, right) # type: ignore
    return node, i


def parse_term(tokens: List[Token], i: int) -> Tuple[Node, int]:
    node, i = parse_factor(tokens, i)
    while i < len(tokens) and tokens[i].type in {TokenType.MULTIPLY, TokenType.DIVIDE}:
        op = tokens[i].value
        right, i = parse_factor(tokens, i + 1)
        node = BinaryOp(op, node, right) # type: ignore
    return node, i


def parse_factor(tokens: List[Token], i: int) -> Tuple[Node, int]:
    sign = 1

    if tokens[i].type in {TokenType.PLUS, TokenType.MINUS}:
        sign = 1 if tokens[i].type == TokenType.PLUS else -1
        i += 1

    if tokens[i].type in {TokenType.DIGIT, TokenType.DOT, TokenType.LETTER}:
        node, i = parse_foo(tokens, i)
    elif tokens[i].type == TokenType.LPAREN:
        node, i = parse_expr(tokens, i + 1)
        if i >= len(tokens) or tokens[i].type != TokenType.RPAREN:
            raise ValueError("Expected ')'")
        i += 1
    else:
        raise ValueError(f"Unexpected token: {tokens[i]}")

    if sign == -1:
        if isinstance(node, Literal):
            node = Literal(sign * node.value)
        elif isinstance(node, Variable):
            node = Variable(name=node.name, coef=sign * node.coef)
        else:
            node = BinaryOp("*", Literal(Fraction(sign)), node)

    return node, i


def parse_foo(tokens: List[Token], i: int) -> Tuple[Node, int]:
    if tokens[i].type in {TokenType.DIGIT, TokenType.DOT}:
        literal, i = parse_num(tokens, i)

        if i < len(tokens) and tokens[i].type == TokenType.LETTER:
            variable, i = parse_var(tokens, i)
            return Variable(variable.name, literal.value), i

        return literal, i

    if i < len(tokens) and tokens[i].type == TokenType.LETTER:
        variable, i = parse_var(tokens, i)
        return variable, i

    raise ValueError(f"Unexpected token: {tokens[i]}")


def parse_num(tokens: List[Token], i: int) -> Tuple[Literal, int]:
    digits = ""

    if i < len(tokens) and tokens[i].type == TokenType.DOT:
        digits += tokens[i].value
        i += 1

        while len(tokens) > i and tokens[i].type == TokenType.DIGIT:
            digits += tokens[i].value
            i += 1

        if digits in {".", ""}:
            raise ValueError("Invalid number")

        return Literal(Fraction(digits)), i

    while i < len(tokens) and tokens[i].type == TokenType.DIGIT:
        digits += tokens[i].value
        i += 1

    if i < len(tokens) and tokens[i].type == TokenType.DOT:
        digits += tokens[i].value
        i += 1

        while len(tokens) > i and tokens[i].type == TokenType.DIGIT:
            digits += tokens[i].value
            i += 1

    if digits in {"", "."}:
        raise ValueError("Ivalid Number")

    return Literal(Fraction(digits)), i


def parse_var(tokens: List[Token], i: int) -> Tuple[Variable, int]:
    letters = ""

    while i < len(tokens) and tokens[i].type == TokenType.LETTER:
        letters += tokens[i].value
        i += 1

    if len(letters) != 1:
        raise ValueError(f"Variables must have exactly only one letter")

    return Variable(letters), i