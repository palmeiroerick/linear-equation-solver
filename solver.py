import operator as op
from typing import List, Union
from data import Node, Root, Literal, Variable, BinaryOp


def has_variable(node: Node) -> bool:
    # verifica se node ou seus filhos contém variável
    if isinstance(node, Variable):
        return True
    if isinstance(node, BinaryOp):
        return has_variable(node.left) or has_variable(node.right)
    return False


def has_literal(node: Node) -> bool:
    # verifica se node ou seus filhos contém literal
    if isinstance(node, Literal):
        return True
    if isinstance(node, BinaryOp):
        return has_literal(node.left) or has_literal(node.right)
    return False


def solver(eq: Root) -> Root:
    eq.left = solve_expr(eq.left)
    eq.right = solve_expr(eq.right)

    # ax = b -> x = b / a
    if isinstance(eq.left, Variable) and isinstance(eq.right, Literal):
        return Root(Variable(), Literal(eq.right.value / eq.left.coef))

    # a = bx -> x = a / b:
    if isinstance(eq.left, Literal) and isinstance(eq.right, Variable):
        return Root(Variable(), Literal(eq.left.value / eq.right.coef))

    # x/a = c/b + dx -> l = lcm(a,b): lx/a = l(c/b + dx)
    # TODO: isso supostamente só deveria ser usado para divisão de x por um literal
    # Ele resolve isso encontrando o lcm de todas os literais que dividem x (denominadores),
    # multiplica left e right pelo lcm e aplica a distributiva para remover todas as frações de x por um literal
    # Caso haja uma divisão de litereral por literal ela deve ser resolvida por solver
    # if contains_fraction(eq):
    #     denominators: list[int] = []

    #     def get_denominators(node: Node):
    #         if isinstance(node, Root):
    #             get_denominators(node.left)
    #             get_denominators(node.right)

    #         if isinstance(node, BinaryOp):
    #             if node.op == "/":
    #                 denominators.append(node.right.value)
    #             else:
    #                 get_denominators(node.left)
    #                 get_denominators(node.right)

    #         return

    #     get_denominators(eq)
    #     l: int = lcm(*denominators)
    #     # return solve(Root(distribute(eq.left, l), distribute(eq.right, l)))
    #     return Root(distribute(eq.left, l), distribute(eq.right, l))

    # ax + b = c + dx -> ax + (-dx) = c + (-b)
    if has_variable(eq.right) or has_literal(eq.left):

        def extract_terms(node: Node) -> List[Literal | Variable]:
            if isinstance(node, BinaryOp):
                return extract_terms(node.left) + extract_terms(node.right)

            if isinstance(node, (Literal, Variable)):
                return [node]

            return []

        left_terms: List[Literal | Variable] = extract_terms(eq.left)
        right_terms: List[Literal | Variable] = extract_terms(eq.right)

        def invert(node: Union[Literal, Variable]) -> Node:
            if isinstance(node, Variable):
                return Variable(coef=node.coef * -1)

            return Literal(node.value * -1)

        eq = Root(None, None)  # type: ignore

        for term in left_terms:
            if isinstance(term, Variable):
                if eq.left:
                    eq.left = BinaryOp("+", eq.left, term)
                else:
                    eq.left = term
            else:
                if eq.right:
                    eq.right = BinaryOp("+", eq.right, invert(term))
                else:
                    eq.right = invert(term)

        for term in right_terms:
            if isinstance(term, Variable):
                if eq.left:
                    eq.left = BinaryOp("+", eq.left, invert(term))
                else:
                    eq.left = invert(term)
            else:
                if eq.right:
                    eq.right = BinaryOp("+", eq.right, term)
                else:
                    eq.right = term

        return solver(eq)

    return eq


def solve_expr(expr: Node) -> Node:
    if isinstance(expr, (Literal, Variable)):
        return expr

    if isinstance(expr, BinaryOp):
        left = solve_expr(expr.left)
        right = solve_expr(expr.right)

        # Apply Distributive
        if (
            expr.op == "*"
            and isinstance(expr.left, Literal)
            and isinstance(expr.right, BinaryOp)
        ):
            return solve_expr(distributive(expr.right, expr.left))

        if (
            expr.op == "*"
            and isinstance(expr.left, BinaryOp)
            and isinstance(expr.right, Literal)
        ):
            return solve_expr(distributive(expr.left, expr.right))

        # Evaluate an operation with literal operands
        if isinstance(left, Literal) and isinstance(right, Literal):
            operations = {"+": op.add, "-": op.sub, "*": op.mul, "/": op.truediv}
            return Literal(operations[expr.op](left.value, right.value))

        # Combine like terms with the variable "x"
        if isinstance(left, Variable) and isinstance(right, Variable):
            return Variable(coef=left.coef + right.coef)

        # Transforms a * x into ax
        if expr.op == "*" and isinstance(left, Literal) and isinstance(right, Variable):
            return Variable(coef=right.coef * left.value)

        # Transforms x * a into ax
        if expr.op == "*" and isinstance(left, Variable) and isinstance(right, Literal):
            return Variable(coef=left.coef * right.value)

        # ax / b -> (a/b)x
        if expr.op == "/" and isinstance(left, Variable) and isinstance(right, Literal):
            return Variable(coef=left.coef / right.value)

        return BinaryOp(expr.op, left, right)

    return expr


def distributive(node: Node, multiplier: Literal) -> Node:
    if isinstance(node, (Literal, Variable)):
        return BinaryOp("*", multiplier, node)

    if isinstance(node, BinaryOp):
        if node.op == "+":
            return BinaryOp(
                "+",
                distributive(node.left, multiplier),
                distributive(node.right, multiplier),
            )

        if node.op == "-":
            return BinaryOp(
                "-",
                distributive(node.left, multiplier),
                distributive(node.right, multiplier),
            )

        if node.op == "/":
            return BinaryOp("/", BinaryOp("*", multiplier, node.left), node.right)

        if node.op == "*":
            return BinaryOp("*", BinaryOp("*", multiplier, node.left), node.right)

    return node
