
from flask import Blueprint, render_template, request, redirect, url_for, flash

#import login funcitonality
from flask_login import login_required, current_user


# import models
from app.models import Shopitems

shop = Blueprint('shop', __name__, template_folder='shoptemplates')

@shop.route('/shop')
@login_required
def getShop():
    p_set = set()
    item = Shopitems.query.all()
    print(item)
    x = current_user.carts.all()
    for ite in item:
        if ite in x:
            flag =True
        else:
            flag =False


    return render_template('shop.html', item =item, flag = flag)

@shop.route('/cart')
@login_required
def showCart():
    items = current_user.carts.all()
    total = len(items)
    x = []
    for i in items:
        x.append(i.price)
    for i in range(0, len(x)):
        x[i] = int(float(x[i]))
    print(x)
    prices = sum(x)
    return render_template('cart.html', items = items, total=total, prices =prices)

@shop.route('/addToCart/<item>')
@login_required
def addItem(item):
    item = Shopitems.query.filter_by(item = item).first()
   
    if item not in current_user.carts.all():
        current_user.addToCart(item)
    return redirect(url_for('shop.showCart'))

@shop.route('/removeFromCart/<item_id>')
@login_required
def removeItem(item_id):
    item = Shopitems.query.filter_by(id = item_id).first()
    current_user.removeFromCart(item)
    return redirect(url_for('shop.showCart'))

@shop.route('/removeAll')
@login_required
def remAll():
    items = Shopitems.query.all()

    for i in items:
        if i in current_user.carts:
            current_user.removeFromCart(i)
        else:
            pass
    return redirect(url_for('shop.getShop'))


@shop.route('/checkout')
@login_required
def checkout():
    items = current_user.carts.all()
    flag=False
    if len(items) < 0:
        flash('You have nothing in your cart')
    else:
        flag=True
    return redirect(url_for('shop.showCart', flag=flag))

