# Defines a special exception for use with the Graph class methods
# Use like any exception: e.g., raise GraphError('Graph.method: ...error indication...')
class GraphError(Exception):
    pass # Inherit all methods, including __init__
 
 
class Graph:
    def __init__(self,*args):
        self.edges = {}
        # You may not define any other attributes
        # Other methods will examine/update the edges attribute
        # Fill edges attribute with *args
        

    def __setitem__(self,o,d):
        if type(o) is not str or (type(d) is not str and d is not None):
            raise GraphError
        if type(o) is str and d == None and o not in self.edges:
            self.edges[o]=[set(),set()]
        elif type(o)==type(d)==str:
            if o not in self.edges:
                self.edges[o]=[set(),set()]
            if d not in self.edges:
                self.edges[d]=[set(),set()]
            self.edges[o][0].add(d)
            self.edges[d][1].add(o)
        
 
 
    def __getitem__(self,item):
        if item in self.edges:
            return self.edges[item][0]
        elif type(item) is tuple and len(item)==2 and item[0] in self.edges and item[1] in self.edges:
            return item[1] in self.edges[item[0]][0]
        else:
            raise GraphError
     

    def __len__(self):
        added=[]
        count =0
        for k in self.edges:
            for v in range(len(self.edges[k][0])):
                if (k,v) and (v,k) not in added:
                    count+=1
                    added.append((k,v))
        return count
 
    
    def __call__(self,d):
        if d in self.edges:
            return self.edges[d][1]    
        raise GraphError

    def degree(self,n):
        if n not in self.edges:
            raise GraphError
        return len(self[n])+len(self(n))
 
     
    def __contains__(self,item):
        if type(item) is str:
            return item in self.edges
        if type(item) is tuple and len(item)==2 and item[1] in self.edges:
            return item[0] in self.edges[item[1]][1]
        else:
            return False    
     

    def load(self,file_name):
        self.edges={}
        for line in file_name:
            l=line.strip().split(':')
            for i in l:
                if i not in self.edges:
                    self.edges[i]=[set(),set()]
                if i != l[0]:
                    self.edges[l[0]][0].add(i)
                    self.edges[i][1].add(l[0])
            

    def __iter__(self):
        order = sorted([k for k in self.edges],key=lambda k: self.degree(k))
        for k in order:
            for v in sorted(self.edges[k][0]):
                yield k,v
            

    def __le__(self,right):
        for k in self.edges:
            if k not in right.edges:
                return False
            for v in self.edges[k][0]:
                if v not in right.edges[k][0]:
                    return False
            for v in self.edges[k][1]:
                if v not in right.edges[k][1]:
                    return False
        return True
 
    def __delitem__(self,item):
        if type(item)== tuple and len(item)==2:
            if item[0] in self.edges and item[1] in self.edges:
                self.edges[item[0]][0].remove(item[1])
                self.edges[item[1]][1].remove(item[0])
            else:
                raise GraphError
        elif item in self.edges:
            for k in self.edges:
                if item in self.edges[k][0]:
                    self.edges[k][0].remove(item)
                if item in self.edges[k][1]:
                    self.edges[k][1].remove(item)
                        
            del self.edges[item]
        else:
            raise GraphError

 
 
     
##############################
 
 
if __name__ == '__main__':
    #Put code here to test Graph class before doing bsc test
    

    
    #driver tests
    import driver
    driver.default_file_name = 'bscile2W22.txt'
    #Uncomment the following lines to see MORE details on exceptions
#     driver.default_show_exception=True
#     driver.default_show_exception_message=True
#     driver.default_show_traceback=True
    driver.driver()
