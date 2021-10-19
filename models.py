from .app import db

class Produto(db.Model):
    Produto_ID= db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    Fornecedor_ID = db.Column(db.Integer)
    Categoria_ID = db.Column(db.String(100))
    P_Modelo = db.Column(db.String(100))
    P_ValorUnitario = db.Column(db.Float)
    P_nome = db.Column(db.String(100))
    P_Marca = db.Column(db.String(100))
    P_Imagem = db.Column(db.String(1000))

class Fornecedor(db.Model):
    Fornecedor_ID= db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
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

class Categoria(db.Model):
    Categoria_ID = db.Column(db.Integer, primary_key=True)
    C_Nome = db.Column(db.String(45))

class Cliente(db.Model):
    Cliente_ID = db.Column(db.Integer, primary_key=True)
    C_Primeiro_Nome = db.Column(db.String(45))
    C_Segundo_Nome = db.Column(db.String(45))
    C_Tipo_Documento = db.Column(db.String(45))
    C_Numero_Documento = db.Column(db.String(100))