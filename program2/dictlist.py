from goody import type_as_str  # Useful for some exceptions

# Submitter: katyh1(Huang, Katy)
# Partner  : jessieh9(He, Jessie)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming

class DictList:
    _initialized=False
    def __init__(self,*args):     
        assert len(args)>0, "Argument cannot be empty"
        for d in args:
            assert type(d) is dict, f"{d} is not a dictionary"
            assert len(d)>0, "Dictionary cannot be empty"
        self.dl = [d for d in args]
        self._initialized=True
    
    def __len__(self):
        return len({k for d in self.dl for k in d})
    
    def __bool__(self):
        return True if len(self.dl)>1 else False
    
    def __repr__(self):
        return f'DictList({str(self.dl)[1:-1]})'
    
    def __contains__(self, key):
        return True if any(key == k for d in self.dl for k in d) else False

    def __getitem__(self,key):
        if not(self.__contains__(key)): raise KeyError(f"{key} not in dictionary keys")
        values = [self.dl[d][key] for d in range(len(self.dl)) if key in self.dl[d]]
        return values[-1]
    
    def __setitem__(self,key,value):
        if not(self.__contains__(key)):
            self.dl.append({key:value})
        else:
            for i in range(len(self.dl)-1,-1,-1):
                if key in self.dl[i]:
                    self.dl[i][key]=value
                    break
    
    def __delitem__(self,key):
        if not(self.__contains__(key)): 
            raise KeyError(f"{key} not in dictionary keys")
        else:
            for i in range(len(self.dl)-1,-1,-1):
                if key in self.dl[i]:
                    del self.dl[i][key]
                    if len(self.dl[i])==0:
                        self.dl.remove(self.dl[i])
                    break
    
    def __call__(self,key):
        return [(d,self.dl[d][k]) for d in range(len(self.dl)) for k in self.dl[d] if k==key]
                
    
    def __iter__(self):
        stored = []
        for d in self.dl[::-1]:
            for k in sorted(d):
                if k not in stored:
                    yield k
                    stored.append(k)
    
    def items(self):
        keys = [k for k in self.__iter__()]
        for d in self.dl[::-1]:
            for k in d:
                if k in keys:
                    yield (k,d[k])
                    keys.remove(k)
    
    def collapse(self):
        return {k:d[k] for d in self.dl for k in d}
    

    def __eq__(self,d2):
        if type(d2)!= DictList and type(d2)!=dict: raise TypeError("right operand must be DictList or Dictionary")
        keys = list(self)
        if sorted(self)==sorted(d2):
            for k in keys:
                if d2[k]!=self[k]:
                    return False
            return True
        return False
    
    def __lt__(self,d2):
        if type(d2)!= DictList and type(d2)!=dict: raise TypeError("right operand must be DictList or Dictionary")
        if set(d2)>(set(self)):
            for k in self:
                if d2[k]!=self[k]:
                    return False
            return True         
        return False
    
    def __gt__(self,d2):
        if type(d2)!= DictList and type(d2)!=dict: raise TypeError("right operand must be DictList or Dictionary")
        if set(d2)<set(self):
            for k in d2:
                if d2[k]!=self[k]:
                    return False
            return True
        return False
    
    def __add__(self, d2):
        if type(d2) != dict and type(d2) != DictList: raise TypeError(f'{d2} is not type DictList nor type dict')
        new = self.dl[:]
        if type(d2) == DictList:
            new.extend(d2.dl)
        else:
            new.append(d2)
        return eval(f'DictList({str(new)[1:-1]})')
    
    def __radd__(self, d2):
        if type(d2) != dict and type(d2) != DictList: raise TypeError(f'{d2} is not type DictList nor type dict')
        new = [d2]
        if type(self) == DictList:
            new.extend(self.dl)
        else:
            new.append(self)
        return eval(f'DictList({str(new)[1:-1]})')


    def __setattr__(self,name,value):
        if self._initialized:
            raise AssertionError('Cannot add new attributes to object after init')
        self.__dict__[name] = value

   
if __name__ == '__main__':
    #Simple tests before running driver
    #Put your own test code here to test DictList before doing bsc tests
    
    d = DictList(dict(a=1,b=2), dict(b=12,c=13))

    print('len(d): ', len(d))
    print('bool(d):', bool(d))
    print('repr(d):', repr(d))
    print(', '.join("'"+x+"'" + ' in d = '+str(x in d) for x in 'abcx'))
    print("d['a']:", d['a'])
    print("d['b']:", d['b'])
    print("d('b'):", d('b'))
    print('iter results:', ', '.join(i for i in d))
    print('item iter results:', ', '.join(str(i) for i in d.items()))
    print('d.collapse():', d.collapse())
    print('d==d:', d==d)
    print('d+d:', d+d)
    print('(d+d).collapse():', (d+d).collapse())
    
    print()
    import driver
    driver.default_file_name = 'bsc22S22.txt'
    # driver.default_show_exception= True
    # driver.default_show_exception_message= True
    # driver.default_show_traceback= True
    driver.driver()
