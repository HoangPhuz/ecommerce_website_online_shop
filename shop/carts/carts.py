from flask import redirect, render_template, url_for, flash, request, session, current_app
from shop import app, db
from shop.products.models import Addproducts
from shop.products.routes import brands, categories

def MagerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False

@app.route('/addcart', methods=["POST"])
def AddCart():
    try:
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('Quantity'))
        colors = request.form.get('colors')
        product = Addproducts.query.filter_by(id=product_id).first()
        if request.method == "POST":
            DictItems = {product_id:{'name': product.name, 'price':float(product.price), 'discount':product.discount, 
                                    'color':colors, 'quantity':quantity, 'image':product.image_1, 'colors':product.colors}}
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    for key, item in session['Shoppingcart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            item['quantity'] += 1
                    
                else:
                    session['Shoppingcart'] =  MagerDicts(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)
            else: 
                session['Shoppingcart'] =  DictItems
                return redirect(request.referrer) 
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)
        
        
@app.route('/carts')
def getCart():
    if 'Shoppingcart' not in session and len(session['Shoppingcart']) <= 0: 
        return redirect(url_for('home'))
    subtotal = 0
    grandtotal = 0
    for key, product in session['Shoppingcart'].items():
        discount = (product['discount']/100)*float(product['price'])* int(product['quantity'])
        subtotal += float(product['price']) * int(product['quantity'])
        subtotal -= discount
        grandtotal = float("%.2f" % (subtotal))
    return render_template('products/carts.html', grandtotal=grandtotal, brands=brands(), categories=categories())


@app.route('/updatecart/<int:code>', methods=["POST"])
def updatecart(code):
    if 'Shoppingcart' not in session and len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    if request.method == "POST":
        quantity = request.form.get('quantity')
        color = request.form.get('color')
        try:
            session.modified = True
            for key, item in session['Shoppingcart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    item['color'] = color
                    flash('Item is updated', 'success')
                    return redirect(url_for('getCart'))
        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))
    

@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'Shoppingcart' not in session and len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                return redirect(url_for('getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))
        
        
@app.route('/clearcart')
def clearcart():
    try:
        session.clear()
        session.pop('Shoppingcart', None)
        return redirect(url_for('home'))
    except Exception as e:
        print(e)
        