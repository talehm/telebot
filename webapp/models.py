from datetime import datetime, timedelta
from webapp.database import db
from webapp import enums
from sqlalchemy import CheckConstraint, Numeric
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from webapp import types
import json


class MyBaseModel(db.Model):
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    id = db.Column(db.Integer, primary_key=True)


# db = SQLAlchemy()
class Seller(MyBaseModel):
    __tablename__ = "account_seller"

    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    address = db.Column(db.String)
    chat_id = db.Column(db.Integer)
    platform = db.Column(db.Enum(enums.Platform), default=enums.Platform.AMAZON)
    country = db.Column(db.Enum(enums.Country), default=enums.Country.GERMANY)
    is_telegram_activated = db.Column(db.Boolean, default=False)
    is_blocked = db.Column(db.Boolean, default=False)
    performance_score = db.Column(db.Float)
    __table_args__ = (
        db.CheckConstraint("performance_score <= 100", name="check_performance_score"),
        db.CheckConstraint("email LIKE '%@%.%'", name="check_email_format"),
    )

    def __init__(
        self,
        first_name,
        last_name,
        email,
        address,
        chat_id,
        platform,
        country,
        is_telegram_activated,
        is_blocked,
        performance_score,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.address = address
        self.chat_id = chat_id
        self.platform = platform
        self.country = country
        self.is_telegram_activated = is_telegram_activated
        self.is_blocked = is_blocked
        self.performance_score = performance_score

    def __repr__(self):
        return "<id {}>".format(self.id)


class Product(MyBaseModel):
    __tablename__ = "product"

    description = db.Column(db.Text)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    count = db.Column(db.Integer)
    seller_id = db.Column(db.Integer, db.ForeignKey("account_seller.id"))
    url = db.Column(db.String, CheckConstraint(text("url ~ '^https?://.*$'")))
    image_url = db.Column(
        db.String, CheckConstraint(text("image_url ~ '^https?://.*$'"))
    )
    status = db.Column(
        db.Enum(enums.ProductStatus), default=enums.ProductStatus.AVAILABLE
    )
    properties = db.Column(db.JSON)
    seller = db.relationship("Seller", backref="products")

    def __init__(
        self, description, name, price, seller_id, url, image_url, status, properties
    ):
        self.url = url
        self.description = description
        self.name = name
        self.price = price
        self.seller_id = seller_id
        self.image_url = image_url
        self.status = status
        self.properties = properties.to_dict()

    def __repr__(self):
        return "<id {}>".format(self.id)

    def order(self):
        self.count -= 1
        if self.count == 0:
            self.status = enums.ProductStatus.SOLD_OUT
        return self


class Verification(MyBaseModel):
    __tablename__ = "account_verification"

    seller_id = db.Column(db.Integer, db.ForeignKey("account_seller.id"))
    verification_code = db.Column(db.Integer)
    hash_string = db.Column(db.String)
    expire_at = db.Column(
        db.DateTime, default=lambda: datetime.utcnow() + timedelta(minutes=5)
    )
    seller = db.relationship("Seller", backref="verifications")

    def __init__(self, seller_id, verification_code, hash_string, created_at, ttl):
        self.seller_id = seller_id
        self.verification_code = verification_code
        self.hash_string = hash_string
        self.created_at = created_at
        self.ttl = ttl

    def __repr__(self):
        return "<id {}>".format(self.id)


class Buyer(MyBaseModel):
    __tablename__ = "account_buyer"
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    username = db.Column(db.String)
    language_code = db.Column(db.String)
    chat_id = db.Column(db.BigInteger, unique=True)
    is_active = db.Column(db.Boolean, default=False)
    is_blocked = db.Column(db.Boolean, default=False)
    paypal = db.Column(db.String)
    amazon_url = db.Column(db.Text)
    amazon_screenshot = db.Column(db.Text)

    def __init__(
        self,
        first_name,
        last_name,
        username,
        language_code,
        chat_id,
        paypal,
        amazon_url,
        amazon_screenshot,
        is_active,
        is_blocked,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.chat_id = chat_id
        self.language_code = language_code
        self.is_active = is_active
        self.is_blocked = is_blocked
        self.paypal = paypal
        self.amazon_url = amazon_url
        self.amazon_screenshot = amazon_screenshot

    def __repr__(self):
        return "<username {}>".format(self.username)


class Message(MyBaseModel):
    __tablename__ = "telegram.buyer_message"

    message_id = db.Column(db.String)
    chat_id = db.Column(db.String)
    text = db.Column(db.Text)

    def __init__(self, message_id, chat_id, text, created_at):
        self.message_id = message_id
        self.chat_id = chat_id
        self.text = text
        self.created_at = created_at

    def __repr__(self):
        return "<message_id {}>: <text {}>".format(self.message_id, self.text)


class Order(MyBaseModel):
    __tablename__ = "order"

    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    buyer_id = db.Column(db.Integer, db.ForeignKey("account_buyer.id"))
    status = db.Column(
        db.Enum(enums.OrderStatus), default=enums.OrderStatus.WAITING_CONFIRMATION
    )
    review_screenshot = db.Column(db.Text, nullable=True)
    order_screenshot = db.Column(db.Text, nullable=True)
    order_number = db.Column(db.String, unique=True, nullable=True)
    buyer = db.relationship("Buyer", backref="orders")
    product = db.relationship("Product", backref="orders")

    def __init__(
        self,
        product_id,
        buyer_id,
        status,
        order_id=None,
        order_screenshot=None,
        review_screenshot=None,
    ):
        self.product_id = product_id
        self.buyer_id = buyer_id
        self.status = status
        self.review_screenshot = review_screenshot
        self.order_screenshot = order_screenshot
        self.order_id = order_id

    def __repr__(self):
        return "<id {}>".format(self.id)
