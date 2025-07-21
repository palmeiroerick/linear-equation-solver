# TODO: distributive when x multiplies x -> x(a + x)
# TODO: Deve ter uma forma melhor de em BinaryOp.__str__() printar não comutatividade

# TODO: Ser mais inteligente nas exceptions do parser
#       Dizendo por exemplo que 2 + = x falta um operador para + não simplismente "list index out of range"

# TODO: the leftmost element don't need parentheses when it is negative
# print -2 + 3 instead of (-2) + 3

# TODO: (parser) operator must be between operands
# TODO: raise error for close parentheses without open parentheses
# TODO: handle correctly with --a or ++a (multiples MINUS or PLUS together)
# TODO: handle with DIGIT, DOT (without digits after dot)
# TODO: handle unfinished expressions (both <expr> and <term>)

# TODO: (solver) identity and contradiction
# TODO: Associativity
# TODO: Testar divisão por frações (2 + x) / 3/4
# TODO: Coletar denominadores de Fraction() para o lcm
# TODO: quando o numero que multiplica x é uma fração 1/3x
# TODO: quando o denominador é variavel 2/x

# TODO: 2 - (3 - x) = 1 -> x = 2 not x = (-4)
# Subtração e divisão são operações não comutativas (a ordem dos operadores importa)
# => ∃a,b:a−b!=b−a

# Isso é resolvivel? (2 / 3) / x) = 1

# TODO: uma equação linear não pode ser definida sintaticamente é necessario semantica
# portanto o solver prescisa analizar a equação e verificar se ela realmente é linear


def main():
    ...


if __name__ == "__main__":
    main()
