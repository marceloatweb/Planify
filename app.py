from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Caminho do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///planify.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo da tabela de lançamentos
class Lancamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    data = db.Column(db.String(10), nullable=False)  # Formato DD/MM/AAAA
    metodo_pagamento = db.Column(db.String(50), nullable=False)

# Criar o banco de dados
with app.app_context():
    db.create_all()

@app.route('/lancamentos', methods=['POST'])
def adicionar_lancamento():
    dados = request.json
    novo_lancamento = Lancamento(
        descricao=dados['descricao'],
        valor=dados['valor'],
        categoria=dados['categoria'],
        data=dados['data'],
        metodo_pagamento=dados['metodo_pagamento']
    )
    db.session.add(novo_lancamento)
    db.session.commit()
    return jsonify({"mensagem": "Lançamento adicionado com sucesso!"})

@app.route('/lancamentos', methods=['GET'])
def listar_lancamentos():
    lancamentos = Lancamento.query.all()
    lista = [{"id": l.id, "descricao": l.descricao, "valor": l.valor,
              "categoria": l.categoria, "data": l.data, "metodo_pagamento": l.metodo_pagamento}
             for l in lancamentos]
    return jsonify(lista)

@app.route('/lancamentos/<int:id>', methods=['DELETE'])
def excluir_lancamento(id):
    lancamento = Lancamento.query.get(id)
    if lancamento:
        db.session.delete(lancamento)
        db.session.commit()
        return jsonify({"mensagem": "Lançamento excluído com sucesso!"})
    return jsonify({"erro": "Lançamento não encontrado!"}), 404


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

