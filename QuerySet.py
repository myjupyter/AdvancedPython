from db_connection import *

class QuerySet:
    
    def __new__(cls, **kwargs):
        return super().__new__(cls)
    
    def __init__(self, owner=None, query_set=None):
        if owner is None:
            raise AttributeError('Owner is None')
            
        self.cls = owner
        if query_set is None:
            self.query_set = list()
        else:
            self.query_set = query_set
    
    def create(self, **kwarg):
        return self.cls(**kwarg)
    
    def __len__(self):
        return len(self.query_set)
    
    def __getitem__(self, index):
        return self.query_set[index]
        
    def __setitem__(self, index, value):
        if isinstance(value, self.cls):
            self.query_set[index] = value
            return
        raise AttributeError("Value in not {0}".format(self.cls))
        
    def __delitem__(self, index):
        del self.query_set[index]
        
    def __iter__(self):
        return iter(self.query_set)

    def __reversed__(self):
        return Query_set(self.cls, reversed(self.query_set))
    
    def __str__(self):
        return str(self.query_set)
    
    def append(self, value):
        print(type(value))
        if isinstance(value, self.cls):
            self.query_set.append(value)
            return
        raise AttributeError("Value is not {0}".format(self.cls))
    
    def all(self):
        if len(self):
            return self
        
        connection = get_connection()
        table_name = self.cls.__dict__['Meta'].__dict__['table_name']
        sql_query = 'SELECT * FROM `%s`'
       
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql_query % (table_name))
                self.query_set += [self.cls(**line) for line in cursor.fetchall()]
        finally:
            connection.close()
            gc.collect()
            return self
        
    def __get_local(self, pk=None, **kwargs):
        pass
        
    def get(self, pk=None, **kwargs):
        #if len(self):
        #     return __get_local(self,**kwarg)
            
        table_name = self.cls.__dict__['Meta'].__dict__['table_name']
        sql_query = 'SELECT * FROM `%s` WHERE %s'
        
        if pk is None and not len(kwargs):
            return self
        
        connection = get_connection()
        if isinstance(pk, int) and pk > 0:
            try:
                with connection.cursor() as cursor:
                    name, value = self.cls()._get_primary_name_value()
                    cursor.execute(sql_query % (table_name, '%s=%s' % ('id', pk)))
                    self.query_set += [self.cls(**cursor.fetchone())]
            finally:
                connection.close()
                gc.collect()
                return self
                
        
        fields = self.cls.__dict__['Meta'].__dict__['fields']
        exemp = self.cls()
        where_list = ' AND '.join(
            [
                '%s=%s' % (field_name ,DBTypes.to_db_string(DBTypes.to_db_bool(field_value)))
                for field_name, field_value in kwargs.items() if hasattr(exemp, field_name)
            ]
        )
        print(where_list)
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql_query % (table_name, where_list))
                self.query_set += [self.cls(**line) for line in cursor.fetchall()]
        finally:
            connection.close()
            gc.collect()
            return self
          
        
        
    def delete(self, pk=None, **kwargs):
        
        table_name = self.cls.__dict__['Meta'].__dict__['table_name']
        sql_query = 'DELETE FROM `%s` WHERE %s'
    
        if pk is None and not len(kwargs):
            return 1
        
        connection = get_connection()
        if isinstance(pk, int) and pk > 0:
            try:
                with connection.cursor() as cursor:
                    name, value = self.cls()._get_primary_name_value()
                    cursor.execute(sql_query % (table_name, '%s=%s' % ('id', pk)))
            finally:
                connection.commit()
                connection.close()
                gc.collect()
                return 0
                        
        fields = self.cls.__dict__['Meta'].__dict__['fields']
        exemp = self.cls()
        where_list = ' AND '.join(
            [
                '%s=%s' % (field_name ,DBTypes.to_db_string(DBTypes.to_db_bool(field_value)))
                for field_name, field_value in kwargs.items() if hasattr(exemp, field_name)
            ]
        )
        print(where_list)
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql_query % (table_name, where_list))
        finally:
            connection.commit()
            connection.close()
            gc.collect()
            return self    
