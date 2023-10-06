from webapp import models, enums
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, URL



class ProductCreateForm(FlaskForm):
    seller_id = SelectField('Seller', coerce=int, validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired(), URL()])
    image_url = StringField('Image URL', validators=[DataRequired(), URL()])
    status = SelectField('Status', choices=[(s.value, s.name) for s in enums.ProductStatus])
    count = StringField('Count', validators=[DataRequired()])
    properties = StringField('Properties', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(ProductCreateForm, self).__init__(*args, **kwargs)
        self.seller_id.choices = [(seller.id, f'{seller.first_name}  {seller.last_name}') for seller in models.Seller.query.all()]
