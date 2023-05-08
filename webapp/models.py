from datetime import datetime, timedelta
from telebot.webapp.database import db
from telebot.webapp import enums
from sqlalchemy import CheckConstraint, Numeric
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from telebot.webapp import types
import json

class MyBaseModel(db.Model):
    __abstract__ = True

    # @classmethod
    # def query(cls, session=None):
    #     print("TEST")
    #     if session is None:
    #         session = db.session
    #     return session.query(cls)
        
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    id = db.Column(db.Integer, primary_key=True)

# db = SQLAlchemy()
class Seller(MyBaseModel):
    __tablename__ = 'account_seller'

    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, CheckConstraint("email ~* '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'"))
    address = db.Column(db.String)
    platform = db.Column(db.Enum(enums.Platform), default=enums.Platform.AMAZON)
    country = db.Column(db.Enum(enums.Country), default=enums.Country.GERMANY)
    is_telegram_activated = db.Column(db.Boolean, default=False)
    is_blocked = db.Column(db.Boolean, default=False)
    performance_score = db.Column(DOUBLE_PRECISION, CheckConstraint('performance_score <= 100'))

    def __init__(self, first_name, last_name, email, address, platform, country,created_at, is_telegram_activated, is_blocked, performance_score):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.address = address
        self.platform = platform
        self.country = country
        self.created_at = created_at
        self.is_telegram_activated = is_telegram_activated
        self.is_blocked = is_blocked
        self.performance_score = performance_score
    def __repr__(self):
        return '<id {}>'.format(self.id)

class Product(MyBaseModel):
    __tablename__ = 'product'

    description = db.Column(db.Text)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    seller_id = db.Column(db.Integer, db.ForeignKey('account_seller.id'))
    url = db.Column(db.String, CheckConstraint(text("url ~ '^https?://.*$'")))
    image_url = db.Column(db.String, CheckConstraint(text("image_url ~ '^https?://.*$'")))
    status = db.Column(db.Enum(enums.ProductStatus), default=enums.ProductStatus.AVAILABLE)
    properties = db.Column(db.JSON)
    seller = db.relationship('Seller', backref='products')

    def __init__(self, description, name, price, seller_id, url, image_url, status, properties):
        self.url = url
        self.description = description
        self.name = name
        self.price = price
        self.seller_id = seller_id
        self.image_url = image_url
        self.status = status
        self.properties = properties.to_dict()

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
class Verification(MyBaseModel):
    __tablename__ = 'account_verification'

    seller_id = db.Column(db.Integer, db.ForeignKey('account_seller.id'))
    verification_code = db.Column(db.Integer)
    hash_string = db.Column(db.String)
    expire_at = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(minutes=5))
    seller = db.relationship('Seller', backref='verifications')

    def __init__(self, seller_id, verification_code, hash_string, created_at, ttl):
        self.seller_id = seller_id
        self.verification_code = verification_code
        self.hash_string = hash_string
        self.created_at = created_at
        self.ttl = ttl
    
    def __repr__(self):
        return '<id {}>'.format(self.id)
    
class Buyer(MyBaseModel):
    __tablename__ = 'account_buyer'
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    username = db.Column(db.String)
    language_code = db.Column(db.String)
    chat_id = db.Column(db.Integer, unique=True)
    is_active = db.Column(db.Boolean, default=False)
    is_blocked = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, username, language_code, chat_id, is_active, is_blocked):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.chat_id = chat_id
        self.language_code = language_code
        self.is_active = is_active
        self.is_blocked = is_blocked

    def __repr__(self):
        return '<username {}>'.format(self.username)
    
class Message(MyBaseModel):
    __tablename__ = 'telegram.buyer_message'

    message_id = db.Column(db.String)
    chat_id = db.Column(db.String)
    text = db.Column(db.Text)

    def __init__(self, message_id, chat_id, text, created_at):
        self.message_id = message_id
        self.chat_id = chat_id
        self.text = text
        self.created_at = created_at

    def __repr__(self):
        return '<message_id {}>: <text {}>'.format(self.message_id, self.text)