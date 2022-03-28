from enum import unique
from management import db, login_manager
from management import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User1.query.get(int(user_id))

class User1(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    shipping_address = db.Column(db.String(length=100), nullable=False)
    mobile_number = db.Column(db.Numeric(),nullable=False)
    password_hash = db.Column(db.String(length=60), nullable=False)
  #  items = db.relationship('Consignmentdetails', backref='owned_user', lazy=True)
    


    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
class Cosignmentdetails(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    consignment_type=db.Column(db.String(length=20),nullable=False)
    receiver_name=db.Column(db.String(length=20),nullable=False)
    receiver_address=db.Column(db.String(length=50),nullable=False)
    receiver_mobile=db.Column(db.Integer(),nullable=False)
   # owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    def __repr__(self):
        return f'Consignmentdetails {self.receiver_name}'

    def buy(self, user):
        self.owner = user.id
        user.budget -= self.price