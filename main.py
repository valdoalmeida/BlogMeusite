from meusite import app

# Verifica se o script está sendo executado diretamente (não importado como módulo).
if __name__ == "__main__":
    """
    Este bloco de código é executado somente quando o arquivo 'main.py' é executado diretamente.
    Ele inicia a aplicação Flask em modo de depuração (debug) para facilitar o desenvolvimento.
    """
    app.run(debug=True)  # Executa a aplicação Flask no servidor local com o modo de depuração ativado.

