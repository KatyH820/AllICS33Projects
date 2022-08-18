import inspect
class C:
    def __init__(self,x):
        self.x = x
    
    def __str__(self):
        return str(self.__dict__)
    
    def bump(self):
        self.x += 1
        
    def __setattr__(self,attr,value):
        code_calling_setattr = inspect.currentframe().f_back.f_code
        code_from_this_class = object.__getattribute__(self,'__class__').__dict__.get(code_calling_setattr.co_name,None)
        assert code_from_this_class != None\
                  and code_calling_setattr is code_from_this_class.__code__,\
                    f'Attempt to set attribute "{attr}" from outside class {object.__getattribute__(self,"__class__")}'
        object.__getattribute__(self,'__dict__')[attr] = value
        
    def __getattribute__(self,attr):
        if not inspect.ismethod(object.__getattribute__(self,attr)):
            code_calling_setattr = inspect.currentframe().f_back.f_code
            code_from_this_class = object.__getattribute__(self,'__class__').__dict__.get(code_calling_setattr.co_name,None)
            assert code_from_this_class != None\
                      and code_calling_setattr is code_from_this_class.__code__,\
                    f'Attempt to get non-method attribute "{attr}" from outside class {object.__getattribute__(self,"__class__")}'
        return object.__getattribute__(self,attr)


o = C(5) # self.x = in __init__ should work
o.bump() # self.x += 1 in bump  should work
print(f'Initial state of o: {o}')

try:
    o.x = 1  # assignment, not in C's methods, should fail
    print('o.x = 1 worked, but should have failed')
except:
    print("Assignment o.x = 1 outside of methods in class C failed")

# Remove o.x = 1 and try the following
def bump(obj):
    obj.x += 1

try:
    bump(o)  # Same method name as in C, but different code, should fail
    print('bump(0) worked, but should have failed')
except:
    print("Call bump(o) with same name as a method in class C failed")

try:
    print(o.x)  # Attempt to access this attribute outside the 
    print('print(o.x) worked, but should have failed')
except:
    print("Access o.x with outside of methods in class C failed")

print(f'Final state of o: {o}')