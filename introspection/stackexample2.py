import inspect

class track_stack:
    def __init__(self,f):
        self.f         = f # function being decorated
        self.calls     = 0 # count of calls to fo
        self.max_stack = 0 # count of maximum # of calls to f in the stack
        self.args_to_dump_stack = None

    def dump_stack_when_args(self,args_to_dump_stack):
        self.args_to_dump_stack = args_to_dump_stack 
          
    def __call__(self,*args,**kargs):
        if args == self.args_to_dump_stack:
            print(80*'-')
            print('Dumping stack(top->bottom): shows function name in each call frame: *args=',args)
            for n,f in enumerate(inspect.stack(),0):
                print(f'{"Bottom" if f.frame.f_code.co_name == "<module>" else (n if n != 0 else "Top"):>8}',
                      f.frame.f_code.co_name,
                      f.frame.f_locals if self.f.__code__ is f.frame.f_code else "")
            print('Dumping stack finished')
            print(80*'-')

        self.calls += 1
        # Count the # of function calls in the stack and update self.max_stack
        #   if it exceeds its current value.
        in_stack_count = 0
        for f in inspect.stack():
            if self.f.__code__ is f.frame.f_code:
                in_stack_count += 1
        if in_stack_count > self.max_stack:
            self.max_stack = in_stack_count

        return self.f(*args,**kargs)

@track_stack
def factorial(n : int) -> int:
    if n == 0:
        return 1
    else:
        return n*factorial(n-1)
factorial.dump_stack_when_args((0,))

n = 5
print(f'\nfactorial({n}) =',factorial(n))
print('# of calls to this factorial function =',factorial.calls)
print('Maximum # of calls to this factorial function ever in the stack =',factorial.max_stack)


@track_stack
def fibonacci(n : int) -> int:
    if n == 0 or n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)
# Don't ever dump the stack

n = 10
print(f'\nfibonacci({n}) =',fibonacci(n))
print('# of calls to this fibonacci function =',fibonacci.calls)
print('Maximum # of calls to this fibonacci function ever in the stack =',fibonacci.max_stack)
