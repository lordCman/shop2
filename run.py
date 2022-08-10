from app import app
from app.models import User, Post, db, Shopitems
from app.shop.forms import CreateShopItemForm

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Shopitems': Shopitems}

if __name__ == '__main__':
    app.run()