from flask_login import UserMixin
from database import db


class Produto(UserMixin, db.Model):
    Produto_ID = db.Column(
        db.Integer, primary_key=True
    )  # primary keys are required by SQLAlchemy
    Fornecedor_ID = db.Column(db.Integer)
    Categoria_ID = db.Column(db.String(100))
    P_Modelo = db.Column(db.String(100))
    P_ValorUnitario = db.Column(db.Float)
    P_nome = db.Column(db.String(100))
    P_Marca = db.Column(db.String(100))
    P_Imagem = db.Column(db.String(1000))


class Fornecedor(UserMixin, db.Model):
    Fornecedor_ID = db.Column(
        db.Integer, primary_key=True
    )  # primary keys are required by SQLAlchemy
    F_Primeiro_Nome = db.Column(db.String(45))
    F_Segundo_Nome = db.Column(db.String(45))
    F_Num_Documento = db.Column(db.String(45))
    F_Tipo_Documento = db.Column(db.String(45))
    F_Telefone_1 = db.Column(db.String(45))
    F_Telefone_2 = db.Column(db.String(45))
    F_Email = db.Column(db.String(45))
    F_Provincia = db.Column(db.String(45))
    F_Distrito = db.Column(db.String(45))
    F_Quarteirao = db.Column(db.String(45))
    F_Bairro = db.Column(db.String(45))
    F_Rua = db.Column(db.String(45))


class Categoria(UserMixin, db.Model):
    __tablename__ = "categoria"
    Categoria_ID = db.Column(db.Integer, primary_key=True)
    C_Nome = db.Column(db.String(45))


class Usuario(UserMixin, db.Model):
    Usuario_ID = db.Column(db.Integer, primary_key=True)
    U_Nome = db.Column(db.String(45))
    U_Email = db.Column(db.String(45))
    U_Senha = db.Column(db.String(45))
    U_Endereco = db.Column(db.String(200))
    U_Celular = db.Column(db.String(50))

    def get_id(self):
        return self.Usuario_ID


class Carrinho(UserMixin, db.Model):
    Cart_ID = db.Column(db.Integer, primary_key=True)
    Usuario_ID = db.Column(db.Integer)
    Produto_ID = db.Column(db.Integer)
    Quantidade = db.Column(db.Integer)
    Total_A_Pagar = db.Column(db.Integer)

    def get_id(self):
        return self.Cart_ID


class Pedido(UserMixin, db.Model):
    Pedido_ID = db.Column(db.Integer, primary_key=True)
    Usuario_ID = db.Column(db.Integer)
    Produto_ID = db.Column(db.Integer)
    Quantidade = db.Column(db.Integer)
    Total_A_Pagar = db.Column(db.Integer)

    def get_id(self):
        return self.Pedido_ID


class Comentario(UserMixin, db.Model):
    Comment_ID = db.Column(db.Integer, primary_key=True)
    Usuario_ID = db.Column(db.Integer)
    Produto_ID = db.Column(db.Integer)
    C_Mensagem = db.Column(db.String(200))
