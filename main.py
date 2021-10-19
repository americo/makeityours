from flask import render_template, request, url_for, redirect, flash, Flask, Blueprint, send_from_directory
from .models import Produto, Fornecedor, Categoria, Cliente
from .app import db
from werkzeug.utils import secure_filename

import os
import uuid

main = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'svg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/')
def index():
    categories = Categoria.query.all()
    all_categories = []
    for category in categories:
        all_categories.append(category)

    products = Produto.query.all()
    all_products = []
    for product in products:
        all_products.append(product)
    return render_template('index.html', categories=all_categories, products=all_products)

@main.route('/admin')
def admin():
    categories = Categoria.query.all()
    all_categories = []
    for category in categories:
        all_categories.append(category)
    return render_template('admin.html', categories=all_categories)

# PRODUCT
@main.route('/product')
def product():
    product_id = request.args.get('id', '')
    product = Produto.query.filter_by(Produto_ID=product_id).first()

    categories = Categoria.query.all()
    all_categories = []
    for category in categories:
        all_categories.append(category)
    return render_template('product.html', product=product, categories=all_categories)

@main.route('/admin/products')
def products():
    categories = Categoria.query.all()
    all_categories = []
    for category in categories:
        all_categories.append(category)

    products = Produto.query.all()
    all_products = []
    for product in products:
        all_products.append(product)
    return render_template('products.html', categories=all_categories, products=all_products)

@main.route('/admin/addProduct', methods=['POST', 'GET'])
def addProduct():
    if request.method == 'GET':
        providers = Fornecedor.query.all()
        all_providers = []
        for provider in providers:
            all_providers.append(provider)

        categories = Categoria.query.all()
        all_categories = []
        for category in categories:
            all_categories.append(category)

        return render_template('addProduct.html', providers=all_providers, categories=all_categories)
    else:
        product_name = request.form.get('product_name')
        provider_name = request.form.get('provider_name')
        category_name = request.form.get('category_name')
        product_brand = request.form.get('product_brand')
        product_model = request.form.get('product_model')
        product_price = request.form.get('product_price')
        print(product_name)

        provider = Fornecedor.query.filter_by(F_Primeiro_Nome=provider_name).first()
        category = Categoria.query.filter_by(C_Nome=category_name).first()

        if 'file' not in request.files:
                print("ERRO")
                flash('No file part')
                return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
        if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                ext = filename.split('.')[-1]
                filename = "%s.%s" % (uuid.uuid4(), ext)
                print(filename)
                file.save(os.path.join('./uploads/products', filename))

        new_product = Produto(Fornecedor_ID=provider.Fornecedor_ID, Categoria_ID=category.Categoria_ID, P_Modelo=product_model,
        P_ValorUnitario=product_price, P_nome=product_name, P_Marca=product_brand, P_Imagem=filename)

        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('main.products'))

@main.route('/admin/editProduct', methods=['GET', 'POST'])
def editProduct():
    if request.method == 'GET':
        product_id = request.args.get('id', '')
        product = Produto.query.filter_by(Produto_ID=product_id).first()

        providers = Fornecedor.query.all()
        all_providers = []
        for provider in providers:
            all_providers.append(provider)

        categories = Categoria.query.all()
        all_categories = []
        for category in categories:
            all_categories.append(category)

        return render_template('editProduct.html', product=product, providers=all_providers ,categories=all_categories)
    else:
        product_id = request.form.get('product_id')
        product_name = request.form.get('product_name')
        provider_name = request.form.get('provider_name')
        category_name = request.form.get('category_name')
        product_brand = request.form.get('product_brand')
        product_model = request.form.get('product_model')
        product_price = request.form.get('product_price')
        print(product_name)

        provider = Fornecedor.query.filter_by(F_Primeiro_Nome=provider_name).first()
        category = Categoria.query.filter_by(C_Nome=category_name).first()

        if 'file' not in request.files:
                print("ERRO")
                flash('No file part')
                return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
        if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                ext = filename.split('.')[-1]
                filename = "%s.%s" % (uuid.uuid4(), ext)
                print(filename)
                file.save(os.path.join('./uploads/products', filename))

        product = Produto.query.filter_by(Produto_ID=product_id).first()

        os.remove(f'./uploads/products/{product.P_Imagem}')
        product.Fornecedor_ID = provider.Fornecedor_ID
        product.Categoria_ID = category.Categoria_ID
        product.P_Modelo = product_model
        product.P_ValorUnitario = product_price
        product.P_nome = product_name
        product.P_Marca = product_brand
        product.P_Imagem = filename

        db.session.commit()

        return redirect(url_for('main.products'))


@main.route('/admin/deleteProduct')
def deleteProduct():
    product_id = request.args.get('id', '')
    product = Produto.query.filter_by(Produto_ID=product_id).first()
    if product:
        os.remove(f'./uploads/products/{product.P_Imagem}')
        db.session.delete(product)
        db.session.commit()

    return redirect(url_for('main.products'))

# PROVIDER
@main.route('/admin/providers')
def providers():
    categories = Categoria.query.all()
    all_categories = []
    for category in categories:
        all_categories.append(category)

    providers = Fornecedor.query.all()
    all_providers = []
    for provider in providers:
        all_providers.append(provider)
    return render_template('providers.html', categories=all_categories, providers=all_providers)

@main.route('/admin/addProvider', methods=['GET'])
def addProvider():
    categories = Categoria.query.all()
    all_categories = []
    for category in categories:
        all_categories.append(category)
    return render_template('addProvider.html', categories=all_categories)

@main.route('/admin/addProvider', methods=['POST'])
def addProviderPost():
    provider_name = request.form.get('provider_name')
    provider_second_name = request.form.get('provider_second_name')
    provider_document_number = request.form.get('provider_document_number')
    provider_document_type = request.form.get('provider_document_type')
    provider_cellphone1 = request.form.get('provider_cellphone1')
    provider_cellphone2 = request.form.get('provider_cellphone2')
    provider_email = request.form.get('provider_email')
    provider_province = request.form.get('provider_province')
    provider_city = request.form.get('provider_city')
    provider_quart = request.form.get('provider_quart')
    provider_district = request.form.get('provider_district')
    provider_street = request.form.get('provider_street')

    new_provider = Fornecedor(F_Primeiro_Nome=provider_name, F_Segundo_Nome=provider_second_name, 
    F_Num_Documento=provider_document_number, F_Tipo_Documento=provider_document_type,
     F_Telefone_1=provider_cellphone1, F_Telefone_2=provider_cellphone2, F_Email=provider_email, 
     F_Provincia=provider_province, F_Distrito=provider_city, F_Quarteirao=provider_quart,
      F_Bairro=provider_district, F_Rua=provider_street)

    db.session.add(new_provider)
    db.session.commit()

    return "</h3>Adicionado com sucesso</h3>"
    return redirect(url_for('main.providers'))

@main.route('/admin/editProvider', methods=['GET', 'POST'])
def editProvider():
    if request.method == 'GET':
        provider_id = request.args.get('id', '')
        provider = Fornecedor.query.filter_by(Fornecedor_ID=provider_id).first()

        categories = Categoria.query.all()
        all_categories = []
        for category in categories:
            all_categories.append(category)

        return render_template('editProvider.html', provider=provider, categories=all_categories)
    else:
        provider_id = request.form.get('provider_id')
        provider_name = request.form.get('provider_name')
        provider_second_name = request.form.get('provider_second_name')
        provider_document_number = request.form.get('provider_document_number')
        provider_document_type = request.form.get('provider_document_type')
        provider_cellphone1 = request.form.get('provider_cellphone1')
        provider_cellphone2 = request.form.get('provider_cellphone2')
        provider_email = request.form.get('provider_email')
        provider_province = request.form.get('provider_province')
        provider_city = request.form.get('provider_city')
        provider_quart = request.form.get('provider_quart')
        provider_district = request.form.get('provider_district')
        provider_street = request.form.get('provider_street')

        provider = Fornecedor.query.filter_by(Fornecedor_ID=provider_id).first()

        provider.F_Primeiro_Nome = provider_name
        provider.F_Segundo_Nome =  provider_second_name
        provider.F_Num_Documento = provider_document_number
        provider.F_Tipo_Documento = provider_document_type
        provider.F_Telefone_1 = provider_cellphone1
        provider.F_Telefone_2 = provider_cellphone2
        provider.F_Email = provider_email
        provider.F_Provincia = provider_province
        provider.F_Distrito = provider_city
        provider.F_Quarteirao = provider_quart
        provider.F_Bairro = provider_district
        provider.F_Rua = provider_street

        db.session.commit()

        return redirect(url_for('main.providers'))


@main.route('/admin/deleteProvider')
def deleteProvider():
    provider_id = request.args.get('id', '')
    provider = Fornecedor.query.filter_by(Fornecedor_ID=provider_id).first()
    if provider:
        db.session.delete(provider)
        db.session.commit()

    return redirect(url_for('main.providers'))


# CATEGORY
@main.route('/admin/categories')
def categories():
    categories = Categoria.query.all()
    all_categories = []
    for category in categories:
        all_categories.append(category)

    return render_template('categories.html', categories=all_categories)

@main.route('/admin/addCategory', methods=['GET', 'POST'])
def addCategory():
    if request.method == 'GET':
        categories = Categoria.query.all()
        all_categories = []
        for category in categories:
            all_categories.append(category)
        return render_template('addCategory.html', categories=all_categories)
    else:
        category_name = request.form.get('category_name')

        new_category = Categoria(C_Nome=category_name)

        db.session.add(new_category)
        db.session.commit()

        return redirect(url_for('main.categories'))

@main.route('/admin/editCategory', methods=['GET', 'POST'])
def editCategory():
    if request.method == 'GET':
        category_id = request.args.get('id', '')
        category = Categoria.query.filter_by(Categoria_ID=category_id).first()

        categories = Categoria.query.all()
        all_categories = []
        for category in categories:
            all_categories.append(category)

        return render_template('editCategory.html', category=category, categories=all_categories)
    else:
        category_id = request.form.get('category_id')
        category_name = request.form.get('category_name')

        category = Categoria.query.filter_by(Categoria_ID=category_id).first()

        category.C_Nome = category_name

        db.session.commit()

        return redirect(url_for('main.categories'))

@main.route('/admin/deleteCategory')
def deleteCategory():
    category_id = request.args.get('id', '')
    category = Categoria.query.filter_by(Categoria_ID=category_id).first()
    if category:
        db.session.delete(category)
        db.session.commit()

    return redirect(url_for('main.categories'))

# CLIENT
@main.route('/addClient', methods=['POST'])
def addClientPost():
    first_name = request.form.get('first_name')
    second_name = request.form.get('second_name')
    document_type = request.form.get('document_type')
    document_number = request.form.get('document_number')

    new_client = Cliente(C_Primeiro_Nome=first_name, C_Segundo_Nome=second_name, C_Tipo_Documento=document_type, C_Numero_Documento=document_number)

    db.session.add(new_client)
    db.session.commit()
    
    return "<script>alert('Compra concluída, o produto será entrege em 24 horas.')</script>"

@main.route('/uploads/products/<filename>')
def load_image(filename):
    return send_from_directory('./uploads/products', filename), 200, {'Content-Type': 'image/jpeg; charset=utf-8'}