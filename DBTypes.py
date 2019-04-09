from Fields import *

class DBTypes:
    
    __types = {
            IntField: 'INT(10)', 
            FloatField: 'FLOAT(53,8)',
            CharField: 'CHAR(255)',
            BoolField: 'BOOLEAN',
            AutoField: 'INT(10)'
    }
    
    __requirement = {False: '', True: 'NOT NULL', None: ''}
    __primary_key = {False: '', True: 'PRIMARY KEY', None: ''}
    
    @classmethod
    def get_db_type(cls, value):
        if isinstance(value, Field):
            return cls.__types[type(value)]
        
    @classmethod
    def get_db_req(cls, value):
        if isinstance(value, Field):
            return cls.__requirement[value.is_required]
        
    @classmethod
    def get_db_prim(cls, value):
        if isinstance(value, Field):
            return cls.__primary_key[value.is_primary]
        
    @classmethod
    def to_db_bool(cls, value):
        if isinstance(value, bool):
            return int(value)
        return value
    
    @classmethod
    def to_db_string(cls, value):
        if isinstance(value, str):
            return '"' + value + '"'
        return value
