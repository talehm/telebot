from flask_admin.contrib.sqla import ModelView
from telebot.webapp import models 
from flask_admin.form import Select2Widget
from telebot.admin import forms


class ProductView(ModelView):
    create_form = forms.ProductCreateForm
    column_list = ['id','seller','name', 'status', 'description',  'price',  'url', ]
    column_searchable_list = ('name',)
    form_widget_args = {
        'description': {'rows': 10},
        'url': {'style': 'width: 95%'},
        'image_url': {'style': 'width: 95%'},
        'seller_id': {'widget': Select2Widget()},
    }
    column_formatters = {
        'seller': lambda view, context, model, name: f'{model.seller.first_name} {model.seller.last_name}' if model.seller else ''
    }
    form_args = {
        'seller': {
            'label': 'Seller',
            'widget': Select2Widget(),
            'query_factory': lambda: models.Seller.query.all(),
            'get_pk': lambda a: a.id,
            'get_label': lambda a: f'{a.first_name} {a.last_name}'
        }
    }



    # admin.add_view(ModelView(Customer, db.session))
    # admin.add_view(ModelView(Order, db.session))