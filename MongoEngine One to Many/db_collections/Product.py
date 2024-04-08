import datetime

from mongoengine import *

from db_collections import PriceHistory


class Product(Document):
    productCode = StringField(db_field='product_code', max_length=15, required=True)
    productName = StringField(db_field='product_name', max_length=70, required=True)
    productDescription = StringField(db_field='product_description', max_length=800, required=True)
    quantityInStock = IntField(db_field='quantity_in_stock', min_value=0, required=True)
    buyPrice = Decimal128Field(db_field='buy_price', min_value=0.01, required=True, precision=2)
    msrp = Decimal128Field(db_field='msrp', min_value=0.01, required=True, precision=2)
    priceHistory = EmbeddedDocumentListField(PriceHistory, db_field='price_history')
    orderItems = ListField(ReferenceField('OrderItem'))

    meta = {
        'collection': 'products',
        'indexes': [
            {'unique': True, 'fields': ['productCode'], 'name': 'products_uk_01'},
            {'unique': True, 'fields': ['productName'], 'name': 'products_uk_02'}
        ]
    }

    def change_price(self, new_price_history: PriceHistory):
        current_price_history: PriceHistory = self.priceHistory[-1]
        if float(current_price_history.newPrice) == float(new_price_history.newPrice):
            raise ValueError('It is already this price.')
        if current_price_history.priceChangeDate >= new_price_history.priceChangeDate:
            raise ValueError('New price change must be later than the latest price change.')
        if new_price_history.priceChangeDate > datetime.datetime.utcnow():
            raise ValueError('The price change cannot occur in the future.')
        self.priceHistory.append(new_price_history)
        self.buyPrice = new_price_history.newPrice

    def __init__(self, productCode, productName, productDescription, quantityInStock, buyPrice, msrp, *args, **values):
        super().__init__(*args, **values)
        if not self.orderItems:
            self.orderItems = []
        self.productCode = productCode
        self.productName = productName
        self.productDescription = productDescription
        self.quantityInStock = quantityInStock
        self.buyPrice = buyPrice
        self.msrp = msrp

    def __str__(self):
        return self.productName

    def add_item(self, item):
        for already_ordered_item in self.orderItems:
            if item.equals(already_ordered_item):
                return
        self.orderItems.append(item)

    def remove_item(self, item):
        for already_ordered_item in self.orderItems:
            if item.equals(already_ordered_item):
                self.orderItems.remove(already_ordered_item)
                break
