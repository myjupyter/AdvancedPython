class MetaManager(type):
    
    def __new__(mcs, name, bases, namespace):
        return super().__new__(mcs, name, bases, namespace)
    
class Manager(metaclass=MetaManager):
    
    def __get__(self, instance, owner=None):
        return QuerySet(owner=owner)
    
    def __delete__(self, instance):
        super().__delete__(instance)
        
