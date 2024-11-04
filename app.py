# Importa as dependências do aplicativo
from flask import Flask, render_template

# Cria um aplicativo Flask chamado "app"
app = Flask(__name__)

# Rota raiz, equivalente a páginai inicial do site (index)
@app.route("/")
def home(): # Função executada ao acessar a rota raiz

    # Cria um usuário "fake" para testes
    # No futuro, isso virá de um cookie
    usuario = {
        'nome': 'Joca da Silva',
        'id': '1'
    }
    
    # Extrai apenas o primeiro nome do usuário
    usuario['pnome'] = usuario['nome'].split()[0]

    # Dados, variáveis e valores a serem passados para o template HTML
    pagina = {
        'titulo': 'CRUDTrecos',
        'usuario': usuario
    }

    # Renderiza o template HTML, passaod valores para ele
    return render_template('_template.html', **pagina)

# Executa o servidor HTTP se estiver no modo de desenvolvimento
# Remova / comente essas linhas no modo de produção
if __name__ == '__main__':
    app.run(debug=True)
