from typing import List, Tuple
from telebot.webapp.enums import ServiceType

class BaseType:
    def to_dict(self):
        result = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                print(type(self))
                if isinstance(value, BaseType):
                    print(value, type)
                    result[key] = value.to_dict()
                else:
                    result[key] = value
        return result
    
class ProductPropertiesRefund(BaseType):
    def __init__(self, isFullRefund: bool, amount:float):
        self.isFullRefund = isFullRefund
        self.amount = amount

class ProductPropertiesPaypal(BaseType):
    def __init__(self, isPaypalFeeIncluded: bool, amount:float):
        self.isPaypalFeeIncluded = isPaypalFeeIncluded
        self.amount = amount

class ProductProperties(BaseType):
    def __init__(self, refund: ProductPropertiesRefund, paypal: ProductPropertiesPaypal, service_type: ServiceType):
        self.refund = refund
        self.paypal = paypal
        self.service_type = service_type


