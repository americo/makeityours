from crypt import methods
from flask import (
    render_template,
    request,
    url_for,
    redirect,
    flash,
    Flask,
    Blueprint,
    send_from_directory,
)
from models import (
    Produto,
    Fornecedor,
    Categoria,
    Usuario,
    Carrinho,
    Pedido,
    Comentario,
)
from flask_login import login_required, current_user
from database import db
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

import os
import uuid


main = Blueprint("main", __name__)

ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif", "svg"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route("/")
def index():
    try:
        cat = request.args.get("category", "")
        categoria = Categoria.query.filter_by(C_Nome=cat).first()
    except:
        pass

    try:
        searchQuery = request.args.get("query", "")
    except:
        hasSearchQuery = False

    categories = Categoria.query.all()
    all_categories = []
    for category in categories:
        all_categories.append(category)

    products = Produto.query.all()
    all_products = []

    if cat:
        for product in products:
            cat1 = int(product.Categoria_ID)
            cat2 = int(categoria.Categoria_ID)
            if cat1 == cat2:
                all_products.append(product)
    else:
        if searchQuery:
            for product in products:
                if searchQuery in product.P_nome:
                    all_products.append(product)
                elif searchQuery in product.P_Modelo:
                    all_products.append(product)
                elif searchQuery in product.P_Marca:
                    all_products.append(product)
                else:
                    pass
            return render_template(
                "index.html",
                categories=all_categories,
                products=all_products,
                searchQuery=searchQuery,
                hasSearchQuery=True,
            )
        else:
            for product in products:
                all_products.append(product)

    return render_template(
        "index.html",
        categories=all_categories,
        products=all_products,
        searchQuery=searchQuery,
        hasSearchQuery=False,
    )


@main.route("/account", methods=["GET", "POST"])
@login_required
def account():
    if request.method == "GET":
        return render_template("account.html")
    else:
        fullname = request.form.get("fullname")
        cellphone = request.form.get("cellphone")
        address = request.form.get("address")
        email = request.form.get("email")

        print(fullname, cellphone, address, email)

        user = Usuario.query.filter_by(U_Email=current_user.U_Email).first()

        try:
            password = request.form.get("password")
            newpassword = request.form.get("newpassword")
        except:
            pass

        if email != current_user.U_Email:
            exist_user = Usuario.query.filter_by(U_Email=email).first()

        try:
            if exist_user:
                flash("Este email já está em uso!")
                return redirect(url_for("main.account"))
        except:
            pass

        if password and newpassword:
            if not user or not check_password_hash(user.U_Senha, password):
                flash("Senha incorrecta!")
                return redirect(url_for("main.account"))
            user.U_Senha = generate_password_hash(newpassword, method="sha256")

        user.U_Nome = fullname
        user.U_Email = email
        user.U_Endereco = address
        user.U_Celular = cellphone

        db.session.commit()

        return redirect(url_for("main.account"))


@main.route("/cart", methods=["GET", "POST", "DELETE"])
@login_required
def cart():
    if request.method == "GET":
        carts = Carrinho.query.filter_by(Usuario_ID=current_user.Usuario_ID)
        all_products = []
        all_carts = []
        total_to_pay = 0

        for cart in carts:
            all_carts.append(cart)
            total_to_pay += cart.Total_A_Pagar
            product = Produto.query.filter_by(Produto_ID=cart.Produto_ID).first()
            all_products.append(product)

        return render_template(
            "cart.html",
            products=all_products,
            carts=all_carts,
            total_to_pay=total_to_pay,
        )
    else:
        user_id = request.form.get("user_id")
        product_id = request.form.get("product_id")
        product_quantity = request.form.get("product_quantity")
        total_to_pay = request.form.get("total_to_pay")

        new_cart = Carrinho(
            Usuario_ID=user_id,
            Produto_ID=product_id,
            Quantidade=product_quantity,
            Total_A_Pagar=total_to_pay,
        )

        db.session.add(new_cart)
        db.session.commit()

        return redirect(url_for("main.cart"))


@main.route("/deleteCart")
@login_required
def deleteCart():
    cart_id = request.args.get("id", "")
    cart = Carrinho.query.filter_by(Cart_ID=cart_id).first()
    if cart:
        db.session.delete(cart)
        db.session.commit()

    return redirect(url_for("main.cart"))


@main.route("/orders", methods=["GET", "POST"])
@login_required
def orders():
    if request.method == "GET":
        orders = Pedido.query.filter_by(Usuario_ID=current_user.Usuario_ID)
        all_products = []
        all_orders = []

        for order in orders:
            all_orders.append(order)
            product = Produto.query.filter_by(Produto_ID=order.Produto_ID).first()
            all_products.append(product)

        print(all_products)
        return render_template("orders.html", orders=all_orders, products=all_products)
    else:
        carts = Carrinho.query.filter_by(Usuario_ID=current_user.Usuario_ID)
        for cart in carts:
            new_order = Pedido(
                Usuario_ID=current_user.Usuario_ID,
                Produto_ID=cart.Produto_ID,
                Quantidade=cart.Quantidade,
                Total_A_Pagar=cart.Total_A_Pagar,
            )
            db.session.add(new_order)
            db.session.delete(cart)

        db.session.commit()

        return redirect(url_for("main.orders"))


@main.route("/admin")
@login_required
def admin():
    categories = Categoria.query.all()
    all_categories = []
    for category in categories:
        all_categories.append(category)
    return render_template("admin.html", categories=all_categories)


# PRODUCT
@main.route("/product")
def product():
    product_id = request.args.get("id", "")
    product = Produto.query.filter_by(Produto_ID=product_id).first()

    categories = Categoria.query.all()
    all_categories = []
    for category in categories:
        all_categories.append(category)

    comments = Comentario.query.filter_by(Produto_ID=product_id)
    all_comments = []
    for comment in comments:
        all_comments.append(comment)

    users = Usuario.query.all()
    all_users = []
    for user1 in users:
        all_users.append(user1)

    return render_template(
        "product.html",
        product=product,
        categories=all_categories,
        comments=all_comments,
        users=users,
    )


@main.route("/addComment", methods=["POST"])
def addComment():
    product_id = request.form.get("product_id")
    comment = request.form.get("comment")

    new_comment = Comentario(
        Usuario_ID=current_user.Usuario_ID,
        Produto_ID=product_id,
        C_Mensagem=comment,
    )

    db.session.add(new_comment)
    db.session.commit()

    return redirect(url_for("main.product", id=product_id))


@main.route("/deleteComment", methods=["GET"])
def deleteComment():
    comment_id = request.args.get("id", "")
    product_id = request.args.get("product_id", "")

    comment = Comentario.query.filter_by(Comment_ID=comment_id).first()
    if comment:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for("main.product", id=product_id))


@main.route("/admin/products")
def products():
    categories = Categoria.query.all()
    all_categories = []
    for category in categories:
        all_categories.append(category)

    products = Produto.query.all()
    all_products = []
    for product in products:
        all_products.append(product)
    return render_template(
        "products.html", categories=all_categories, products=all_products
    )


@main.route("/admin/addProduct", methods=["POST", "GET"])
def addProduct():
    if request.method == "GET":
        providers = Fornecedor.query.all()
        all_providers = []
        for provider in providers:
            all_providers.append(provider)

        categories = Categoria.query.all()
        all_categories = []
        for category in categories:
            all_categories.append(category)

        return render_template(
            "addProduct.html", providers=all_providers, categories=all_categories
        )
    else:
        product_name = request.form.get("product_name")
        provider_name = request.form.get("provider_name")
        category_name = request.form.get("category_name")
        product_brand = request.form.get("product_brand")
        product_model = request.form.get("product_model")
        product_price = request.form.get("product_price")
        print(product_name)

        provider = Fornecedor.query.filter_by(F_Primeiro_Nome=provider_name).first()
        category = Categoria.query.filter_by(C_Nome=category_name).first()

        if "file" not in request.files:
            print("ERRO")
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            ext = filename.split(".")[-1]
            filename = "%s.%s" % (uuid.uuid4(), ext)
            print(filename)
            file.save(os.path.join("./uploads/products", filename))

        new_product = Produto(
            Fornecedor_ID=provider.Fornecedor_ID,
            Categoria_ID=category.Categoria_ID,
            P_Modelo=product_model,
            P_ValorUnitario=product_price,
            P_nome=product_name,
            P_Marca=product_brand,
            P_Imagem=filename,
        )

        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for("main.products"))


@main.route("/admin/editProduct", methods=["GET", "POST"])
def editProduct():
    if request.method == "GET":
        product_id = request.args.get("id", "")
        product = Produto.query.filter_by(Produto_ID=product_id).first()

        providers = Fornecedor.query.all()
        all_providers = []
        for provider in providers:
            all_providers.append(provider)

        categories = Categoria.query.all()
        all_categories = []
        for category in categories:
            all_categories.append(category)

        return render_template(
            "editProduct.html",
            product=product,
            providers=all_providers,
            categories=all_categories,
        )
    else:
        product_id = request.form.get("product_id")
        product_name = request.form.get("product_name")
        provider_name = request.form.get("provider_name")
        category_name = request.form.get("category_name")
        product_brand = request.form.get("product_brand")
        product_model = request.form.get("product_model")
        product_price = request.form.get("product_price")
        print(product_name)

        provider = Fornecedor.query.filter_by(F_Primeiro_Nome=provider_name).first()
        category = Categoria.query.filter_by(C_Nome=category_name).first()

        if "file" not in request.files:
            print("ERRO")
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            ext = filename.split(".")[-1]
            filename = "%s.%s" % (uuid.uuid4(), ext)
            print(filename)
            file.save(os.path.join("./uploads/products", filename))

        product = Produto.query.filter_by(Produto_ID=product_id).first()

        os.remove(f"./uploads/products/{product.P_Imagem}")
        product.Fornecedor_ID = provider.Fornecedor_ID
        product.Categoria_ID = category.Categoria_ID
        product.P_Modelo = product_model
        product.P_ValorUnitario = product_price
        product.P_nome = product_name
        product.P_Marca = product_brand
        product.P_Imagem = filename

        db.session.commit()

        return redirect(url_for("main.products"))


@main.route("/admin/deleteProduct")
def deleteProduct():
    product_id = request.args.get("id", "")
    product = Produto.query.filter_by(Produto_ID=product_id).first()
    if product:
        os.remove(f"./uploads/products/{product.P_Imagem}")
        db.session.delete(product)
        db.session.commit()

    return redirect(url_for("main.products"))


# PROVIDER
@main.route("/admin/providers")
def providers():
    categories = Categoria.query.all()
    all_categories = []
    for category in categories:
        all_categories.append(category)

    providers = Fornecedor.query.all()
    all_providers = []
    for provider in providers:
        all_providers.append(provider)
    return render_template(
        "providers.html", categories=all_categories, providers=all_providers
    )


@main.route("/admin/addProvider", methods=["GET"])
def addProvider():
    categories = Categoria.query.all()
    all_categories = []
    for category in categories:
        all_categories.append(category)
    return render_template("addProvider.html", categories=all_categories)


@main.route("/admin/addProvider", methods=["POST"])
def addProviderPost():
    provider_name = request.form.get("provider_name")
    provider_second_name = request.form.get("provider_second_name")
    provider_document_number = request.form.get("provider_document_number")
    provider_document_type = request.form.get("provider_document_type")
    provider_cellphone1 = request.form.get("provider_cellphone1")
    provider_cellphone2 = request.form.get("provider_cellphone2")
    provider_email = request.form.get("provider_email")
    provider_province = request.form.get("provider_province")
    provider_city = request.form.get("provider_city")
    provider_quart = request.form.get("provider_quart")
    provider_district = request.form.get("provider_district")
    provider_street = request.form.get("provider_street")

    new_provider = Fornecedor(
        F_Primeiro_Nome=provider_name,
        F_Segundo_Nome=provider_second_name,
        F_Num_Documento=provider_document_number,
        F_Tipo_Documento=provider_document_type,
        F_Telefone_1=provider_cellphone1,
        F_Telefone_2=provider_cellphone2,
        F_Email=provider_email,
        F_Provincia=provider_province,
        F_Distrito=provider_city,
        F_Quarteirao=provider_quart,
        F_Bairro=provider_district,
        F_Rua=provider_street,
    )

    db.session.add(new_provider)
    db.session.commit()

    return redirect(url_for("main.providers"))


@main.route("/admin/editProvider", methods=["GET", "POST"])
def editProvider():
    if request.method == "GET":
        provider_id = request.args.get("id", "")
        provider = Fornecedor.query.filter_by(Fornecedor_ID=provider_id).first()

        categories = Categoria.query.all()
        all_categories = []
        for category in categories:
            all_categories.append(category)

        return render_template(
            "editProvider.html", provider=provider, categories=all_categories
        )
    else:
        provider_id = request.form.get("provider_id")
        provider_name = request.form.get("provider_name")
        provider_second_name = request.form.get("provider_second_name")
        provider_document_number = request.form.get("provider_document_number")
        provider_document_type = request.form.get("provider_document_type")
        provider_cellphone1 = request.form.get("provider_cellphone1")
        provider_cellphone2 = request.form.get("provider_cellphone2")
        provider_email = request.form.get("provider_email")
        provider_province = request.form.get("provider_province")
        provider_city = request.form.get("provider_city")
        provider_quart = request.form.get("provider_quart")
        provider_district = request.form.get("provider_district")
        provider_street = request.form.get("provider_street")

        provider = Fornecedor.query.filter_by(Fornecedor_ID=provider_id).first()

        provider.F_Primeiro_Nome = provider_name
        provider.F_Segundo_Nome = provider_second_name
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

        return redirect(url_for("main.providers"))


@main.route("/admin/deleteProvider")
def deleteProvider():
    provider_id = request.args.get("id", "")
    provider = Fornecedor.query.filter_by(Fornecedor_ID=provider_id).first()
    if provider:
        db.session.delete(provider)
        db.session.commit()

    return redirect(url_for("main.providers"))


# CATEGORY
@main.route("/admin/categories")
def categories():
    categories = Categoria.query.all()
    all_categories = []
    for category in categories:
        all_categories.append(category)

    return render_template("categories.html", categories=all_categories)


@main.route("/admin/addCategory", methods=["GET", "POST"])
def addCategory():
    if request.method == "GET":
        categories = Categoria.query.all()
        all_categories = []
        for category in categories:
            all_categories.append(category)
        return render_template("addCategory.html", categories=all_categories)
    else:
        category_name = request.form.get("category_name")

        new_category = Categoria(C_Nome=category_name)

        db.session.add(new_category)
        db.session.commit()

        return redirect(url_for("main.categories"))


@main.route("/admin/editCategory", methods=["GET", "POST"])
def editCategory():
    if request.method == "GET":
        category_id = request.args.get("id", "")
        category = Categoria.query.filter_by(Categoria_ID=category_id).first()

        categories = Categoria.query.all()
        all_categories = []
        for category in categories:
            all_categories.append(category)

        return render_template(
            "editCategory.html", category=category, categories=all_categories
        )
    else:
        category_id = request.form.get("category_id")
        category_name = request.form.get("category_name")

        category = Categoria.query.filter_by(Categoria_ID=category_id).first()

        category.C_Nome = category_name

        db.session.commit()

        return redirect(url_for("main.categories"))


@main.route("/admin/deleteCategory")
def deleteCategory():
    category_id = request.args.get("id", "")
    category = Categoria.query.filter_by(Categoria_ID=category_id).first()
    if category:
        db.session.delete(category)
        db.session.commit()

    return redirect(url_for("main.categories"))


@main.route("/uploads/products/<filename>")
def load_image(filename):
    return (
        send_from_directory("./uploads/products", filename),
        200,
        {"Content-Type": "image/jpeg; charset=utf-8"},
    )
