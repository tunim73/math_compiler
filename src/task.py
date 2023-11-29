import ply.lex as lex
import ply.yacc as yacc
import statistics
import os

tokens = (
    'LOAD', 'NAME', 'EXIT', 'AND', 'MEDIA', 'MEDIANA', 'MODA', 'FREQUENCIA'
)

t_LOAD = r'load'
t_EXIT = r'exit'
t_AND = r'and'
t_MEDIA = r'media'
t_MEDIANA = r'mediana'
t_MODA = r'moda'
t_FREQUENCIA = r'frequencia'

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*\.txt'
    return t

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

precedence = (
    ('left', 'AND'),
)
current_array = []

def p_start(p):
    '''
    start : command
          | expression
    '''          
    print(p[1])



def p_command_load(p):
    'command : LOAD NAME'
    filename = p[2]
    
    if not filename.endswith('.txt'):
        print("Formato de arquivo invalido, tem que ser .txt")
        return

    if not os.path.isabs(filename):
        filename = os.path.abspath(filename)

    try:
        with open(filename, 'r') as file:
            content = file.read()
            array = [int(num) for num in content.split()]
            global current_array
            current_array = array
            p[0] = 'Array carregado com sucesso!'

    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except ValueError:
        print(f"Array no '{filename}' no formato incorreto. Use espaço ' ' como separador")
    
def p_command_exit(p):
    'command : EXIT'
    exit()



# Regra para a expressão
def p_expression(p):
    '''
    expression : F
               | expression AND expression
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == 'and':
        p[0] = p[1] + p[3]



def p_function_media(p):
    'F : MEDIA'
    global current_array
    if current_array:
        media = statistics.mean(current_array)
        
        p[0] = f'\nMédia: {media:.2f}'
    else:
        print("Sem array para utilização.")

def p_function_mediana(p):
    'F : MEDIANA'
    global current_array
    if current_array:
        mediana = statistics.median(current_array)
        p[0] = f'\nMediana: {mediana}'
    else:
        print("Sem array para utilização.")

def p_function_moda(p):
    'F : MODA'
    global current_array
    if current_array:
        moda = statistics.mode(current_array)
        p[0] = f'\nModa: {moda}'
    else:
        print("Sem array para utilização.")

def p_function_frequencia(p):
    'F : FREQUENCIA'
    global current_array
    if current_array:
        freq = {num: current_array.count(num) for num in set(current_array)}
        p[0] = f'\nFrequencia absoluta: {freq}'        
    else:
        print("Sem array para utilização.")



# Regra para lidar com erros de sintaxe
def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

while True:
    try:
        s = input('> ')
    except EOFError:
        break
    if not s:
        continue
    yacc.parse(s)
