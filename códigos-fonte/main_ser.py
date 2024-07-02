import os
import ply.lex as lex
import ply.yacc as yacc
from lexer_ser import tokens, lexer
from parser_ser import parser
from tradutor_ser import traduz_para_python

def tokenizar_arquivo(nome_arquivo):
    """Função para tokenizar o conteúdo de um arquivo.

    Args:
        nome_arquivo (str): Nome do arquivo a ser tokenizado.

    Returns:
        list: Lista de tokens encontrados no arquivo.
    """
    with open(nome_arquivo, 'r') as file:
        data = file.read()

    lexer.input(data)
    tokens_result = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens_result.append(str(tok))
    return tokens_result

def analisar_arquivo(nome_arquivo):
    """Função para realizar a análise sintática de um arquivo.

    Args:
        nome_arquivo (str): Nome do arquivo a ser analisado.

    Returns:
        tuple or None: Resultado da análise sintática, se bem sucedida.
    """
    with open(nome_arquivo, 'r') as file:
        data = file.read()

    result = parser.parse(data, lexer=lexer)
    return result

def traduzir_arquivo(nome_arquivo):
    """Função para traduzir o conteúdo de um arquivo para Python.

    Args:
        nome_arquivo (str): Nome do arquivo a ser traduzido.

    Returns:
        str or None: Código Python traduzido, se a análise sintática for bem sucedida.
    """
    with open(nome_arquivo, 'r') as file:
        data = file.read()

    result = parser.parse(data, lexer=lexer)
    if result:
        codigo_python = traduz_para_python(result)
        return codigo_python
    return None

def salvar_resultado(nome_arquivo, resultado, pasta_resultados):
    """Função para salvar o resultado em um arquivo.

    Args:
        nome_arquivo (str): Nome do arquivo onde o resultado será salvo.
        resultado (str): Resultado a ser salvo no arquivo.
        pasta_resultados (str): Pasta onde o arquivo será salvo.
    """
    if not os.path.exists(pasta_resultados):
        os.makedirs(pasta_resultados)

    with open(os.path.join(pasta_resultados, nome_arquivo), 'w') as file:
        file.write(resultado)

def main():
    """Função principal que executa todas as etapas: tokenização, análise sintática e tradução."""
    arquivos = ['entrada_saida.ser', 'condicao.ser', 'repeticao.ser']
    resultados_tokens = ['resultado_entrada_saida_tokens.txt', 'resultado_condicao_tokens.txt', 'resultado_repeticao_tokens.txt']
    resultados_sintaxe = ['resultado_entrada_saida_sintaxe.txt', 'resultado_condicao_sintaxe.txt', 'resultado_repeticao_sintaxe.txt']
    resultados_traducao = ['resultado_entrada_saida_traducao.py', 'resultado_condicao_traducao.py', 'resultado_repeticao_traducao.py']

    pasta_tokens = 'resultados_tokens'
    pasta_sintaxe = 'resultados_sintaxe'
    pasta_traducao = 'resultados_traducao'

    for i in range(len(arquivos)):
        nome_arquivo = arquivos[i]

        # Captura de tokens
        tokens_result = tokenizar_arquivo(nome_arquivo)
        salvar_resultado(resultados_tokens[i], "Tokens:\n" + "\n".join(tokens_result), pasta_tokens)

        # Análise Sintática
        sintaxe_result = analisar_arquivo(nome_arquivo)
        salvar_resultado(resultados_sintaxe[i], "Analise Sintatica:\n" + str(sintaxe_result), pasta_sintaxe)

        # Tradução para Python
        traducao_result = traduzir_arquivo(nome_arquivo)
        if traducao_result:
            salvar_resultado(resultados_traducao[i], "#Codigo Python traduzido:\n" + traducao_result, pasta_traducao)
        else:
            salvar_resultado(resultados_traducao[i], "Erro de analise sintatica.", pasta_traducao)

if __name__ == '__main__':
    main()
