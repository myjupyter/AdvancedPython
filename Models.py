import inspect

from db_connection import *
from DBTypes import DBTypes
from Fields import * 
from QuerySet import QuerySet
from Manager import Manager

class MetaModel(type):
    
    def __new__(mcs, name, bases, namespace):
        super_new = super().__new__
        
        # To choose only bases class constructed by MetaModel
        parents = tuple([b for b in bases if isinstance(b, MetaModel)])
        if not parents:
            return super_new(mcs, name, bases, namespace)
        
        new_namespace = dict()
        module = namespace.pop('__module__', None)
        if module is not None:
            new_namespace['__module__'] = module
            
        classcell = namespace.pop('__classcell__', None)
        if classcell is not None:
            new_namespace['__classcell__'] = classcell

        new_class = super_new(mcs, name, parents, new_namespace)
        
        fields = {name: value for name, value in namespace.items() if isinstance(value, Field)}
        methods = {name: value for name, value in namespace.items() if inspect.isfunction(value)}
        
        fields_name = set(fields.keys())
        
        meta = namespace.pop('Meta', None)
        if meta is not None:
            if not hasattr(meta, 'table_name'):
                setattr(meta, 'table_name', name)
            # There shoulde change conditions
            if not hasattr(meta, 'fields'):
                setattr(meta, 'fields', fields_name)
        else:
            meta = type('Meta', tuple(), {'table_name' : name, 'fields' : fields_name})
        
        # To inherite the fields by MRO
        for base_cls in new_class.mro():
            for field_name, value in base_cls.__dict__.items():  
                if isinstance(value, Field):
                    fields.update({field_name: value})
                    continue
                if inspect.isfunction(value):
                    methods.update({field_name: value})
        
        
        fields = mcs._check_primary(fields)
        meta.fields.update(set(fields.keys()))
        
        fields.update(methods)
        fields.update(mcs._set_manager(namespace))

        
        # To add meta-data
        setattr(new_class, 'Meta', meta)
        
        # To set fields from base classes
        for attr_name, attr_value in fields.items():
            setattr(new_class, attr_name, attr_value)

        return new_class
    
    @classmethod
    def _check_primary(cls, namespace=None):
        if namespace is None:
            return None
        
        primary_dict = {name: value for name, value in namespace.items() if (value.is_primary and value.name != '_id')}
        if len(primary_dict) > 1:
            raise AttributeError(
                'Model has to have only one primary_key field'
            )
        elif len(primary_dict) == 1:
            namespace.pop('id')
            return namespace

        return namespace
    
    @classmethod
    def _set_manager(cls, namespace=None):
        if namespace is None:
            return None
        
        managers = {name: value for name, value in namespace.items() if isinstance(value, Manager)}
        if len(managers) == 0:
            managers.update({'objects': Manager()})
        if len(managers) > 1:
            raise AttributeError(
                'Table have to has only one Manager()'
            )
        return managers
            
        
class Model(metaclass=MetaModel):
    
    class Meta:
        table_name = 'Model'
        fields = {'id'}
    
    id = AutoField('id',primary_key=True)
    objects = Manager()
    
    def __init__(self, **kwargs):
        
        for attr_name, attr_value in kwargs.items():
            if attr_name in self.__class__.__dict__['Meta'].__dict__['fields']:
                setattr(self, attr_name, attr_value)
            
    def _get_primary_name_value(self):
        for name, value in self.__class__.__dict__.items():
            if isinstance(value, Field):
                if value.is_primary:
                    return name, getattr(self, name)
        raise RuntimeError('Model has no primary key!')
        
    def __update(self):
        connection = get_connection()
        table_name = self.__class__.__dict__['Meta'].__dict__['table_name']
        update_reuslt = 0
        
        try:
            with connection.cursor() as cursor:
                name, value = self._get_primary_name_value()
                if value is None:
                    raise RuntimeError('Primary key must be not None')
                if (cursor.execute('SELECT * FROM %s WHERE %s=%s' % (table_name, name, value))):
                    update_query = 'UPDATE {0} SET {1} WHERE {2}'
                    attr_list = [
                        str(attr_name) + '=' + str(DBTypes.to_db_string(DBTypes.to_db_bool(getattr(self, attr_name))))
                        for attr_name, attr_value in self.__class__.__dict__.items()
                        if isinstance(attr_value, Field) and not attr_value.is_primary
                    ]
                    attr_list = ','.join(attr_list)
                    update_query = update_query.format(
                        table_name,
                        attr_list,
                        '%s=%s' % (name, value)
                    )
                    cursor.execute(update_query)
                    connection.commit()
                    update_reuslt = 1
                    
        finally:
            connection.close()
            gc.collect()
            return update_reuslt
                         
                
    def save(self):
        connection = get_connection()
        table_name = self.__class__.__dict__['Meta'].__dict__['table_name']
        
        if self.__update():
            return
        
        try:
            with connection.cursor() as cursor:
                value_list = list()
                name_list = list()
                string_list = list()
                for field_name in self.__class__.__dict__['Meta'].__dict__['fields']:
                    value_list.append(getattr(self, field_name))
                    name_list.append(field_name)
                    string_list.append(
                        '`%s` %s %s %s' % (
                            field_name, 
                            DBTypes.get_db_type(self.__class__.__dict__[field_name]),
                            DBTypes.get_db_req(self.__class__.__dict__[field_name]),
                            DBTypes.get_db_prim(self.__class__.__dict__[field_name]),
                        )
                    )
                string_list = ','.join(string_list)
                cursor.execute(
                    'CREATE TABLE IF NOT EXISTS `%s` (%s)' % (
                        table_name,
                        string_list
                    )
                )
                value_list = [str(DBTypes.to_db_string(DBTypes.to_db_bool(e))) for e in value_list]
                value_list = ','.join(value_list)
                name_list = ','.join(name_list)
                query_insert = 'INSERT INTO %s (%s) VALUES (%s)' % (
                    table_name,
                    name_list,
                    value_list
                )
                cursor.execute(query_insert)
                connection.commit()
        finally:
            connection.close()
            gc.collect()
