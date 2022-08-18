import inspect
class C:
    def __init__(self,x):
        self.x = x
    
    def bump(self):
        self.x += 1
        
        
# Original code assuming __getattribute__ works correctly
    def __setattr__(self,attr,value):
        code_calling_setattr = inspect.currentframe().f_back.f_code
        code_from_this_class = self.__class__.__dict__.get(code_calling_setattr.co_name,None)
#         #above code not call C.__getattribute__,
#         #and will work when calling C.__getattribute__ because C.__setattribute__ is method in C
#         #but doing the code below is faster, which bypasses calls to C.__getattribute__ altogether
#         code_from_this_class = object.__getattribute__(self,'__class__').__dict__.get(code_calling_setattr.co_name,None)
        assert code_from_this_class != None\
                  and code_calling_setattr is code_from_this_class.__code__,\
                f'Attempt to set attribute "{attr}" from outside class {self.__class__}'
        object.__getattribute__(self,'__dict__')[attr] = value
        
##Code with prints        
#     def __setattr__(self,attr,value):
#         print('setattribute')
#         code_calling_setattr = inspect.currentframe().f_back.f_code
#         print('got code_calling')
#         code_from_this_class = object.__getattribute__(self,'__class__').__dict__.get(code_calling_setattr.co_name,None)
#         print('got code_from')
# #         code_from_this_class = self.__class__.__dict__.get(code_calling_setattr.co_name,None)
#         assert code_from_this_class != None\
#                   and code_calling_setattr is code_from_this_class.__code__,\
#                 f'Attempt to set attribute "{attr}" from outside class {self.__class__}'
#         print('after assert')
#         object.__getattribute__(self,'__dict__')[attr] = value
#         print('after setting')
#         
#     def __getattribute__(self,attr):
#         print('getattribute',attr)
#         if not inspect.ismethod(object.__getattribute__(self,attr)):
#             code_calling_setattr = inspect.currentframe().f_back.f_code
#             
#             code_from_this_class = object.__getattribute__(self,'__class__').__dict__.get(code_calling_setattr.co_name,None)
#     
#             assert code_from_this_class != None\
#                       and (method or code_calling_setattr is code_from_this_class.__code__),\
#                     f'Attempt to set attribute "{attr}" from outside class ' #{self.__class__}'
#         return object.__getattribute__(self,attr) # specify __geatattribute__ inherited from object class
# 
# #Code without prints
#     def __setattr__(self,attr,value):
#         code_calling_setattr = inspect.currentframe().f_back.f_code
#         code_from_this_class = object.__getattribute__(self,'__class__').__dict__.get(code_calling_setattr.co_name,None)
#         assert code_from_this_class != None\
#                   and code_calling_setattr is code_from_this_class.__code__,\
#                 f'Attempt to set attribute "{attr}" from outside class {self.__class__}'
#         object.__getattribute__(self,'__dict__')[attr] = value
#         
#     def __getattribute__(self,attr):
#         if not inspect.ismethod(object.__getattribute__(self,attr)):
#             code_calling_setattr = inspect.currentframe().f_back.f_code
#             
#             code_from_this_class = object.__getattribute__(self,'__class__').__dict__.get(code_calling_setattr.co_name,None)
#     
#             assert code_from_this_class != None\
#                       and (method or code_calling_setattr is code_from_this_class.__code__),\
#                     f'Attempt to set attribute "{attr}" from outside class {self.__class__}'
#         return object.__getattribute__(self,attr) # specify __geatattribute__ inherited from object class
# 
    # Must do all getting attribute from self/C non-recursively with object.__getattribute__
    # 
    def __getattribute__(self,attr):
        if not inspect.ismethod(object.__getattribute__(self,attr)):
            code_calling_setattr = inspect.currentframe().f_back.f_code
            
#             #This code from __setattr__ cannot be used here, because of recursion problem
#             #Instead attribute retrieval for C objects must be done with object.__getattribute__
#             code_from_this_class = self.__class__.__dict__.get(code_calling_setattr.co_name,None)

            code_from_this_class = object.__getattribute__(self,'__class__').__dict__.get(code_calling_setattr.co_name,None)
       
            assert code_from_this_class != None\
                      and code_calling_setattr is code_from_this_class.__code__,\
                    f'Attempt to set attribute "{attr}" from outside class {self.__class__}'
        return object.__getattribute__(self,attr)




o = C(5) # self.x = in __init__ should work
o.bump() # self.x += 1 in bump  should work

try:
    o.x = 1  # assignment, not in C's methods, should fail
except:
    print("Assignment o.x = 1 outside of methods in class C failed")

# Remove o.x = 1 and try the following
def bump(obj):
    obj.x += 1

try:
    bump(o)  # Same method name as in C, but different code, should fail
except:
    print("Call bump(o) with same name as a method in class C failed")

try:
    print(o.x)  # Attempt to access this attribute outside the 
except:
    print("Access o.x with outside of methods in class C failed")
