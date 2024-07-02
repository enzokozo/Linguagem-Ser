import ply.lex as lex

# Lista de nomes de tokens
tokens = [
    'INICIO', 'FIM',      # Tokens para INICIO e FIM
    'INT', 'REAL', 'CHAR', 'VAR', 'LETRA', 'DIGITO', 'NUMERO', 'DECIMAL', 'ARGUMENTO', 'FRASE',  # Tokens para tipos e identificadores
    'INPUT', 'PRINT',     # Tokens para INPUT e PRINT
    'IF', 'ELSE', 'FOR', 'WHILE',  # Tokens para estruturas condicionais e de repetição
    'RECEBE', 'RELACIONAL', 'IGUAL', 'MAIORIGUAL', 'MAIOR', 'MENORIGUAL', 'MENOR', 'DIFERENTE',  # Tokens para operadores relacionais
    'AND', 'OR', 'NOT', 'LOGICO',  # Tokens para operadores lógicos
    'SOMA', 'SUBTRACAO', 'MULTIPLICACAO', 'DIVISAO', 'MOD', 'INCREMENTA', 'DECREMENTA', 'ARITMETICO',  # Tokens para operadores aritméticos
    'SEPARADOR', 'ABREASPAS', 'FECHAASPAS', 'DOISPONTOS', 'PONTOVIRGULA', 'ABREPARENTESES', 'FECHAPARENTESES',  # Tokens para símbolos diversos
    'ABRECHAVES', 'FECHACHAVES', 'INICIOBLOCO', 'FIMBLOCO'  # Tokens para delimitadores de bloco
]

# Palavras reservadas
reserved = {
    'commence': 'INICIO',    # Palavra reservada para o token INICIO
    'terminate': 'FIM',      # Palavra reservada para o token FIM
    'int': 'INT',            # Palavra reservada para o token INT
    'real': 'REAL',          # Palavra reservada para o token REAL
    'char': 'CHAR',          # Palavra reservada para o token CHAR
    'input': 'INPUT',        # Palavra reservada para o token INPUT
    'print': 'PRINT',        # Palavra reservada para o token PRINT
    'if': 'IF',              # Palavra reservada para o token IF
    'else': 'ELSE',          # Palavra reservada para o token ELSE
    'for': 'FOR',            # Palavra reservada para o token FOR
    'while': 'WHILE',        # Palavra reservada para o token WHILE
    'AND': 'AND',            # Palavra reservada para o token AND
    'OR': 'OR',              # Palavra reservada para o token OR
    'NOT': 'NOT',            # Palavra reservada para o token NOT
    'begin': 'INICIOBLOCO',  # Palavra reservada para o token INICIOBLOCO
    'end': 'FIMBLOCO'        # Palavra reservada para o token FIMBLOCO
}

# Expressões regulares para tokens simples

# Símbolos reservados para operadores relacionais
t_RECEBE = r'='
t_IGUAL = r'=='
t_MAIORIGUAL = r'>='
t_MAIOR = r'>'
t_MENORIGUAL = r'<='
t_MENOR = r'<'
t_DIFERENTE = r'!='

# Símbolos reservados para operadores aritméticos
t_SOMA = r'\+'
t_SUBTRACAO = r'-'
t_MULTIPLICACAO = r'\*'
t_DIVISAO = r'/'
t_MOD = r'%'
t_INCREMENTA = r'\+\+'
t_DECREMENTA = r'--'

# Símbolo reservado para separadores
t_SEPARADOR = r'[.,]'

# Símbolos reservados para delimitadores
t_ABREASPAS = r'\"'
t_FECHAASPAS = r'\"'
t_DOISPONTOS = r':'
t_PONTOVIRGULA = r';'
t_ABREPARENTESES = r'\('
t_FECHAPARENTESES = r'\)'
t_ABRECHAVES = r'\{'
t_FECHACHAVES = r'\}'

# Função para operadores aritméticos
def t_ARITMETICO(t):
    r'\+|-|\*|/|%'
    return t

# Função para operadores relacionais
def t_RELACIONAL(t):
    r'==|>=|>|<=|<|!='
    return t

# Função para identificar variáveis (identificadores)
def t_VAR(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = reserved.get(t.value, 'VAR')  # Checa se é uma palavra reservada
    return t

# Função para identificar números decimais
def t_DECIMAL(t):
    r'-?[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t

# Função para identificar números inteiros
def t_NUMERO(t):
    r'-?[0-9]+'
    t.value = int(t.value)
    return t

# Função para identificar letras
def t_LETRA(t):
    r'[a-zA-Z0-9]'
    return t

# Função para identificar frases delimitadas por aspas duplas
def t_FRASE(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t

# Ignora espaços em branco e tabulações
t_ignore = ' \t'

# Trata quebra de linha
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Trata erros de caracteres inválidos
def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)

# Constrói o lexer
lexer = lex.lex()
