import ply.lex as lex
import ply.yacc as yacc
import statistics
import os


""" Exemplo sentenças no terminal
load x.txt
media 
moda 
frequencia and mediana

"""



# Tokens foram modificados { 

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

# }


# Não modificados {
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()
# }


# regras de precedências modificado {
precedence = (
    ('left', 'AND'),
)
# }


# Para armazenar o array que veio do arquivo txt
current_array = []


# Produções modificas { 

# S -> C | E 
def p_start(p):
    '''
    start : command
          | expression
    '''          
    print(p[1])


# C -> LOAD NAME
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
    
# C -> EXIT
def p_command_exit(p):
    'command : EXIT'
    exit()


# Regra para a expressão
# E -> F | E AND E (expresão com a recursão à esquerda, sem o não terminal G)
def p_expression(p):
    '''
    expression : F
               | expression AND expression
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == 'and':
        p[0] = p[1] + p[3]

# F -> MEDIA
def p_function_media(p):
    'F : MEDIA'
    global current_array
    if current_array:
        media = statistics.mean(current_array)
        
        p[0] = f'\nMédia: {media:.2f}'
    else:
        print("Sem array para utilização.")

# F -> MEDIANA
def p_function_mediana(p):
    'F : MEDIANA'
    global current_array
    if current_array:
        mediana = statistics.median(current_array)
        p[0] = f'\nMediana: {mediana}'
    else:
        print("Sem array para utilização.")

# F -> MODA
def p_function_moda(p):
    'F : MODA'
    global current_array
    if current_array:
        moda = statistics.mode(current_array)
        p[0] = f'\nModa: {moda}'
    else:
        print("Sem array para utilização.")

# F -> FREQUENCIA
def p_function_frequencia(p):
    'F : FREQUENCIA'
    global current_array
    if current_array:
        freq = {num: current_array.count(num) for num in set(current_array)}
        p[0] = f'\nFrequencia absoluta: {freq}'        
    else:
        print("Sem array para utilização.")

# } 

# Daqui para baixo, sem modificações que intereferem em algo

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
