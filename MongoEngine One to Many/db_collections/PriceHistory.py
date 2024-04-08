import datetime

from mongoengine import *


class PriceHistory(EmbeddedDocument):
    newPrice = Decimal128Field(db_field='new_price', required=True)
    priceChangeDate = DateTimeField(db_field='price_change_date', required=True)

    def __init__(self, newPrice, priceChangeDate: datetime, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.newPrice = newPrice
        self.priceChangeDate = priceChangeDate

    def __str__(self):
        return f'Price History Entry: New price: {self.newPrice}, on date: {self.priceChangeDate}'
