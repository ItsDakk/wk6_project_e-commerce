from flask import render_template, redirect, url_for, flash, request
from app.models import Product
from . import bp as shop

@shop.route('/shop', methods = ['GET', 'POST'])
# @login_required
def shop():
    products=Product.query.all()

    return render_template('shop.html.j2', products = products)

    