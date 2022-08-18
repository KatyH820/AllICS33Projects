# Update by setting bool as to whether setting new attributes outside class methods are allowed
import inspect
class C:
    _private = {"x",'bump2'}
    def __init__(self,x):
        self.x = x
        self.y = x
        
    def __str__(self):
        return str(self.__dict__)
    
    def bump(self):
        self.x += 1
        
        
    def bump2(self):
        self.x += 1
        
        
    def bump3(self):
        self.bump2()
        
        
    def __setattr__(self,attr,value):
        if attr in object.__getattribute__(self,'__class__')._private:
            code_calling_setattr = inspect.currentframe().f_back.f_code
            code_from_this_class = object.__getattribute__(self,'__class__').__dict__.get(code_calling_setattr.co_name,None)
            assert code_from_this_class != None\
                      and code_calling_setattr is code_from_this_class.__code__,\
                    f"Attempt to set private attribute \"{attr}\" from outside class {object.__getattribute__(self,'__class__')}"
        object.__getattribute__(self,'__dict__')[attr] = value
        
    def __getattribute__(self,attr):
        if  attr in object.__getattribute__(self,'__class__')._private:
            code_calling_setattr = inspect.currentframe().f_back.f_code
            code_from_this_class = object.__getattribute__(self,'__class__').__dict__.get(code_calling_setattr.co_name,None)
            assert code_from_this_class != None\
                      and code_calling_setattr is code_from_this_class.__code__,\
                    f"Attempt to get private attribute \"{attr}\" from outsidee class {object.__getattribute__(self,'__class__')}"
        return object.__getattribute__(self,attr)




o = C(5) # self.x = in __init__ should work
o.bump() # self.x += 1 in bump  should work
o.y = 1  # o.y = 1 should work (y is not private
print(f'Initial state of o: {o}')

try:
    o.x = 1  # assignment to private, should fail
    print('o.x = 1 worked, but should have failed')
except:
    print("Assignment o.x = 1 failed: x is considered private in class C")

try:
    o.bump2()  # call of private, should fail
    print('o.bump2() worked, but should have failed')
except:
    print("Call o.bump2() failed: bump2 is considered private in class C")


o.bump3() # bump3 is not private; it calls private bump2 which is allowed


# Remove o.x = 1 and try the following
def bump(obj):
    obj.x += 1

try:
    bump(o)  # Same method name as in C, but different code, should fail
    print('bump(0) worked, but should have failed')
except:
    print("Call bump(o) failed: same name as a method in class C but not in class C")

try:
    print(o.x)  # Attempt to access this attribute outside the 
    print('print(o.x) worked, but should have failed')
except:
    print('Access o.x failed: x is considered private in class C')

o.z = 1

print(f'Final state of o: {o}')