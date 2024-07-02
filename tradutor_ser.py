import re  # Importa o módulo de expressões regulares

def parse_program(code):
    tokens = tokenize(code)  # Tokeniza o código fonte
    return parse_tokens(tokens)  # Chama a função para analisar e interpretar os tokens

def tokenize(code):
    code = code.replace('\n', ' ')  # Remove quebras de linha e substitui por espaços
    tokens = re.findall(r'commence|terminate|begin|end|else|if|input|print|\w+|\d+|[{}():;=]', code)  # Encontra todos os tokens usando expressões regulares
    return tokens  # Retorna a lista de tokens encontrados

def parse_tokens(tokens):
    def parse_block():
        commands = []
        while tokens and tokens[0] not in {'end', 'else', 'terminate'}:  # Enquanto houver tokens e não for encontrado um token de fim de bloco
            commands.append(parse_command())  # Adiciona um comando parseado ao bloco de comandos
        return commands  # Retorna a lista de comandos do bloco

    def parse_command():
        token = tokens.pop(0)  # Remove e retorna o primeiro token da lista
        if token == 'input':
            tokens.pop(0)  # Remove '{'
            var = tokens.pop(0)  # Captura a variável de entrada
            tokens.pop(0)  # Remove '}'
            tokens.pop(0)  # Remove ';'
            return ('input', var)  # Retorna uma tupla indicando um comando de entrada
        elif token == 'print':
            tokens.pop(0)  # Remove '{'
            arg = tokens.pop(0)  # Captura o argumento da impressão
            tokens.pop(0)  # Remove '}'
            tokens.pop(0)  # Remove ';'
            # Retorna uma tupla indicando um comando de impressão, com o tipo do argumento ('FRASE' para string entre aspas, 'VAR' para variável)
            return ('print', ('FRASE', arg)) if arg.startswith('"') and arg.endswith('"') else ('print', ('VAR', arg))
        elif token == 'if':
            tokens.pop(0)  # Remove '('
            cond = parse_condition()  # Analisa a condição do if
            tokens.pop(0)  # Remove ')'
            tokens.pop(0)  # Remove 'begin'
            if_commands = parse_block()  # Analisa o bloco de comandos dentro do if
            tokens.pop(0)  # Remove 'end'
            else_part = None
            if tokens and tokens[0] == 'else':  # Se houver um bloco else
                tokens.pop(0)  # Remove 'else'
                if tokens and tokens[0] == 'if':  # Se for um else if
                    else_part = ('else if', parse_command())  # Analisa o else if
                else:
                    tokens.pop(0)  # Remove 'begin'
                    else_part = ('else', parse_block())  # Analisa o bloco else
                    tokens.pop(0)  # Remove 'end'
            return ('if', cond, if_commands, else_part)  # Retorna uma tupla representando a estrutura condicional if

        elif re.match(r'\w+', token):  # Se o token for um identificador (variável ou declaração)
            var = token
            if tokens[0] == ':':
                tokens.pop(0)  # Remove ':'
                var_type = tokens.pop(0)  # Captura o tipo da variável
                tokens.pop(0)  # Remove ';'
                return ('declaracao', var, var_type)  # Retorna uma tupla indicando uma declaração de variável
            elif tokens[0] == '=':
                tokens.pop(0)  # Remove '='
                expr = parse_expression()  # Analisa a expressão atribuída à variável
                tokens.pop(0)  # Remove ';'
                return ('atribuicao', var, expr)  # Retorna uma tupla indicando uma atribuição de variável

        raise SyntaxError(f'Unexpected token: {token}')  # Lança um erro se encontrar um token inesperado

    def parse_expression():
        token = tokens.pop(0)  # Remove e retorna o primeiro token da lista de tokens
        if re.match(r'\d+', token):  # Se o token for um número
            return token  # Retorna o número como uma string
        elif re.match(r'\w+', token):  # Se o token for um identificador
            return ('VAR', token)  # Retorna uma tupla indicando um identificador (variável)
        elif token in {'+', '-', '*', '/'}:  # Se o token for um operador aritmético
            left = parse_expression()  # Analisa a expressão à esquerda do operador
            op = token  # Captura o operador
            right = parse_expression()  # Analisa a expressão à direita do operador
            return ('operacao', left, op, right)  # Retorna uma tupla indicando uma operação aritmética

        raise SyntaxError(f'Unexpected token in expression: {token}')  # Lança um erro se encontrar um token inesperado em uma expressão

    def parse_condition():
        left = parse_expression()  # Analisa a expressão à esquerda da condição
        op = tokens.pop(0)  # Captura o operador de comparação
        right = parse_expression()  # Analisa a expressão à direita da condição
        return ('condicao', left, op, right)  # Retorna uma tupla indicando uma condição

    tokens.pop(0)  # Remove 'commence' do início do programa
    commands = parse_block()  # Analisa o bloco de comandos principal do programa
    tokens.pop(0)  # Remove 'terminate' do fim do programa
    return ('programa', commands)  # Retorna uma tupla indicando o programa com seus comandos

def traduz_para_python(arvore):
    if arvore[0] == 'programa':  # Se a raiz da árvore for um programa
        python_code = ''
        for comando in arvore[1]:  # Para cada comando no programa
            python_code += traduz_comando_para_python(comando) + '\n'  # Traduz o comando para Python e adiciona ao código Python gerado
        return python_code.strip()  # Retorna o código Python gerado, removendo espaços em branco desnecessários
    elif isinstance(arvore, list):  # Se a raiz da árvore for uma lista (bloco de comandos)
        python_code = ''
        for comando in arvore:  # Para cada comando no bloco de comandos
            python_code += traduz_comando_para_python(comando) + '\n'  # Traduz o comando para Python e adiciona ao código Python gerado
        return python_code.strip()  # Retorna o código Python gerado, removendo espaços em branco desnecessários
    return ''  # Retorna vazio se a árvore estiver vazia ou não reconhecida

def traduz_comando_para_python(comando):
    if comando[0] == 'declaracao':  # Se for uma declaração de variável
        return ''  # Em Python, não é necessário declarar variáveis explicitamente
    elif comando[0] == 'atribuicao':  # Se for uma atribuição de variável
        var = comando[1]  # Captura o nome da variável
        expr = comando[2]  # Captura a expressão atribuída à variável
        if isinstance(expr, tuple) and expr[0] == 'operacao':  # Se a expressão for uma operação aritmética
            left = traduz_argumento_para_python(expr[2])  # Traduz o lado esquerdo da operação
            op = expr[1]  # Captura o operador da operação
            right = traduz_argumento_para_python(expr[3])  # Traduz o lado direito da operação
            return f"{var} = {left} {op} {right}"  # Retorna a atribuição traduzida para Python
        else:  # Se for uma atribuição simples
            return f"{var} = {traduz_argumento_para_python(expr)}"  # Retorna a atribuição traduzida para Python
    elif comando[0] == 'input':  # Se for um comando de entrada
        return f"{comando[1]} = int(input())"  # Retorna a entrada de dados traduzida para Python
    elif comando[0] == 'print':  # Se for um comando de impressão
        return f"print({traduz_argumento_para_python(comando[1])})"  # Retorna o comando de impressão traduzido para Python
    elif comando[0] == 'if':  # Se for uma estrutura condicional if
        condicao = traduz_condicao_para_python(comando[1])  # Traduz a condição do if para Python
        corpo_if = traduz_para_python(comando[2])   # Traduz o corpo do if para Python
        else_part = traduz_else(comando[3]) if comando[3] else ''  # Traduz o bloco else (se existir)
        if else_part:  # Se houver um bloco else
            return f"if {condicao}:\n{indent(corpo_if)}\n{else_part}"  # Retorna a estrutura condicional if-else traduzida para Python
        else:  # Se não houver bloco else
            return f"if {condicao}:\n{indent(corpo_if)}"  # Retorna a estrutura condicional if traduzida para Python

    elif comando[0] == 'else if':  # Se for um bloco else if
        condicao = traduz_condicao_para_python(comando[1])  # Traduz a condição do else if para Python
        corpo_else_if = traduz_para_python(comando[2])  # Traduz o corpo do else if para Python
        return f"elif {condicao}:\n{indent(corpo_else_if)}"  # Retorna o else if traduzido para Python

    elif comando[0] == 'else':  # Se for um bloco else
        corpo_else = traduz_para_python(comando[1])  # Traduz o corpo do else para Python
        return f"else:\n{indent(corpo_else)}"  # Retorna o bloco else traduzido para Python

    elif comando[0] == 'repeticao_for':  # Se for uma estrutura de repetição for
        var_iteracao = comando[1][1]  # Captura a variável de iteração do for
        inicio = traduz_argumento_para_python(comando[3][2][3])  # Traduz o início do intervalo do for para Python
        fim = traduz_argumento_para_python(comando[2][3])  # Traduz o fim do intervalo do for para Python
        corpo_for = traduz_para_python(comando[4])  # Traduz o corpo do for para Python
        return f"for {var_iteracao} in range({inicio}, {fim} + 1):\n{indent(corpo_for)}"  # Retorna o for traduzido para Python

    elif comando[0] == 'repeticao_while':  # Se for uma estrutura de repetição while
        corpo_while = traduz_para_python(comando[2])  # Traduz o corpo do while para Python
        return f"while {traduz_condicao_para_python(comando[1])}:\n{indent(corpo_while)}"  # Retorna o while traduzido para Python

    elif comando[0] == 'bloco':  # Se for um bloco de comandos
        return traduz_para_python(comando[1])  # Traduz o bloco de comandos para Python

    return ''  # Retorna vazio se o comando não for reconhecido

def traduz_else(else_comando):
    if else_comando[0] == 'else if':  # Se for um bloco else if
        condicao = traduz_condicao_para_python(else_comando[1])  # Traduz a condição do else if para Python
        corpo_else_if = traduz_para_python(else_comando[2])  # Traduz o corpo do else if para Python
        else_part = traduz_else(else_comando[3]) if else_comando[3] else ''  # Traduz o bloco else (se existir)
        if else_part:  # Se houver um bloco else
            return f"elif {condicao}:\n{indent(corpo_else_if)}\n{indent(else_part)}"  # Retorna o else if e else traduzidos para Python
        else:  # Se não houver bloco else
            return f"elif {condicao}:\n{indent(corpo_else_if)}"  # Retorna o else if traduzido para Python

    elif else_comando[0] == 'else':  # Se for um bloco else
        corpo_else = traduz_para_python(else_comando[1])  # Traduz o corpo do else para Python
        return f"else:\n{indent(corpo_else)}"  # Retorna o bloco else traduzido para Python

    return ''  # Retorna vazio se o bloco else não for reconhecido

def traduz_argumento_para_python(argumento):
    if isinstance(argumento, str) and argumento.isdigit():  # Se o argumento for uma string contendo apenas dígitos
        return argumento  # Retorna o argumento como está
    elif isinstance(argumento, str):  # Se o argumento for uma string (variável ou frase)
        if argumento.startswith('"') and argumento.endswith('"'):  # Se for uma frase entre aspas
            return argumento  # Retorna a frase como está
        else:  # Se for uma variável
            return argumento  # Retorna a variável como está
    elif isinstance(argumento, tuple) and argumento[0] == 'operacao':  # Se o argumento for uma operação aritmética
        # Retorna a operação aritmética traduzida para Python
        return f"{traduz_argumento_para_python(argumento[1])} {argumento[2]} {traduz_argumento_para_python(argumento[3])}"
    elif isinstance(argumento, tuple) and argumento[0] == 'VAR':  # Se o argumento for uma variável
        return argumento[1]  # Retorna o nome da variável
    return str(argumento)  # Retorna o argumento como uma string

def traduz_condicao_para_python(condicao):
    if len(condicao) == 4:  # Se a condição tiver 4 elementos (comparação entre variáveis ou valores)
        # Retorna a condição comparativa traduzida para Python
        return f"{traduz_argumento_para_python(condicao[1])} {condicao[2]} {traduz_argumento_para_python(condicao[3])}"
    elif len(condicao) == 3:  # Se a condição tiver 3 elementos (condição lógica)
        # Retorna a condição lógica traduzida para Python
        return f"{condicao[0]} {traduz_condicao_para_python(condicao[1])} {traduz_condicao_para_python(condicao[2])}"
    return ''  # Retorna vazio se a condição não for reconhecida

def indent(code, level=1):
    if not code:  # Se o código estiver vazio
        return ''  # Retorna vazio
    indentation = '    ' * level  # Gera a indentação com base no nível especificado
    # Retorna o código indentado com o nível especificado
    return '\n'.join(indentation + line for line in code.split('\n'))