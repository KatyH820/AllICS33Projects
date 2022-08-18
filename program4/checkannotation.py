from goody import type_as_str
import inspect
# Submitter: katyh1(Huang, Katy)
# Partner  : jessieh9(He, Jessie)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming

class Check_All_OK:
    """
    Check_All_OK class implements __check_annotation__ by checking whether each
      annotation passed to its constructor is OK; the first one that
      fails (by raising AssertionError) prints its problem, with a list of all
      annotations being tried at the end of the check_history.
    """
       
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_All_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check,param,value,check_history):
        for annot in self._annotations:
            check(param, annot, value, check_history+'Check_All_OK check: '+str(annot)+' while trying: '+str(self)+'\n')


class Check_Any_OK:
    """
    Check_Any_OK implements __check_annotation__ by checking whether at least
      one of the annotations passed to its constructor is OK; if all fail 
      (by raising AssertionError) this classes raises AssertionError and prints
      its failure, along with a list of all annotations tried followed by the
      check_history.
    """
    
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_Any_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check,param,value,check_history):
        failed = 0
        for annot in self._annotations: 
            try:
                check(param, annot, value, check_history)
            except AssertionError:
                failed += 1
        if failed == len(self._annotations):
            assert False, repr(param)+' failed annotation check(Check_Any_OK): value = '+repr(value)+\
                         '\n  tried '+str(self)+'\n'+check_history                 



class Check_Annotation:
    # We start by binding the class attribute to True meaning checking can occur
    #   (but only when the function's self._checking_on is also bound to True)
    checking_on  = True
  
    # For checking the decorated function, bind its self._checking_on as True
    def __init__(self, f):
        self._f = f
        self._checking_on = True

    # Check whether param's annot is correct for value, adding to check_history
    #    if recurs; defines many local function which use it parameters.  
    def check(self,param,annot,value,check_history=''):
        
        # Define local functions for checking, list/tuple, dict, set/frozenset,
        #   lambda/functions, and str (str for extra credit)
        # Many of these local functions called by check, call check on their
        #   elements (thus are indirectly recursive)
        # We start by comparing check's function annotation to its arguments
        def check_list_tuple(obj_type):
            assert type(value) is obj_type, f"'{param}' failed annotation check(wrong type): value = {repr(value)}\n\twas type {type_as_str(value)} ...should be type {str(obj_type)[8:-2]}"
            if len(annot) == 1:
                for pos, ele in enumerate(value):
                    self.check(param, annot[0], ele, f'{str(obj_type)[8:-2]}[{str(pos)}] check: {annot[0]}')
            elif len(annot) > 1:
                assert len(value) == len(annot), f"'{param}' failed annotation check(wrong number of elements): value = [{repr(value)}]\n\tannotation had {len(annot)} elements{str(annot)}"
                for pos, ele in enumerate(value):
                    self.check(param, annot[pos], ele, f'{str(obj_type)[8:-2]}[{str(pos)}] check: {annot[pos]}')
        def check_set_frozenset(s_type):
            assert type(value) == s_type, f"'{param}' failed annotation check(wrong type): value = {repr(value)}\n\twas type {type_as_str(value)} ...should be type {str(s_type)[8:-2]}"
            assert len(annot) == 1, f"'{param}' annotation inconsistency: set should have 1 item but had {len(annot)}\n\t annotation = {annot}"
            for x in value:
                self.check(param, list(annot)[0], x, f'set value check: {list(annot)[0]}')
        
        def check_dict():
            assert isinstance(value, dict), f"'{param}' failed annotation check(wrong type): value = {repr(value)}\n\twas type {type_as_str(value)} ...should be type dict"
            assert len(annot) == 1, f"'{param}' annotation inconsistency: dict should have 1 item but had {len(annot)}\n\t annotation = {annot}"
            for k,v in value.items():
                self.check(param, list(annot.keys())[0], k, f'dict key check: {list(annot.keys())[0]}')
                self.check(param, list(annot.values())[0], v, f'dict value check: {list(annot.values())[0]}')
            
        def check_fun():
            sig = inspect.signature(annot)
            assert len(sig.parameters) == 1, f"'{param}' annotation inconsistency: predicate should have 1 parameter but had {len(sig.parameters)}\n\tpredicate = {annot}"
            try:
                answer = annot(value)
            except Exception as error:
                assert False, f"'{param}' annotation predicate({annot}) raised exception\n  exception = {type(error).__name__}: {error}\n{check_history}"
            else:
                assert answer,f"'{param}' failed annotation check: value = {repr(value)}\n\t predicate = {annot}"
        def check_str():
            try:

                eval(annot)
            except Exception as error:
                assert False,error
            else:
                assert eval(annot),'next'
                
        if annot == None:
            return 
        elif type(annot) is type:
            assert isinstance(value, annot), f"'{param}' failed annotation check(wrong type): value = {repr(value)}\n\t was type {type_as_str(value)} ...should be type {str(annot)[8:-2]}"
        elif isinstance(annot, list):
            check_list_tuple(list)
        elif isinstance(annot, tuple):
            check_list_tuple(tuple)
        elif isinstance(annot, dict):
            check_dict()
        elif isinstance(annot, set):
            check_set_frozenset(set)
        elif isinstance(annot, frozenset):
            check_set_frozenset(frozenset)
        elif inspect.isfunction(annot):
            check_fun()
        elif isinstance(annot,str):
            check_str()
        else:
            try:
                annot.__check_annotation__(self.check, param, value, check_history)
            except AttributeError:
                raise AssertionError(f"'{param}' annotation undecipherable: {annot}")
    # Return result of calling decorated function call, checking present
    #   parameter/return annotations if required
    def __call__(self, *args, **kargs):

        # Returns the parameter->argument bindings as an OrderedDict, derived
        #   from dict, binding the function header's parameters in order

        def param_arg_bindings():
            f_signature  = inspect.signature(self._f)
            bound_f_signature = f_signature.bind(*args,**kargs)
            for param in f_signature.parameters.values():
                if not (param.name in bound_f_signature.arguments):
                    bound_f_signature.arguments[param.name] = param.default
            return bound_f_signature.arguments
        # If annotation checking is turned off at the class or function level
        #   just return the result of calling the decorated function
        # Otherwise do all the annotation checking
        if not self._checking_on:
            
            return self._f(args,kargs)
        else:
            try:
                # Check the annotation for each of the annotated parameters
                binding = param_arg_bindings()
                expected = self._f.__annotations__
                # Compute/remember the value of the decorated function
                for arg in binding:
                    self.check(arg, expected[arg], binding[arg])
                decorated  = self._f(*args,**kargs)
                # If 'return' is in the annotation, check it
                if 'return' in expected:
                    binding['_return']=expected['return']
                    self.check('return', expected['return'], decorated)
                # Return the decorated answer
                return decorated
                
            # On first AssertionError, print the source lines of the function and reraise 
            except AssertionError:
                # print(80*'-')
                # for l in inspect.getsourcelines(self._f)[0]: # ignore starting line #
                #     print(l.rstrip())
                # print(80*'-')
                raise




  
if __name__ == '__main__':     
    # an example of testing a simple annotation  
    # def f(x:int): pass
    # f = Check_Annotation(f)
    # f(3)
    # f('a')
           
    #driver tests
    import driver
    driver.default_file_name = 'bscp4S22.txt'
#     driver.default_show_exception= True
#     driver.default_show_exception_message= True
#     driver.default_show_traceback= True
    driver.driver()
