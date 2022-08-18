import inspect
import re

division = '\n'+78*'-'
max_attr_length = 1000
def bump(mo):
    return 'TOP' + str(int(mo.group(1))-1)    
    
def display_all_attributes(text,obj):
    dispatch = {
        "<class 'module'>" : ['__doc__', '__file__'],
        "<class 'type'>" : ['__doc__', '__name__', '__qualname__', '__module__'],
        "<class 'method'>" : ['__doc__', '__name__', '__qualname__', '__func__', '__self__', '__module__'],
        "<class 'function'>" : ['__doc__', '__name__', '__qualname__', '__code__', '__defaults__', '__kwdefaults__', '__globals__', '__annotations__', '__closure__', '__module__'],
        "<class 'frame'>" : ['f_code.co_name', 'f_back', 'f_builtins', 'f_code', 'f_globals', 'f_lasti', 'f_lineno', 'f_locals', 'f_trace'],
        "<class 'code'>" : ['co_argcount', 'co_code', 'co_cellvars', 'co_consts', 'co_filename', 'co_firstlineno', 'co_flags',
                    'co_lnotab', 'co_freevars', 'co_posonlyargcount', 'co_kwonlyargcount', 'co_name',  'co_names',  'co_nlocals', 'co_stacksize', 'co_varnames'],
        "<class 'builtin_function_or_method'>" : ['__doc__', '__name__', '__qualname__', '__self__']}

    attrs = dispatch[(key := str(type(obj)))]
    max_len = max(len(k) for k in attrs)
    if key ==  "<class 'frame'>":
        if obj.f_back == None:
            print('\n'+re.sub(r"TOP([+-]?\d*)","BOTTOM",text)+": "+str(type(obj)))
        else:
            print(f'\n{text.replace("TOP0","TOP")}: {type(obj)}')
    else:
        print(f'\n{text}: {type(obj)}')
    for attr in sorted(dispatch[str(type(obj))]):
        try:
            print(f'  {attr:{max_len}} : ',end='')
            print(f'{str(eval("obj."+attr))[0:max_attr_length]}')
        except:
            print('...Not found')
    if key == "<class 'function'>":
        display_all_attributes(text+" code",obj.__code__)
    elif key ==  "<class 'method'>":
        display_all_attributes(text+" code",obj.__func__.__code__)
    elif key ==  "<class 'frame'>" and obj.f_back != None:
            display_all_attributes(re.sub(r'TOP([+-]?\d*)',bump,text),obj.f_back)


def display_signature(text,f):
    print(f'\n{text}')
    sig = inspect.signature(f) 
    print('str(signature) =', str(sig))
    max_len = max([len(param) for param in sig.parameters])
    print('Information about each parameter name')
    for param_name,param_info in sig.parameters.items():
        print(f'  {param_name:{max_len}} : annotation = {param_info.annotation}')
        print(f'  {" ":{max_len+3}}default    = {param_info.default}')
        print(f'  {" ":{max_len+3}}kind       = {param_info.kind.description}')
 

def display_binding_information(text,f,*args,**kargs):
    combine_args = args + tuple(str(p)+' = '+str(v) for p,v in kargs.items())
    str_args = '(' + ', '.join(str(v) for v in combine_args)+')'
    print(text)
    print('\nSignature/Binding information for:',f.__name__+str_args)
    display_signature('Signature',f)
    try:
        sig = inspect.signature(f)
        ba = sig.bind(*args,**kargs)
        print('\nWith the assignment, ba = inspect.signature(f).bind(*args,**kargs)')
        print('  ba.arguments       :',ba.arguments)
        print('  ba.args            :',ba.args)
        print('  ba.kwargs          :',ba.kwargs)
        print('  ba.signature       :',ba.signature)
        print('  ba.apply_defaults():',ba.apply_defaults())
        print('  ba.args            :',ba.arguments)
    except:
        print('Binding failed: no further information')



def is_even(x ) -> bool:
    """x is even if its remainder is 0 when divided by two"""
    return x%2 == 0

def opposite_of(f : callable) -> callable:
    def not_f(x):
        return not f(x)
    return not_f

display_all_attributes('function is_even', is_even)
print(division)

display_all_attributes('function opposite_of', opposite_of)
print(division)

display_all_attributes('function not_f', opposite_of(is_even))
print(division)

display_signature('function is_even ',is_even)
print(division)

def f(a,b,*c,d=None,**kargs): pass
display_binding_information('\ndef f(a,b,*c,d=None,**kargs): pass',f,1,2,3,4,5,6, foo = 3)

print(division)


def factorial(n : int) -> int:
    if n == 0:
        display_all_attributes(f'factorial_frame TOP0', inspect.currentframe()); return 1
    else:
        return n*factorial(n-1)
    
print(factorial(3))   