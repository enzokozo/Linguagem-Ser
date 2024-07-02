import ply.yacc as yacc
from lexer_ser import tokens  # Importa os tokens do lexer

# Definir precedência dos operadores
precedence = (
    ('left', 'SOMA', 'SUBTRACAO'),
    ('left', 'MULTIPLICACAO', 'DIVISAO', 'MOD', 'ARITMETICO'),
    ('right', 'NOT'),
    ('left', 'AND', 'OR'),
)

# Regras de produção

# Regra para o programa completo
def p_programa(p):
    '''programa : INICIO comandos FIM'''
    p[0] = ('programa', p[2])

# Regra para múltiplos comandos
def p_comandos(p):
    '''comandos : comando comandos 
                | comando'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]

# Regra para um único comando
def p_comando(p):
    '''comando : declaracao PONTOVIRGULA
               | atribuicao PONTOVIRGULA
               | input PONTOVIRGULA
               | print PONTOVIRGULA
               | condicional
               | repeticao_for
               | repeticao_while
               | bloco'''
    p[0] = p[1]

# Regra para declaração de variáveis
def p_declaracao(p):
    '''declaracao : VAR DOISPONTOS tipo'''
    p[0] = ('declaracao', p[1], p[3])

# Regra para tipos (int, real, char)
def p_tipo(p):
    '''tipo : INT
            | REAL
            | CHAR'''
    p[0] = p[1]

# Regra para atribuição de valores a variáveis
def p_atribuicao(p):
    '''atribuicao : VAR RECEBE VAR  
                  | VAR RECEBE NUMERO 
                  | VAR RECEBE operacao'''
    p[0] = ('atribuicao', p[1], p[3])

# Regra para entrada de dados (input)
def p_input(p):
    '''input : INPUT ABRECHAVES VAR FECHACHAVES'''
    p[0] = ('input', p[3])

# Regra para saída de dados (print)
def p_print(p):
    '''print : PRINT ABRECHAVES VAR FECHACHAVES
             | PRINT ABRECHAVES FRASE FECHACHAVES'''
    p[0] = ('print', p[3])

# Regra para estruturas condicionais (if-else)
def p_condicional(p):
    '''condicional : IF ABREPARENTESES condicao FECHAPARENTESES INICIOBLOCO comandos FIMBLOCO else'''
    p[0] = ('if', p[3], p[6], p[8])

# Regra para o bloco else
def p_else(p):
    '''else : ELSE condicional
            | ELSE INICIOBLOCO comandos FIMBLOCO
            | empty'''
    if len(p) == 3:
        p[0] = ('else', p[2])
    elif len(p) == 5:
        p[0] = ('else', p[3])
    else:
        p[0] = None

# Regra para estruturas de repetição (for)
def p_repeticao_for(p):
    '''repeticao_for : FOR ABREPARENTESES atribuicao PONTOVIRGULA condicao PONTOVIRGULA atribuicao FECHAPARENTESES INICIOBLOCO comandos FIMBLOCO'''
    p[0] = ('repeticao_for', p[3], p[5], p[7], p[10])

# Regra para estruturas de repetição (while)
def p_repeticao_while(p):
    '''repeticao_while : WHILE ABREPARENTESES condicao FECHAPARENTESES INICIOBLOCO comandos FIMBLOCO'''
    p[0] = ('repeticao_while', p[3], p[6])

# Regra para blocos delimitados (início e fim)
def p_bloco(p):
    '''bloco : INICIOBLOCO comandos FIMBLOCO'''
    p[0] = ('bloco', p[2])

# Regra para condições (lógicas ou relacionais)
def p_condicao(p):
    '''condicao : condicao_logica
                | condicao_relacional'''
    p[0] = p[1]

# Regra para condições lógicas (AND, OR, NOT)
def p_condicao_logica(p):
    '''condicao_logica : condicao_logica AND condicao_logica
                       | condicao_logica OR condicao_logica
                       | NOT condicao'''
    if len(p) == 4:
        p[0] = ('logica', p[1], p[2], p[3])
    elif len(p) == 3:
        p[0] = ('logica', p[1], None, p[2])

# Regra para condições relacionais (==, >=, >, <=, <, !=)
def p_condicao_relacional(p):
    '''condicao_relacional : VAR RELACIONAL VAR
                           | VAR RELACIONAL NUMERO'''
    p[0] = ('relacional', p[1], p[2], p[3])

# Regra para operações aritméticas (++, --, +, -, *, /)
def p_operacao(p):
    '''operacao : VAR INCREMENTA
                | VAR DECREMENTA
                | VAR ARITMETICO VAR
                | VAR ARITMETICO NUMERO'''
    p[0] = ('operacao', p[2], p[1], p[3])

# Regra para produção vazia
def p_empty(p):
    'empty :'
    pass

# Função para lidar com erros de sintaxe
def p_error(p):
    if p:
        print(f"Erro de sintaxe próximo a '{p.value}' na linha {p.lineno}.")
    else:
        print("Erro de sintaxe inesperado.")

# Constrói o parser
parser = yacc.yacc()