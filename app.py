from flask import Flask, render_template, request
from flaskext.mysql import MySQL

app = Flask(__name__)

# Instancio o meu objeto do MySQL
mysql = MySQL()

# Estou configurando o meu banco no app

# Nome do usuário do banco de dados
app.config['MYSQL_DATABASE_USER'] = 'root'
# Senha do Banco de dados
app.config['MYSQL_DATABASE_PASSWORD'] = 'NpmFmMxjmSXk46k'
# Nome do banco de dados que voce quer gerenciar no projeto (Importante ter um banco com esse nome criado)
app.config['MYSQL_DATABASE_DB'] = 'aula3'
# URL para acessar o banco de dados, caso tenha o banco baixado localmente, normalmente será 'localhost'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/signup', methods=['POST', 'GET'])
def post():  # Método de criar dado
    try:
        # Estou resgatando as variaveis do meu formulario
        # IMPORTANTE: O resgate é feito com base no 'name' que voce coloca no input
        _name = request.form['name']
        _email = request.form['email']
        _password = request.form['password']

        if _name and _password and _email:
            conn = mysql.connect()
            cursor = conn.cursor()

            # Aqui estou criando uma variavel apenas para receber a string do query
            # Na variavel 'value' eu passo os dados que é passado no formulário
            sql = "INSERT INTO tb_users(name, email, password) VALUES (%s, %s, %s)"
            value = (_name, _email, _password)

            # Eu chamo o cursor do meu mysql e rodo o comando execute, para executar a query
            # Primeiro parametro é a query e o segundo os dados que quero substituir no value(%s)
            cursor.execute(sql, value)
            conn.commit()

    except Exception as e:
        # eu printo o que deu de erro na minha execução no banco
        print("Problem inserting into db: " + str(e))
    finally:
        # O finally vai ser executado independente se der erro ou não, no final ele irá renderizar a tela de do form
        return render_template('index.html')


@app.route('/list', methods=['POST', 'GET'])
def index():
    # Instancio a conexão do banco e separo em uma outra variavel o cursor para execução das queries
    conn = mysql.connect()
    cursor = conn.cursor()

    # Aqui estou criando uma variavel apenas para receber a string do query
    query = 'SELECT name, email, password FROM tb_users'
    cursor.execute(query)

    # Resgato o resultado do meu SELECT
    data = cursor.fetchall()

    # Renderizo meu HTML passando o que retorna da minha pesquisa no banco
    return render_template('list.html', data=data)


if __name__ == '__main__':
    app.debug = True
    app.run()

# BANCO

# Para criar o banco de dados é essa query a seguir
# CREATE DATABASE aula3

# Criação da tabela:

# create table tb_users (
#	id int auto_increment primary key,
#	name varchar(100) not null,
#   email varchar(255) not null,
#   password varchar(255) not null
# );
