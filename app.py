# Importa as dependências
from flask import Flask

# Criar um aplicativo chamado 'app' do tipo 'Flask'
app = Flask(__name__)

# Processa a rota "raiz" executando a função logo abaixo
@app.route("/")
def home(): # Função a ser executada
    return "<p>Olá Mundo!</p>" # retorno para o navegador

# Executa o servidor de teste
if __name__ == '__main__':
    app.run(debug=True)