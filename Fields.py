from Validators import IntValidator, CharValidator, FloatValidator        

class Field:
    
    def __init__(self, name='', cls=None, required=True, default=None, primary_key=False):
        self.name = '_' + name
        self.cls = cls
        self.required = required
        self.default = self.validate(default)
        self.primary_key = primary_key
        
    def __get__(self, instance, owner=None):
        if owner is None:
            return AttributeError('This field must be defined in a class!')
        return getattr(instance, self.name, self.default)
    
    def __set__(self, instance, value):
        instance.__dict__[self.name] = value
    
    def __delete__(self, instance):
        if instance is None:
            raise AttributeError()
        del instance.__dict__[self.name]
        
    def validate(self, value):
        if value is None and not self.required:
            return None
        return self.cls(value)
    
    def cls_validate(self, value):
        if not isinstance(value, self.cls):
            raise AttributeError('The value have to be {0}'.format(self.cls))
        return 
    
    @property
    def is_primary(self):
        return self.primary_key

    @property
    def is_required(self):
        return self.required
    
    @property
    def get_defaule(self):
        return self.default
        
class IntField(Field):
    
    def __init__(self, name='', min_value=None, max_value=None, **kwarg):
        self.min_value = IntValidator.validateMin(min_value)
        self.max_value = IntValidator.validateMax(max_value)
        super().__init__(name, int, **kwarg)
        
        
    def __get__(self, instance, owner=None):
        return super().__get__(instance, owner)
        
    def __set__(self, instance, value):
        super().cls_validate(value)
       
        if self.min_value > value or self.max_value < value:
            raise AttributeError(
                'Value have to lay between {0} and {1}'.format(
                    self.min_value,
                    self.max_value
                )
            )
        super().__set__(instance, value)

    def __delete__(self, instance):
        super().__delete__(instance)
        
        
class CharField(Field):
    
    def __init__(self, name='', max_length=None, min_length=None, **kwarg):
        self.min_length = CharValidator.validateMin(min_length)
        self.max_length = CharValidator.validateMax(max_length)
        super().__init__(name, str, **kwarg)
        
    def __get__(self, instance, owner=None):
        return super().__get__(instance, owner)
    
    def __set__(self, instance, value):
        super().cls_validate(value)
        
        if self.min_length > len(value) or self.max_length < len(value):
            raise AttributeError(
                'Value have to lay between {0} and {1}'.format(
                    self.min_length,
                    self.max_lenght
                )
            )
        super().__set__(instance, value)
        
    def __delete__(self, instance):
        super().__delete__(instance)
        
        
class BoolField(Field):
    
    def __init__(self, name='', **kwarg):
        super().__init__(name, bool, **kwarg)
        
    def __get__(self, instance, owner=None):
        return super().__get__(instance, owner)
    
    def __set__(self, instance, value):
        super().__set__(instance, value)
        
    def __delete__(self, instance):
        super().__delete__(instance)
        
        
class FloatField(Field):
    
    def __init__(self, name='', min_val=None, max_val=None, **kwarg):
        self.min_val = CharValidator.validateMin(min_val)
        self.max_val = CharValidator.validateMax(max_val)
        super().__init__(name, float, **kwarg)
        
    def __get__(self, instance, owner=None):
        return super().__get__(instance, owner)
    
    def __set__(self, instance, value):
        super().cls_validate(value)
        super().__set__(instance, value)
        
    def __delete__(self, instance):
        super().__delete__(instance)
        
        
class AutoField(IntField):
    
    def __init__(self, name='', **kwarg):
        kwarg['required'] = False
        if kwarg.get('default', None) is not None:
            raise AttributeError(
                'AutoField does not contain default value!'
            )
        super().__init__(name, min_value=0, max_value=2**31-1, **kwarg)
        
    def __get__(self, instance, owner=None):
        return super().__get__(instance, owner)
    
    def __set__(self, instance, value):
        super().cls_validate(value)
        super().__set__(instance, value)
    
    def __delete__(self, instance):
        super().__delete__(instance)
