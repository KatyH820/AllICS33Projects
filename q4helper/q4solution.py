from helpers import primes, hide, nth
from builtins import RuntimeError



def differences(iterable1,iterable2):
    compare = zip(iterable1,iterable2)
    for i, ele in enumerate(compare):
        if ele[0]!=ele[1]:
            yield (i+1,ele[0],ele[1])
            
            
   
def once_in_a_row(iterable):
    added=[]
    for i in iterable:
        if len(added)==0 or i != added[-1]:
            yield i
        added.append(i)
                

def in_between(iterable, starter, stopper):
    gen = iter(iterable)
    doyield = False
    while True:
        try:
            if starter(x:=next(gen)):
                yield x
                doyield = True
                if stopper(x):
                    doyield = False
            while doyield:
                    y = next(gen)
                    yield y
                    if stopper(y):
                        doyield=False
        except StopIteration:
                return
        

def pick(iterable,n):
    gen = iter(iterable)
    lst1=[next(gen) for i in range(n)]
    while len(lst1)==n:
        yield lst1
        try:
            lst1=[next(gen) for i in range(n)]
        except StopIteration:
            return


def slice_gen(iterable, start, stop, step):
    assert step > 0, "Step must be positive";assert start >= 0,'Start must be non negative';assert stop >= 0, 'Stop must be non negative'
    gen = iter(enumerate(iterable))
    for i in range(start):next(gen)
    for i in range(start, stop, step): 
        try:
            n,a = next(gen)
            if n == i:
                yield a
            for j in range(step-1):
                next(gen)
        except StopIteration:
            return

 
def alternate_all(*args):
    lst = list(iter(arg) for arg in args)
    max_count = len(lst)
    while True:
        count = 0
        for arg in lst:
            try:
                yield next(arg)
            except StopIteration:
                count+=1
                if count == max_count:
                    break
                pass
        if count == max_count:
            break
        




class ListSI:
    def __init__(self,initial):
        self._real_list  = list(initial)
        self._iter_count = 0
        self.allow_change = True
    def __repr__(self):
        return repr(self._real_list)

    def __len__(self):
        return len(self._real_list)

    def append(self,value):
        if self.allow_change==False:
            raise RuntimeError
        self._real_list.append(value) #Write code here

    def __getitem__(self,index):
        return self._real_list[index]

    def __setitem__(self,index, value):
        self._real_list[index] = value

    def __delitem__(self,index):
        if self.allow_change==False:
            raise RuntimeError    
        del self._real_list[index] # Write code here

    def __iter__(self):   
        class ListSI_iter:
            def __init__(self,aList):
                self.main = aList
                self._aListSI = aList._real_list # Write code here
                self._next = 0
            def __next__(self):
                self._next+=1
                try:
                    return self._aListSI[self._next-1]
                except IndexError:
                    self.main._iter_count -=1
                    if self.main._iter_count ==0:
                        self.main.allow_change=True
                    raise StopIteration

            def __iter__(self):
                return self
        self.allow_change = False
        self._iter_count +=1
        return ListSI_iter(self)

def fool_it():
    l = ListSI(['a','b', 'c'])
    for i in l:
        break       # Write code here...

    l.append('z')  # so that this statement incorrectly raises a RuntimeError exception    


if __name__ == '__main__':
    # print(''.join([v for v in alternate_all(hide('fg'),hide('hijk'),hide('abcde'))]))
    #-->fhagibjckde
    
    # Test differences; you can add your own test cases
    print('Testing differences')
    for i in differences('3.14159265', '3x14129285'):
        print(i,end=' ')    
    print()

    for i in differences(hide('3.14159265'), hide('3x14129285')):
        print(i,end=' ')    
    print()

    for i in differences(primes(), hide([2, 3, 1, 7, 11, 1, 17, 19, 1, 29])):
        print(i,end=' ')    
    print('\n')

    for i in differences(hide([2, 3, 1, 7, 11, 1, 17, 19, 1, 29]), primes()):
        print(i,end=' ')    
    print('\n')

              
    # Test once_in_a_row; you can add your own test cases
    print('\nTesting once_in_a_row')
    for i in once_in_a_row('abcccaaabddeee'):
        print(i,end='')    
    print()

    for i in once_in_a_row(hide('abcccaaabddeee')):
        print(i,end='')    
    print('\n')
    
        
    # Test in_between; you can add your own test cases
    print('\nTesting in_between')
    for i in in_between('123abczdefalmanozstuzavuwz45z', (lambda x : x == 'a'), (lambda x : x == 'z')):
        print(i,end='')
    print()
    
    for i in in_between(hide('123abczdefalmanozstuzavuwz45z'), (lambda x : x == 'a'), (lambda x : x == 'z')):
        print(i,end='')
    print()
    
    for i in in_between(primes(), (lambda x : x%10 == 3), (lambda x : x%10 == 7)):
        print(i,end=' ')
        if i > 100:
            break
    print()
    
    for i in in_between('123abczdefalmanozstuzavuwz45z', (lambda x : x == 'a'), (lambda x : x == 'a')):
        print(i,end='')
    print('\n')


    # Test pick' you can add your own test cases
    print('\nTesting pick')
    for i in pick('abcdefghijklm',4):
        print(i,end='')
    print()
    
    for i in pick(hide('abcdefghijklm'),4):
        print(i,end='')
    print()

    for i in pick(primes(),5):
        print(i,end=' ')
        if i[3] > 100:
            break
    print('\n')


    # Test slice_gen; add your own test cases
    print('\nTesting slice_gen')
    for i in slice_gen('abcdefghijk', 3,7,1):
        print(i,end='')
    print()
       
    for i in slice_gen('abcdefghijk', 3,20,1):
        print(i,end='')
    print()
       
    for i in slice_gen(hide('abcdefghijklmnopqrstuvwxyz'), 3, 20, 3):
        print(i,end='')
    print()
       
    for i in slice_gen(primes(), 100,200,5):
        print(i,end=' ')
    print('\n')

    
    # Test alternate_all; you can add your own test cases
    print('Testing alternate_all')
    for i in alternate_all('abcde','fg','hijk'):
        print(i,end='')
    print('\n')
    
    for i in alternate_all(hide('abcde'), hide('fg'),hide('hijk')):
        print(i,end='')
    print('\n\n')


    # Test ListSI; you can add your own test cases
    print('Testing ListSI: no exception')
    l = ListSI(['a', 'b', 'c'])
    for i in l:
        print(i)
    l.append('z')
    print(l)
    print()
    
    # print('Testing ListSI: exception by append')
    l = ListSI(['a', 'b', 'c'])
    try:
        for i in l:
            l.append('z')
            print('worked, but should have raised exception')
    except RuntimeError:
        print('correctly raised exception')
    print(l)
    print()

    print('Testing ListSI: exception by del')
    l = ListSI(['a', 'b', 'c'])
    try:
        for i in l:
            del l[0]
            print('worked, but should have raised exception')
    except RuntimeError:
        print('correctly raised exception')
    print(l)
    print()
    
    print('Testing ListSI: no exception')
    l = ListSI(['a', 'b', 'c'])
    try:
        for i in l:
            for j in l:
                pass
        l.append('z')
    except RuntimeError:
        print('incorrectly raised exception')
    print(l)
    print()
    
    print('Testing ListSI: exception by append, nested 2')
    l = ListSI(['a', 'b', 'c'])
    try:
        for i in l:
            for j in l:
                l.append('z')
                print('worked, but should have raised exception')
    except RuntimeError:
        print('correctly raised exception')
    print(l)
    print()
    
    print('Testing ListSI: exception by append, nested 1')
    l = ListSI(['a', 'b', 'c'])
    try:
        for i in l:
            for j in l:
                pass
            l.append('z')
            print('worked, but should have raised exception')
    except RuntimeError:
        print('correctly raised exception')
    print(l)
    print('\n')
    
    print('Testing fool_it')
    try:
        fool_it()
        print('worked, but should have raised exception')
    except RuntimeError:
        print('correctly raised exception')
    print('\n\n')
    
    
    
    import driver
    driver.default_file_name = 'bscq4S22.txt'
#     driver.default_show_exception=True
#     driver.default_show_exception_message=True
#     driver.default_show_traceback=True
    driver.driver()
    
    
