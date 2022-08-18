import inspect

# Store a raw_function object, and a reference to the class for dispatching it
# When a DispatchableFunction is called, use the dispatch_class to find the raw
#  function with the correct name and signature and then call it 
class DispatchableFunction:
    # Remember the raw function and the dispatching class for it
    def __init__(self, raw_function, dispatch_class):
        self.raw_function   = raw_function            # store decoration information for function
        self.dispatch_class = dispatch_class
    
    # When any dispatchable function is called, determine which function to call
    #   by using rules from the dispatch_class (which tries to match the name and signature)     
    def __call__(self, *args, **kargs):
        df = self.dispatch_class.dispatch(self, *args, **kargs) # find it
        return df.raw_function(*args, **kargs)                  # call it




                                                 
# Functions registered in this class are dispatched by their names and signature
#  (parameter annotations)
# If the argument types don't identically match any annotation, check for a unique match
#    of the argument values as instances of the signature annotations: uses in inheritance
# See the register/dispatch (and key) methods for details
class DispatchBySignature:
    function_map = {} # Updated by register method (used as a decorator); examined by dispatch
    

    # This class will never be instantiated 
    def __init__(self):
        raise Exception('DispatchBySignature.__init__: Attempted to construct an object from this class')    
    

    # Helper called by register and dispatch (in DispatchableFunction.__call__) to access
    #   the unique correct DispatchBySignature object storing the function_map      
    # Computes/returns the hashable key (for storing/finding functions in the function_map): 
    #   a tuple of the function's name, followed by a tuple types computed from either a
    #   (a) register: all the types (annotations) of parameters, with object replacing unspecified annotations
    #   (b) dispatch: all the types of arguments in a function call
    # Use the tuple constructor to compute the tuple, not a generator, to compute the tuple
    @staticmethod
    def key(raw_function, args=None):
        if args != None: # called from dispatch (in DispatchableFunction.__call__): use argument types
            types = tuple([type(a) for a in args]) 
        else:            # called from register: use annotations (with object when unspecified) 
            signature = inspect.signature(raw_function).parameters
            types = tuple([(spec.annotation if spec.annotation != inspect._empty else object)
                              for _,spec in signature.items()])

        return tuple([raw_function.__name__, types]) 
      

    # Decorate the raw_function by putting its key in the function_map; ensure it is unique
    @staticmethod
    def register(raw_function):
        df = DispatchableFunction(raw_function, DispatchBySignature)
        sig_key = DispatchBySignature.key(raw_function, args=None)
        
        if sig_key in DispatchBySignature.function_map:
            raise TypeError('DispatchBySignature.register: attempt to re-register a signature =',sig_key)
 
        DispatchBySignature.function_map[sig_key] = df
        return df

    # Lookup the registered raw function based on df using the DispatchBySignature semantics
    # Note that **kargs must be present here, but does not participate in computing the key
    @staticmethod
    def dispatch(df, *args, **kargs):
        raw_function = df.raw_function 
        # Try for a direct match (all argument types == signature annotations) and return it
        arg_types        = DispatchBySignature.key(raw_function, args=args)
        unique_f_to_call = DispatchBySignature.function_map.get(arg_types, None)
        if unique_f_to_call != None:
            return unique_f_to_call
        
        # (To understand the following code, you must understand Inheritance in Python)
        # Otherwise, build a list of all matching functions, based in inheritance hierarchies
        #   and checking whether isinstance(argument-values,signature-annotations)
        matching = [(param_annots, raw_func)
                       for param_annots, raw_func in DispatchBySignature.function_map.items()
                          if len(arg_types) == len(param_annots)
                             and arg_types[0] == param_annots[0]
                             and all(isinstance(at, pa) for at, pa in zip(args, param_annots[1]))]
        
        # If there is a unique match, return it; otherwise raise one of two exceptions
        # Some languages will "score" multiple matches and return the one with the highest score
        if len(matching) == 1:
            return matching[0][1] # [0] only item [1] function for that item
        elif len(matching) == 0:
                raise TypeError("DispatchBySignature.dispatch: No matching functions located for",arg_types,'in',[a for a  in DispatchBySignature.function_map])
        
        else:
            raise TypeError("DispatchBySignature.dispatch: Multiple matching functions located for",arg_types,'in',[a for a, _  in matching])





if __name__ == '__main__':

    def show_and_eval_handling_exceptions(expr_as_str):
        print('\nshow_and_eval_handling_exceptions:',expr_as_str)
        try:
            print('  ...value is', eval(expr_as_str))
        except Exception as e:
            print('  ...value is not computable by dispatching')
            print(e)
       
 
    print('\nregistering: def f (a : int, b : int) -> int:',)
    @DispatchBySignature.register
    def f (a : int, b : int) -> int:
        return a + b
    
    print('\nregistering: def f (a : str, b : str) -> int:',)
    @DispatchBySignature.register
    def f (a : str, b : str) -> int:
        return len(a) + len(b)
 
    show_and_eval_handling_exceptions('f(1,1)')
    show_and_eval_handling_exceptions('f("abc","xyz")')  
    
    try: 
        print('\nregistering: def f (a : int, b : int) -> int:')
        @DispatchBySignature.register
        def f (a : int, b : int) -> int:
            return a + b
    except Exception as e:
        print('  ...failed to register')
        print(e)
        
    show_and_eval_handling_exceptions('f("abc",1)')  
     
    print('\nregistering: def f (a : str, b : int) -> int:',)
    @DispatchBySignature.register
    def f (a : str, b : int) -> int:
        return len(a) + b
    
    show_and_eval_handling_exceptions('f("abc",1)')  
    show_and_eval_handling_exceptions('f("abc",1.)')  
 
    import numbers
    print('\nregistering: def f (a : str, b : numbers.Number) -> int:',)
    @DispatchBySignature.register
    def f (a : str, b : numbers.Number) -> int:
        return len(a) + b
    
    show_and_eval_handling_exceptions('f("abc",1.)')  
    show_and_eval_handling_exceptions('f("abc",3+4j)')  
    