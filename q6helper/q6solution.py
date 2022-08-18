import prompt
from goody import irange
from collections import defaultdict


# List Node class and helper functions (to set up problem)

class LN:
    def __init__(self,value,next=None):
        self.value = value
        self.next  = next

def list_to_ll(l):
    if l == []:
        return None
    front = rear = LN(l[0])
    for v in l[1:]:
        rear.next = LN(v)
        rear = rear.next
    return front

def str_ll(ll):
    answer = ''
    while ll != None:
        answer += str(ll.value)+'->'
        ll = ll.next
    return answer + 'None'



# Tree Node class and helper functions (to set up problem)

class TN:
    def __init__(self,value,left=None,right=None):
        self.value = value
        self.left  = left
        self.right = right

def list_to_tree(alist):
    if alist == None:
        return None
    else:
        return TN(alist[0],list_to_tree(alist[1]),list_to_tree(alist[2])) 
    
def str_tree(atree,indent_char ='.',indent_delta=2):
    def str_tree_1(indent,atree):
        if atree == None:
            return ''
        else:
            answer = ''
            answer += str_tree_1(indent+indent_delta,atree.right)
            answer += indent*indent_char+str(atree.value)+'\n'
            answer += str_tree_1(indent+indent_delta,atree.left)
            return answer
    return str_tree_1(0,atree) 


# Define append_ordered ITERATIVELY

def append_ordered(ll,v):
    if ll == None:
        return LN(v)
    if ll.value>=v:
        return LN(v,ll)
    front = ll
    while ll!=None:
        if ll.next==None:
            ll.next= LN(v)
            return front
        elif ll.next.value>=v:
            temp=ll.next
            ll.next = LN(v,temp)
            return front
        ll =ll.next
    return front
            
    
# Define append_ordered RECURSIVELY

def append_ordered_r(ll,v):
    if ll == None:
        return LN(v)
    if ll.value>=v:
        return LN(v,ll)
    else:
        return LN(ll.value,append_ordered_r(ll.next,v))




# Define max_depth RECURSIVELY

def max_depth(t,value): 
    def in_tree(t,value):
        if t is None:
            return False
        if t.value==value:
            return True
        else:
            return in_tree(t.left,value) or in_tree(t.right,value)
    if not(in_tree(t,value)) or type(t) is not TN:#tree dont have value or tree is none return -1
        return -1
    else:
        return max(max_depth(t.left, value)+1, max_depth(t.right, value)+1)



from tkinter import StringVar

# Define StringVar_WithHistory

class StringVar_WithHistory(StringVar):
    def __init__(self,*args):
        StringVar.__init__(self,*args)
        self.history = []
    def set(self,value):
        if value != StringVar.get(self):
            StringVar.set(self,value)
            self.history.append(value)
    def undo(self):
        if len(self.history)>1:
            self.history=self.history[:-1]
            StringVar.set(self,self.history[-1])
            
        




# OptionMenuUndo: acts like an OptionMenu, but also allows undoing the most recently
#   selected option, all the way back to the title (whose selection cannot be undone).
# It overrides the __init__ method and defines the new methods get, undo, and 
#   simulate_selections.
# It will work correctly if StringVar_WithHistory is defined correctly
from tkinter import OptionMenu
class OptionMenuUndo(OptionMenu):
    def __init__(self,parent,title,*option_tuple,**configs):
        self.result = StringVar_WithHistory()
        self.result.set(title)
        OptionMenu.__init__(self,parent,self.result,*option_tuple,**configs)

    # Get the current option  
    def get(self):                
        return self.result.get() # Call get on the StringVar_WithHistory attribute

    # Undo the most recent option
    def undo(self):
        self.result.undo()       # Call undo on the StringVar_WithHistory attribute
      
    # Simulate selecting an option (mostly for test purposes)
    def simulate_selection(self,option):
        self.result.set(option)  # Call set on the StringVar_WithHistory attribute





    
# Testing Script

if __name__ == '__main__':
    print('Testing append_ordered')
    ll = list_to_ll([])
    print('\noriginal list                = ',str_ll(ll))
    ll = append_ordered(ll,5) 
    print('resulting list (appended 5)  = ',str_ll(ll))
    
    ll = list_to_ll([5])
    print('\noriginal list                = ',str_ll(ll))
    ll = append_ordered(ll,1) 
    print('resulting list (appended 1)  = ',str_ll(ll))
    
    ll = list_to_ll([5])
    print('\noriginal list                = ',str_ll(ll))
    ll = append_ordered(ll,10) 
    print('resulting list (appended 10) = ',str_ll(ll))
    
    ll = list_to_ll([5,10])
    print('\noriginal list                = ',str_ll(ll))
    ll = append_ordered(ll,1) 
    print('resulting list (appended 1)  = ',str_ll(ll))
    
    ll = list_to_ll([5,10])
    print('\noriginal list                = ',str_ll(ll))
    ll = append_ordered(ll,7) 
    print('resulting list (appended 7)  = ',str_ll(ll))
    
    ll = list_to_ll([5,10])
    print('\noriginal list                = ',str_ll(ll))
    ll = append_ordered(ll,12) 
    print('resulting list (appended 12) = ',str_ll(ll))
    
    ll = list_to_ll([1,3,4,6,9,13,18])
    print('\noriginal list                = ',str_ll(ll))
    ll = append_ordered(ll,0) 
    print('resulting list (appended 0)  = ',str_ll(ll))
    
    ll = list_to_ll([1,3,4,6,9,13,18])
    print('\noriginal list                = ',str_ll(ll))
    ll = append_ordered(ll,2) 
    print('resulting list (appended 2)  = ',str_ll(ll))
    
    ll = list_to_ll([1,3,4,6,9,13,18])
    print('\noriginal list                = ',str_ll(ll))
    ll = append_ordered(ll,8) 
    print('resulting list (appended 8)  = ',str_ll(ll))
    
    ll = list_to_ll([1,3,4,6,9,13,18])
    print('\noriginal list                = ',str_ll(ll))
    ll = append_ordered(ll,17) 
    print('resulting list (appended 17) = ',str_ll(ll))
    
    ll = list_to_ll([1,3,4,6,9,13,18])
    print('\noriginal list                = ',str_ll(ll))
    ll = append_ordered(ll,19) 
    print('resulting list (appended 19) = ',str_ll(ll))
    
    # Put in your own tests here
    
    
    print('Testing append_ordered')
    ll = list_to_ll([])
    print('\noriginal list                = ',str_ll(ll))
    ll = append_ordered_r(ll,5) 
    print('resulting list (appended 5)  = ',str_ll(ll))
    
    ll = list_to_ll([5])
    print('\noriginal list                = ',str_ll(ll))
    ll = append_ordered_r(ll,1) 
    print('resulting list (appended 1)  = ',str_ll(ll))
    
    ll = list_to_ll([5])
    print('\noriginal list                = ',str_ll(ll))
    ll = append_ordered_r(ll,10) 
    print('resulting list (appended 10) = ',str_ll(ll))
    
    ll = list_to_ll([5,10])
    print('\noriginal list                = ',str_ll(ll))
    ll = append_ordered_r(ll,1) 
    print('resulting list (appended 1)  = ',str_ll(ll))
    
    ll = list_to_ll([5,10])
    print('\noriginal list                = ',str_ll(ll))
    ll = append_ordered_r(ll,7) 
    print('resulting list (appended 7)  = ',str_ll(ll))
    
    ll = list_to_ll([5,10])
    print('\noriginal list                = ',str_ll(ll))
    ll = append_ordered_r(ll,12) 
    print('resulting list (appended 12) = ',str_ll(ll))
    
    ll = list_to_ll([1,3,4,6,9,13,18])
    print('\noriginal list                = ',str_ll(ll))
    ll = append_ordered_r(ll,0) 
    print('resulting list (appended 0)  = ',str_ll(ll))
    
    ll = list_to_ll([1,3,4,6,9,13,18])
    print('\noriginal list                = ',str_ll(ll))
    ll = append_ordered_r(ll,2) 
    print('resulting list (appended 2)  = ',str_ll(ll))
    
    ll = list_to_ll([1,3,4,6,9,13,18])
    print('\noriginal list                = ',str_ll(ll))
    ll = append_ordered_r(ll,8) 
    print('resulting list (appended 8)  = ',str_ll(ll))
    
    ll = list_to_ll([1,3,4,6,9,13,18])
    print('\noriginal list                = ',str_ll(ll))
    ll = append_ordered_r(ll,17) 
    print('resulting list (appended 17) = ',str_ll(ll))
    
    ll = list_to_ll([1,3,4,6,9,13,18])
    print('\noriginal list                = ',str_ll(ll))
    ll = append_ordered(ll,19) 
    print('resulting list (appended 19) = ',str_ll(ll))
    
    # Put in your own tests here
    
    
    print('\n\nTesting max_depth')
    tree = list_to_tree(None)
    print('\nfor tree = \n',str_tree(tree))
    for i in [1]:
        print('max_depth(tree,'+str(i)+') = ', max_depth(tree,i))
    
    tree = list_to_tree([1, [2, None, None], [3, None, None]])
    print('\nfor tree = \n',str_tree(tree))
    for i in irange(1,3):
        print('max_depth(tree,'+str(i)+') = ', max_depth(tree,i))
    
    tree = list_to_tree([3, [2, None, [3, None, None]], [1, [3, None, None], None]])
    print('\nfor tree = \n',str_tree(tree))
    for i in irange(1,3):
        print('max_depth(tree,'+str(i)+') = ', max_depth(tree,i))
    
    tree = list_to_tree([3, [2, [3, None, [2, None, None]], [3, None, [3, None, None]]], [1, [3, [2, None, [2, None, None]], None], None]])
    print('\nfor tree = \n',str_tree(tree))
    for i in irange(1,3):
        print('max_depth(tree,'+str(i)+') = ', max_depth(tree,i))
    
    # Put in your own tests here
    
    
    print('\nTesting OptionMenuUndo')
    from tkinter import *
    print('Simulate using StringVar_WithHistory or build/test actual GUI')
    if prompt.for_bool('Simulate',default=True):
        # Needed for obscure reasons: OptionMenu must still be placed in main
        root = Tk()
        root.title('Widget Tester')
        main = Frame(root)
    
        # Construct an OptionMenuUndo object for simulation
        omu = OptionMenuUndo(main, 'Choose Option', 'option1','option2','option3')
    
        # Initially its value is 'Choose Option'
        print(omu.get(), '   should be Choose Option')
    
        # Select a new option
        omu.simulate_selection('option1')
        print(omu.get(), '         should be option1')
    
        # Select a new option
        omu.simulate_selection('option2')
        print(omu.get(), '         should be option2')
    
        # Select the same option (does nothing)
        omu.simulate_selection('option2')
        print(omu.get(), '         should still be option2')
    
        # Select a new option
        omu.simulate_selection('option3')
        print(omu.get(), '         should be option3')
    
        # Undo the last option: from 'option3' -> 'option2'
        omu.undo()
        print(omu.get(), '         should go back to option2')
    
        # Undo the last option: from 'option2' -> 'option1'
        omu.undo()
        print(omu.get(), '         should go back to option1')
    
        # Undo the last option: from 'option1' -> 'Choose Option'
        omu.undo()
        print(omu.get(), '   should go back to Choose Option')
    
        # Cannot undo the first option: does nothing
        omu.undo()
        print(omu.get(), '   should still be Choose Option')
    
    
        # Cannot undo the first option: does nothing
        omu.undo()
        print(omu.get(), '   should still be Choose Option')
    
    else: #Build/Test real widget
    
        # #OptionMenuToEntry: with title, linked_entry, and option_tuple
        # #get is an inherited pull function; put is a push function, pushing
        # #  the selected option into the linked_entry (replacing what is there)
        # 
        root = Tk()
        root.title('Widget Tester')
        main = Frame(root)
        main.pack(side=TOP,anchor=W)
    
        omu = OptionMenuUndo(main, 'Choose Option', 'option1','option2','option3')
        omu.grid(row=1,column=1)
        omu.config(width = 10)
    
        b = Button(main,text='Undo Option',command=omu.undo)
        b.grid(row=1,column=2)
    
        root.mainloop()    
    # # Put in your own tests here

   
    import driver
    driver.default_file_name = 'bscq6S22.txt'
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    print('\n\n')
    driver.driver()
    
