# x + y
# x * y
# x % y
# x / y
# x ** y
# x xor y
# x and y
# x or y
import operator
import string
import itertools

from utilities import random_integer, big_prime

OPERATORS = {'+' : operator.add, '*' : operator.mul, '%' : operator.mod,
             '-' : operator.sub, '/' : operator.div, '**' : operator.pow,
             '^' : operator.xor, '&' : operator.and, '|' : operator.or}
OPERATORS2 = [operator.add, operator.mul, operator.mod, operator.sub,
              operator.pow, operator.div, operator.xor, operator.and,
              operator.or]
ARITHMETIC = ('+', '*', '%', '/', '**')
BOOLEAN = ('^', '&', '|')
LETTERS = string.ascii_letters

def search_for_dh_relation(letters=LETTERS, operators=OPERATORS2):
    # create an add function
    #   - takes n variables
    #   - has n - 1 instructions

    # create a double and add type mul function
    #   - just use basic double and add for now
    # use it for dh key gen/agreement
    # use random parameters for public parameters
    function_generator = make_functions(letters=letters, operators=operators)
    add, add_params = next(function_generator)
    mul = new_double_and_add(add=add) #mul = make_functions(letters=letters, operators=operators)

    dh_params = dict((parameter, random_integer(size)) for parameter in add_params)


def make_functions(variable_range=slice(2, 5), operator_range=(1, 4),
                   letters=LETTERS, operators=OPERATORS2):
    _letters = []
    output = dict()
    for variable_count in range(2, 5):
        _letters.append(letters[variable_count - 2])
        for variables in itertools.product(*_letters):
            _operators = []
            for operator_count in range(1, variable_count + 1):
                _operators.append(operators[operator_count - 1])
            for expression_operators in itertools.product(*_operators):
                variable_operator_pairs = itertools.izip(variables, expression_operators)
                expression = ' '.join("{} {}".format(*item) for item in variable_operator_pairs)
                expression += " {}".format(variables[-1])
                source = "def add(" + ', '.join('{}'.format(item) for item in set(variables)) + "): "
                source += "    return {}".format(expression)
                code = compile(source, '', "exec")
                exec code in output
                yield (output.pop("add"), variables)
                assert not output
