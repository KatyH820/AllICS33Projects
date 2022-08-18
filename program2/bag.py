from collections import defaultdict
from goody import type_as_str

# Submitter: katyh1(Huang, Katy)
# Partner  : jessieh9(He, Jessie)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming


class Bag:
    def __init__(self, bag=[]):
        self._bag = {k:bag.count(k) for k in bag}
        # self._bk = list(self._bag)
        
    def __repr__(self):
        if len(self._bag) != 0:
            return f'Bag({[key for key in self._bag for x in range(self._bag[key])]})'
        else:
            return 'Bag()'
        
    def __str__(self):
        string = 'Bag('
        if len(self._bag) != 0:
            for k,v in self._bag.items():
                string += f'{k}[{str(v)}],'
            string= string[:-1]
        string += ')'
        return  string

    def __len__(self):
        return sum([v for v in self._bag.values()])
    
    def unique(self):
        return len(self._bag.keys())
    
    def __contains__(self,ele):
        return ele in self._bag.keys()
    
    def count(self,ele):
        return self._bag[ele] if ele in self._bag else 0
    
    def add(self,ele):
        if ele in self._bag:
            self._bag[ele]+=1
        else:
            self._bag[ele]=1
    
    def __add__(self,b1):
        if type(b1) is not Bag: raise NotImplemented
        nlst = [ele for ele in b1._bag for i in range(b1._bag[ele])]
        olst = [ele for ele in self._bag for i in range(self._bag[ele])]
        new_info = nlst+olst
        return Bag(new_info)
    
    def remove(self,ele):
        if ele in self._bag and self._bag[ele] >0:
            self._bag[ele]-=1
            if self._bag[ele] == 0:
                del self._bag[ele]
        else:
            raise ValueError(f'{ele} is not in the bag')
    
    def __eq__(self, b1):
        if type(b1) != Bag:
            return False
        return self._bag.items() == b1._bag.items()
    
    def __iter__(self):
        odict = self._bag.copy()
        def _gen(bag):
            for item in bag:
                for num in range(odict[item]):
                    yield item
        return _gen(list(self._bag))
    



        

    



        
        

                
              



if __name__ == '__main__':
    # print(all((v+'['+str(c)+']' in str(b1) for v,c in dict(a=1,b=2,c=1,d=3).items())))
    #driver tests
    import driver
    driver.default_file_name = 'bsc21S22.txt'
#     driver.default_show_exception= True
#     driver.default_show_exception_message= True
#     driver.default_show_traceback= True
    driver.driver()
