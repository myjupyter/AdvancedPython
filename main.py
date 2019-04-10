from Models import Model
from Fields import *
from db_connection import *

init_db('localhost', 'root', 'lumen23291633')

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
a.id = 0
a.save()
a = Stuff(Sex=False)
a.id = 1
a.save()
