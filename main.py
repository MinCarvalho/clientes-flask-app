from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates', static_url_path='/static', static_folder='static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clientes.db'
database = SQLAlchemy(app)

class Cliente(database.Model):
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    nome = database.Column(database.String(150))
    cpf = database.Column(database.String(20))
    email = database.Column(database.String(150))

    def __init__(self, nome, cpf, email):
        self.nome = nome
        self.cpf = cpf
        self.email = email

# Crie o banco de dados
with app.app_context():
    database.create_all()


@app.route('/')
def index():   
    cliente = Cliente.query.all()
    return render_template('index.html', cliente=cliente)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        cliente = Cliente(request.form['nome'], 
                          request.form['cpf'], 
                          request.form['email'])
        database.session.add(cliente)
        database.session.commit()
        return redirect((url_for('index')))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'] )
def edit(id):
    cliente = Cliente.query.get(id)
    if request.method == 'POST':
        cliente.nome = request.form['nome']
        cliente.cpf = request.form['cpf']
        cliente.email = request.form['email']
        database.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', cliente=cliente)

@app.route('/delete/<int:id>')
def delete(id):
    cliente = Cliente.query.get(id)
    database.session.delete(cliente)
    database.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
