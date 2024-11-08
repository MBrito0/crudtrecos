# Importa as dependências do aplicativo
from flask import Flask, g, make_response, redirect, render_template, request, url_for
from flask_mysqldb import MySQL
import json
from functions.geral import datetime_para_string, remove_prefixo

# Cria um aplicativo Flask chamado "app"
app = Flask(__name__)

# Configurações de acesso ao MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crudtrecos'

# Setup da conexão com MySQL
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['MYSQL_USE_UNICODE'] = True
app.config['MYSQL_CHARSET'] = 'utf8mb4'

# Variável de conexão com o MySQL
mysql = MySQL(app)


@app.before_request
def start():

    # Setup do MySQL para corrigir acentuação
    cur = mysql.connection.cursor()
    cur.execute("SET NAMES utf8mb4")
    cur.execute("SET character_set_connection=utf8mb4")
    cur.execute("SET character_set_client=utf8mb4")
    cur.execute("SET character_set_results=utf8mb4")

    # Setup do MySQL para dias da semana e meses em português
    cur.execute("SET lc_time_names = 'pt_BR'")

    # Lê o cookie do usuário → 'usuario'
    cookie = request.cookies.get('usuario')

    if cookie:
        # Se o cookie existe
        # Converte o cookie JSON para um dicionário Python
        g.usuario = json.loads(cookie)
    else:
        # Se o cookie não existe, a variável do ususário está vazia
        g.usuario = ''

    # # Cria um usuário "fake" para testes
    # # No futuro, isso virá de um cookie
    # g.usuario = {
    #     'id': '1',
    #     'nome': 'Joca da Silva',
    #     'pnome': 'Joca',
    # }


@app.route("/")  # Rota raiz, equivalente a página inicial do site (index)
def index():  # Função executada ao acessar a rota raiz

    # Verifica se o usuário está logado → Pelo cookie
    if g.usuario == '':
        # Se o usuário não está logado
        # Redireciona para a página de login
        return redirect(url_for('login'))

    acao = request.args.get('a')

    # Um SQL de teste para exibir todos os 'trecos' do usuário conectado
    sql = '''
        SELECT t_id, t_foto, t_nome, t_descricao, t_localizacao 
        FROM treco
        WHERE t_usuario = %s 
            AND t_status = 'on'
        ORDER BY t_data DESC
    '''
    cur = mysql.connection.cursor()
    cur.execute(sql, (g.usuario['id'],))
    trecos = cur.fetchall()
    cur.close()

    # Teste de mesa para verificar o retorno dos dados do banco de dados
    # print('\n\n\n', trecos, '\n\n\n')

    # Dados, variáveis e valores a serem passados para o template HTML
    pagina = {
        'titulo': 'CRUDTrecos',
        'usuario': g.usuario,
        'trecos': trecos,
        'acao': acao
    }

    # Renderiza o template HTML, passando valores (pagina) para ele
    return render_template('index.html', **pagina)


# Rota para a página de cadastro de novo treco
@app.route('/novo', methods=['GET', 'POST'])
def novo():  # Função executada para cadastrar novo treco

    # Variável que ativa a mensagem de sucesso no HTML
    sucesso = False

    # Se o formulário foi enviado
    if request.method == 'POST':

        # Obtém os dados preenchidos na forma de dicionário
        form = dict(request.form)

        # Teste de mesa (comente depois dos testes)
        # Verifica se os dados do formulário chegaram ao back-end
        # print('\n\n\n', form, '\n\n\n')

        # Grava os dados no banco de dados
        sql = '''
            INSERT INTO treco (
                t_usuario, t_foto, t_nome, t_descricao, t_localizacao
            ) VALUES (%s, %s, %s, %s, %s)
        '''
        cur = mysql.connection.cursor()
        cur.execute(sql, (
            g.usuario['id'],
            form['foto'],
            form['nome'],
            form['descricao'],
            form['localizacao'],
        ))
        mysql.connection.commit()
        cur.close()

        sucesso = True

    # Dados, variáveis e valores a serem passados para o template HTML
    pagina = {
        'titulo': 'CRUDTrecos - Novo Treco',
        'usuario': g.usuario,
        'sucesso': sucesso,
    }

    # Renderiza o template HTML, passaod valores para ele
    return render_template('novo.html', **pagina)


@app.route('/login', methods=['GET', 'POST'])  # Rota para login de usuário
def login():

    erro = False

    if request.method == 'POST':
        # Se o formulário foi enviado

        # Pega os dados preenchidos no formulário
        form = dict(request.form)

        # Pesquisa se os dados existem no banco de dados → usuario
        # datetime.datetime(2024, 11, 8, 9, 23, 28)
        sql = '''
            SELECT *,
                -- Gera uma versão das datas em pt-BR
                DATE_FORMAT(u_data, '%%d/%%m/%%Y às %%H:%%m') AS u_databr,
                DATE_FORMAT(u_nascimento, '%%d/%%m/%%Y') AS u_nascimentobr
            FROM usuario
            WHERE u_email = %s
                AND u_senha = SHA1(%s)
                AND u_status = 'on'
        '''
        cur = mysql.connection.cursor()
        cur.execute(sql, (form['email'], form['senha'],))
        usuario = cur.fetchone()
        cur.close()

        # Teste mesa
        # print('\n\n\nDICT:', usuario, '\n\n\n')

        if usuario == None:
            # Se o usuário não foi encontrado
            erro = True
        else:
            # Se achou o usuário
            # Apaga a senha do usuário para salvar no cookie
            del usuario['u_senha']

            # Primeiro nome do usuário
            usuario['u_pnome'] = usuario['u_nome'].split()[0]

            # Formata as datas para usar no JSON
            usuario = datetime_para_string(usuario)

            # Remove o prefixo das chaves do dicionário
            cookie_valor = remove_prefixo(usuario)

            # Converte os dados em JSON (texto) para gravar no cookie
            # Porque cookies só aceitam dados na forma de JSON
            cookie_json = json.dumps(cookie_valor)

            # Teste de mesa
            # print('\n\n\nCOOKIE:', cookie_json, '\n\n\n')

            # Prepara a página de destino → index
            resposta = make_response(redirect(url_for('index')))

            # Cria um cookie
            resposta.set_cookie(
                key='usuario',  # Nome do cookie
                value=cookie_json,  # Valor a ser gravado no cookie
                max_age=60 * 60 * 24 * 365  # Validade do cookie em segundos
            )

            # Redireciona para a página de destino → index
            return resposta

    # Dados, variáveis e valores a serem passados para o template HTML
    pagina = {
        'titulo': 'CRUDTrecos - Login',
        'erro': erro
    }

    return render_template('login.html', **pagina)


@app.route('/cadastro', methods=['GET', 'POST'])  # Cadastro de usuário
def cadastro():

    # Dados, variáveis e valores a serem passados para o template HTML
    pagina = {
        'titulo': 'CRUDTrecos - Cadastre-se',
    }

    return render_template('cadastro.html', **pagina)


@app.route('/novasenha', methods=['GET', 'POST'])  # Pedido de senha de usuário
def novasenha():

    # Dados, variáveis e valores a serem passados para o template HTML
    pagina = {
        'titulo': 'CRUDTrecos - Nova Senha'
    }

    return render_template('novasenha.html', **pagina)


@app.route('/perfil')
def perfil():

    # Dados, variáveis e valores a serem passados para o template HTML
    pagina = {
        'titulo': 'CRUDTrecos - Novo Treco',
        'usuario': g.usuario
    }

    # Renderiza o template HTML, passaod valores para ele
    return render_template('perfil.html', **pagina)


@app.route('/apaga/<id>')
def apaga(id):

    # (des)comente o método para apagar conforme o seu caso
    # sql = 'DELETE FROM treco WHERE t_id = %s' # Apaga completamente o treco (CUIDADO!)
    # Altera o status do treco para 'del'
    sql = "UPDATE treco SET t_status = 'del'  WHERE t_id = %s"

    # Executa o SQL
    cur = mysql.connection.cursor()
    cur.execute(sql, (id,))
    mysql.connection.commit()
    cur.close()

    # Retorna para a página anterior
    return redirect(url_for('index', a='apagado'))


@app.route('/logout')
def logout():

    # Página de destino de logout
    resposta = make_response(redirect(url_for('login')))

    # apaga o cookie do usuário
    resposta.set_cookie(
        key='usuario',  # Nome do cookie
        value='',  # Apara o valor do cookie
        max_age=0  # A validade do cookie é ZERO
    )

    # Redireciona para login
    return resposta


# Executa o servidor HTTP se estiver no modo de desenvolvimento
# Remova / comente essas linhas no modo de produção
if __name__ == '__main__':
    app.run(debug=True)
