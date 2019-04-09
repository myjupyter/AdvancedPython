class Validator:
    
    _min_val = 0
    _max_val = 0 
    
    def __init__(self, min_val=0, max_val=0):
        _min_val = min_val
        _max_val = max_val
        
    @classmethod
    def validateMax(cls, value):
        if isinstance(value, int):
            return value if value <= cls._max_val else cls._max_val
        return cls._max_val
    
    @classmethod
    def validateMin(cls, value):
        if isinstance(value, int):
            return value if value >= cls._min_val else cls._min_val
        return cls._min_val
        
    
    
class IntValidator(Validator):
    
    _min_val = -2**31
    _max_val = 2**31 - 1
    
    def __init__(self, min_val=-2**31, max_val=2**31 - 1):
        super().__init__(min_val, max_val)
    
    
class CharValidator(Validator):
    
    _min_val = 1
    _max_val = 8000 
    
    def __init__(self, min_val=1, max_val=8000):
        super().__init__(min_val, max_val)
    
        
class FloatValidator(Validator):
    
    _min_val = -1.79e+308  
    _max_val = 1.79e+308
    
    def __init__(self, min_val=-1.79e+308, max_val=1.79e+308):
        super()._init_(min_val, max_val)
