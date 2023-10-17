from shop import app, db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def user_loader(user_id):
    return Register.query.get(user_id)
    

class Register(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(10), unique=False, nullable=False)
    password = db.Column(db.String(100), unique=False, nullable=False)
    date_created = db.Column(db.Integer, nullable=False, default=int(datetime.utcnow().timestamp()))
    def __repr__(self):
        return "<Register %r>" % self.name
    
with app.app_context():
    db.create_all()
