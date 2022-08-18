import re, traceback, keyword

# Submitter: katyh1(Huang, Katy)
# Partner  : jessieh9(He, Jessie)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming
def pnamedtuple(type_name, field_names, mutable = False,  defaults = {}):
    def show_listing(s):
        for line_number, line_text in enumerate(s.split('\n'),1):           
            print(f' {line_number: >3} {line_text.rstrip()}')
    pattern = r'^[a-zA-Z]\w*$'
    field_pattern = r"^\[?(['a-zA-Z][\d_]*[\W]*?)*\]?$"
    if re.match(pattern, str(type_name)) == None or str(type_name) in keyword.kwlist:
        raise SyntaxError(f'{type_name} is not a legal name or already exists as a keyword')
    if re.match(field_pattern, str(field_names))==None or any(k in str(field_names) for k in keyword.kwlist):
        raise SyntaxError(f'An element of {field_names} is not a legal field name.')
    # put your code here
    # bind class_definition (used below) to the string constructed for the class
    def delete_dup(field):
        passed = set()
        for i in field:
            if i not in passed:
                passed.add(i)
                yield i

    if type(field_names)==str:
        if ',' in field_names:
            fields = list(delete_dup(field_names.replace(',',' ').split()))
        else:
            fields = list(delete_dup(field_names.split()))
    elif type(field_names)==list:
        fields = field_names
        

    if len(defaults)>0:
        for k in defaults:
            if k not in fields:
                raise SyntaxError('Key is not in the field names')
    def init_str(fields,defaults):
        rstr=f'def __init__(self,'
        for item in fields:
            if item in defaults:
                rstr+=f", {item}={defaults[item]}"
            else:
                rstr+= f' {item},'
        
        rstr=rstr[:-1]+'):\n'
        for name in fields:
            rstr+= f'        self.{name}={name}\n'
        return rstr
    def accessor_str(fields):
        rstr = ''
        for name in fields:
            rstr+=f'    def get_{name}(self):\n'
            rstr+=f'        return self.{name}\n\n'
        return rstr
    
    class_definition = f'''\
class {type_name}:
    _fields = {str(fields)}
    _mutable = {mutable}
    {init_str(fields,defaults)}
    def __repr__(self):
        return '{type_name}'+ str(tuple(str(key)+'='+str(self.__dict__[key]) for key in self._fields)).replace("'",' ').replace(' ','')
        
{accessor_str(fields)}
    def __getitem__(self,item):
        if type(item)==int:
            if not item<len(self._fields): raise IndexError("Index out of range")
            return self.__dict__[self._fields[item]]
        if type(item)==float:
            raise IndexError("Index cannot be float")
        elif type(item)==str:
            if item not in self._fields: raise IndexError("key is not in the field names")
            return self.__dict__[item]
            
    def __eq__(self,right):
        if type(self)==type(right) and self._fields == right._fields and all(self[k]==right[k] for k in self._fields):
            return True
        return False
        
    def _asdict(self):
        rdict = dict()
        for k in self._fields:
            rdict[k]=self[k]
        return rdict
        
    def _make(iterable):
        return {type_name}(*iterable)
    
    def _replace(self,**kargs):
        if any(k not in self._fields for k in kargs): raise TypeError("kargs names are nott field_names")
        if self._mutable:
            for k in kargs:
                self.__dict__[k]=kargs[k]
        elif not(self._mutable):
            new = dict()
            for name in self._fields:
                if name in kargs:
                    new[name]=kargs[name]
                else:
                    new[name]=self.__dict__[name]
            return type(self)._make(new.values())
            
    def __setattr__(self,key,value):
        if len(self.__dict__)!=len(self._fields):
            self.__dict__[key] = value
        else:
            if (not self._mutable):
                raise AttributeError("Cannot change immutable object")
            else:
                self.__dict__[key]=value   

    '''

    
    # Debug help: uncomment next line, which prints source code for the class
    # show_listing(class_definition)
    
    # Execute the class_definition's str in name_space; next bind its
    #   source_code attribute to this class_definition; following try+except
    #   return the class object created; if there are any syntax errors, show
    #   the class and also show the error
    name_space = dict( __name__ = f'pnamedtuple_{type_name}' )                    
    try:
        exec(class_definition,name_space)
        name_space[type_name].source_code = class_definition
    except (TypeError,SyntaxError):                        
        show_listing(class_definition)
        traceback.print_exc()
    return name_space[type_name]


    
if __name__ == '__main__':
    # Test simple pnamedtuple below in script: Point=pnamedtuple('Point','x,y')

    #driver tests
    import driver  
    driver.default_file_name = 'bscp3S22.txt'
#     driver.default_show_exception_message = True
#     driver.default_show_traceback = True
    driver.driver()
