from llvmlite import ir
import io

# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables -- all in one file.
# -----------------------------------------------------------------------------

reserved = {
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'fun': 'FUN',
    'end': 'END'
}

tokens = (
    'COMMA',
    'NAME', 'NUMBER',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS',
    'LPAREN', 'RPAREN', 'SEMI'
) + tuple(reserved.values())

# Tokens

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_FUN = r'fun'
t_END = r'end'
t_COMMA = r','
t_SEMI = r';'


def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'NAME')    # Check for reserved words
    return t


def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


# Ignored characters
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
import ply.lex as lex

# Parsing rules

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),
)

# dictionary of names
names = {}


def p_statements(t):
    '''statements : statement
                  | statement SEMI
                  | statement SEMI statements'''
    t[0] = t[1]


def p_statement_fun(t):
    #'statement : FUN NAME LPAREN arguments RPAREN statements END'
    'statement : FUN NAME LPAREN arguments RPAREN statements END'
    print("fun {}".format(t[2]))
    t[0] = t[1]


def p_statement_assign(t):
    'statement : NAME EQUALS expression'
    name = t[3]
    names[t[1]] = name
    generator.g_var(name)


def p_statement_expr(t):
    'statement : expression'
    print(t[1])


def p_arguments_none(t):
    'arguments : '

    t[0] = []


def p_arguments_one(t):
    'arguments : NAME'
    t[0] = [t[1]]


def p_arguments_many(t):
    'arguments : NAME COMMA arguments'
    t[0] = l = [t[1]]
    l.extend(t[3])


def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if t[2] == '+':
        t[0] = t[1] + t[3]
    elif t[2] == '-':
        t[0] = t[1] - t[3]
    elif t[2] == '*':
        t[0] = t[1] * t[3]
    elif t[2] == '/':
        t[0] = t[1] / t[3]


def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = -t[2]


def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]


def p_expression_number(t):
    'expression : NUMBER'
    t[0] = t[1]


def p_expression_name(t):
    'expression : NAME'
    try:
        t[0] = names[t[1]]
    except LookupError:
        print("Undefined name '%s'" % t[1])
        t[0] = 0


def p_error(t):
    # tok = parser.parser.token()
    if t is not None:
        print("Syntax error at '{}' at line {}.".format(
            t.value, t.lineno
        ))
    else:
        print("Some mystic error happend.")


import ply.yacc as yacc

generator = None


class Generator(object):
    def __init__(self):
        global generator

        self.parser = yacc.yacc()
        self.int_type = ir.IntType(64)
        self.setup_main_context()
        generator = self

    def parse(self, s):
        return self.parser.parse(s)

    def setup_main_context(self):
        self.main_context = None
        self.set_module()

    def set_module(self):
        self.module = ir.Module("__main__")

    def g_var(self, name):
        var = ir.GlobalVariable(self.module, self.int_type, name)

    def print(self):
        o = io.StringIO()
        print(self.module, file=o)
        return o.getvalue()


lexer = None
parser = None


def new_parser():
    global parser, lexer
    lexer = lex.lex()
    parser = yacc.yacc()


def pars_test_interactive():
    while True:
        try:
            s = input('calc > ')   # Use raw_input on Python 2
        except EOFError:
            break
        parser.parse(s)
