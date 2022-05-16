from flask import render_template
from . import bp as shop

@shop.route('/shop', methods = ['GET', 'POST'])
# @login_required
def shop():

    return render_template('shop.html.j2')