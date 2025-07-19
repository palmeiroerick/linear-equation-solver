from lexer import lexer
from parser import parser
from solver import solver

# TODO: distributive when x multiplies x -> x(a + x)
# TODO: 2 - (3 - x) = 1 -> x = 2 not x = (-4)
# Subtração e divisão são operações não comutativas (a ordem dos operadores importa)
# => ∃a,b:a−b!=b−a
# TODO: Deve ter uma forma melhor de em BinaryOp.__str__() printar não comutatividade

# TODO: Ser mais inteligente nas exceptions do parser
#       Dizendo por exemplo que 2 + = x falta um operador para + não simplismente "list index out of range"


def main():
    tokens = lexer(" (-50x + (-20)) * 100 = 100 * (2 + 1) + 30")
    # tokens = lexer("2 + 2 = x")
    # # tokens = lexer(" -5x + (-2) = 1 * (2 + 1) + 3")
    # tokens = lexer("2 - (3 - 1x) = 1")
    eq = parser(tokens)
    print(solver(eq))


if __name__ == "__main__":
    main()
