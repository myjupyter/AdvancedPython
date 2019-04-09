from Models import Model
from Fields import *

class User(Model):
    
    TelNumber = IntField('TelNumber',required=True, default=2)
    Name =      CharField('Name',required=True, default='fdf')
    Sex =       BoolField('Sex',required=True, default=True)
    Money  =    FloatField('Money',required=False, default=0.0)
    
    def __init__(self, **kwarg):
        super().__init__(**kwarg)
    
    def update_money(self, value):
        self.Money = value
        
    

class Stuff(User):
    Post = IntField(required=True, default = -1)

a = Stuff()

a.save()
