import prompt                          # for driver, which prompts user
from collections import defaultdict    # use if you want (see problem descriptions)

# You might use the following abbreviations (or their full names)
#   for the various parts of the Warehouse database

# i    : as inventory (how many products are available)
# p    : as product
# w    : as warehouse


def read_db(openfile : open)  -> {str:{str:int}}:
    db = defaultdict(dict)
    for line in openfile:
        linelst = line.strip().split(':')
        item = linelst[0]
        for i in range(1,len(linelst),2):
            db[linelst[i]][item]=int(linelst[i+1])
    return db


        
def inventory(db : {str:{str:int}})  -> [(str,int)]: 
    result = defaultdict(int)
    for city in db:
        for item in db[city]:
            result[item]+=db[city][item]
    return sorted(result.items(),key = lambda x: (-x[1], x[0]))



def resupply(db : {str:{str:int}},  must_have : int)  -> {str: {(str,int)}}:  
    supply = defaultdict(set)
    for city in db:
        for item in db[city]:
            if  db[city][item] < must_have:
                supply[item].add((city,must_have-db[city][item]))
    return supply

            
def update_purchases(db : {str:{str:int}},  purchases : [(str,str)] )  -> {(str,str)}:
    fail = set()
    for purchase in purchases:
        place = purchase[0]
        item = purchase[1]
        if place in db and item in db[place] and db[place][item]>0:
            db[place][item]-=1
        else:
            fail.add(purchase)
    return fail
    



      
def product_locations(db : {str:{str:int}})  -> [(str,[(str,int)])]:  
    result = defaultdict(list)
    for city in db:
        for item in db[city]:
            result[item].append((city,db[city][item]))
    return sorted(result.items())


def unique_supplier(db : {str:{str:int}})  -> {str:{str}}:
    items = [item for city in db for item in db[city]]
    result = defaultdict(set)
    for i in items:
        if items.count(i) ==1:
            for city in db:
                if i in db[city]:
                    result[city].add(i)
    return result


 
if __name__ == '__main__':
    # You can add any of your own specific testing code here
    # You can comment-out tests after your code passes them (but don't change your code!)
     
    # checks whether answer is correct, printing appropriate information
    # Note that dict/defaultdict will compare == if they have the same keys and
    #   associated values, regardless of the fact that they print differently
    def check (answer, correct):
        if (answer == correct):
            print ('    CORRECT')
        else:
            print ('    INCORRECT')
            print ('      was       =',answer)
            print ('      should be =',correct)
        print()
 
  
    # These tests are similar to those that the driver will execute for batch self-checks
    # To run a test, enter True (or just press enter); to skip a test, enter False 
         
    if prompt.for_bool('Test read_db?', True): 
        db = 'db1.txt'
        answer = read_db(open(db))
        print('  db =',db,'\n  read_db =',answer)
        check(answer, {'Irvine':  {'brush': 3,    'comb': 2,    'wallet': 2},
                       'Newport': {'comb': 1,     'stapler': 0},
                       'Tustin' : {'keychain': 3, 'pencil': 4,  'wallet': 3}})


        db = 'db2.txt'
        answer = read_db(open(db))
        print('  db =',db,'\n  read_db =',answer)
        check(answer, {'Irvine':  {'brush': 4, 'comb': 2, 'keychain': 6, 'lipgloss': 3, 'wallet': 3},
                       'Newport': {'brush': 1, 'comb': 5, 'keychain': 3, 'lipgloss': 6, 'wallet': 1},
                       'Tustin':  {'brush': 1, 'comb': 3, 'keychain': 2, 'lipgloss': 4, 'wallet': 2}})

    ##################################################
              

    if prompt.for_bool('Test inventory?', True): 
        db = {'Irvine':  {'brush': 3,    'comb': 2,    'wallet': 2},
              'Newport': {'comb': 1,     'stapler': 0},
              'Tustin' : {'keychain': 3, 'pencil': 4,  'wallet': 3}}

        answer = inventory(db)
        print('  db =',db,'\n  inventory =',answer)
        check(answer, [('wallet', 5), ('pencil', 4), ('brush', 3), ('comb', 3), ('keychain', 3), ('stapler', 0)])

 
        db = {'Irvine':  {'brush': 4, 'comb': 2, 'keychain': 6, 'lipgloss': 3, 'wallet': 3},
              'Newport': {'brush': 1, 'comb': 5, 'keychain': 3, 'lipgloss': 6, 'wallet': 1},
              'Tustin':  {'brush': 1, 'comb': 3, 'keychain': 2, 'lipgloss': 4, 'wallet': 2}}

        answer = inventory(db)
        print('  db =',db,'\n  inventory =',answer)
        check(answer, [('lipgloss', 13), ('keychain', 11), ('comb', 10), ('brush', 6), ('wallet', 6)])

 
    ##################################################
              

    if prompt.for_bool('Test resupply?', True): 
        db = {'Irvine':  {'brush': 3,    'comb': 2,    'wallet': 2},
              'Newport': {'comb': 1,     'stapler': 0},
              'Tustin' : {'keychain': 3, 'pencil': 4,  'wallet': 3}}

        answer = resupply(db,3)
        print('  db =',db,'\n  resupply =',answer)
        check(answer, {'comb': {('Newport', 2), ('Irvine', 1)}, 'wallet': {('Irvine', 1)}, 'stapler': {('Newport', 3)}})

 
        db = {'Irvine':  {'brush': 4, 'comb': 2, 'keychain': 6, 'lipgloss': 3, 'wallet': 3},
              'Newport': {'brush': 1, 'comb': 5, 'keychain': 3, 'lipgloss': 6, 'wallet': 1},
              'Tustin':  {'brush': 1, 'comb': 3, 'keychain': 2, 'lipgloss': 4, 'wallet': 2}}

        answer = resupply(db,4)
        print('  db =',db,'\n  resupply =',answer)
        check(answer, {'comb': {('Tustin', 1), ('Irvine', 2)}, 'lipgloss': {('Irvine', 1)}, 'wallet': {('Tustin', 2), ('Newport', 3), ('Irvine', 1)}, 'brush': {('Tustin', 3), ('Newport', 3)}, 'keychain': {('Tustin', 2), ('Newport', 1)}})

 
    ##################################################
    
         
    if prompt.for_bool('Test update_purchases?', True): 
        db = {'Irvine':  {'brush': 3,    'comb': 2,    'wallet': 2},
              'Newport': {'comb': 1,     'stapler': 0},
              'Tustin' : {'keychain': 3, 'pencil': 4,  'wallet': 3}}
        purchases = [('Irvine', 'brush'), ('Newport','comb'), ('Tustin', 'car'), ('Newport', 'comb')]

        answer = update_purchases(db,purchases)
        print('  db =',db,'\n  update_purchases =',answer)
        check(answer, {('Tustin', 'car'), ('Newport', 'comb')})
        print('  db mutated =',db)
        check(db, {'Irvine':  {'brush': 2,    'comb': 2,    'wallet': 2},
                   'Newport': {'comb': 0,     'stapler': 0},
                   'Tustin' : {'keychain': 3, 'pencil': 4,  'wallet': 3}})

        
        db = {'Irvine':  {'brush': 4, 'comb': 2, 'keychain': 6, 'lipgloss': 3, 'wallet': 3},
              'Newport': {'brush': 1, 'comb': 5, 'keychain': 3, 'lipgloss': 6, 'wallet': 1},
              'Tustin':  {'brush': 1, 'comb': 3, 'keychain': 2, 'lipgloss': 4, 'wallet': 2}}
        purchases = [('Santa-Ana','brush'), ('Tustin', 'brush'), ('Newport','keychain'), ('Newport', 'food'), ('Tustin', 'brush')]

        answer = update_purchases(db,purchases)
        print('  db =',db,'\n  update_purchases =',answer)
        check(answer, {('Newport', 'food'), ('Santa-Ana','brush'),('Tustin', 'brush')})
        print('  db mutated =',db)
        check(db, {'Irvine':  {'brush': 4, 'comb': 2, 'keychain': 6, 'lipgloss': 3, 'wallet': 3},
                   'Newport': {'brush': 1, 'comb': 5, 'keychain': 2, 'lipgloss': 6, 'wallet': 1},
                   'Tustin':  {'brush': 0, 'comb': 3, 'keychain': 2, 'lipgloss': 4, 'wallet': 2}})

        
    ##################################################
   
         
    if prompt.for_bool('Test product_locations?', True): 
        db = {'Irvine':  {'brush': 3,    'comb': 2,    'wallet': 2},
              'Newport': {'comb': 1,     'stapler': 0},
              'Tustin' : {'keychain': 3, 'pencil': 4,  'wallet': 3}}


        answer = product_locations(db)
        print('  db =',db,'\n  product_locations =',answer)
        check(answer, [('brush', [('Irvine', 3)]),
                       ('comb', [('Irvine', 2), ('Newport', 1)]),
                       ('keychain', [('Tustin', 3)]),
                       ('pencil', [('Tustin', 4)]),
                       ('stapler', [('Newport', 0)]),
                       ('wallet', [('Irvine', 2), ('Tustin', 3)])])
 
 
        db = {'Irvine':  {'brush': 4, 'comb': 2, 'keychain': 6, 'lipgloss': 3, 'wallet': 3},
              'Newport': {'brush': 1, 'comb': 5, 'keychain': 3, 'lipgloss': 6, 'wallet': 1},
              'Tustin':  {'brush': 1, 'comb': 3, 'keychain': 2, 'lipgloss': 4, 'wallet': 2}}


        answer = product_locations(db)
        print('  db =',db,'\n  product_locations =',answer)
        check(answer,  [('brush', [('Irvine', 4), ('Newport', 1), ('Tustin', 1)]),
                        ('comb', [('Irvine', 2), ('Newport', 5), ('Tustin', 3)]),
                        ('keychain', [('Irvine', 6), ('Newport', 3), ('Tustin', 2)]),
                        ('lipgloss', [('Irvine', 3), ('Newport', 6), ('Tustin', 4)]),
                        ('wallet', [('Irvine', 3), ('Newport', 1), ('Tustin', 2)])])
 
 
    ##################################################
              

    if prompt.for_bool('Test unique_supplier?', True): 
        db = {'Irvine':  {'brush': 3,    'comb': 2,    'wallet': 2},
              'Newport': {'comb': 1,     'stapler': 0},
              'Tustin' : {'keychain': 3, 'pencil': 4,  'wallet': 3}}
        answer = unique_supplier(db)
        print('  db =',db,'\n  unique_supplier =',answer)
        check(answer, {'Irvine': {'brush'}, 'Newport': {'stapler'}, 'Tustin': {'pencil', 'keychain'}})

        
        db = {'Irvine':  {'brush': 4, 'comb': 2, 'keychain': 6,                'wallet': 3},
              'Newport': {            'comb': 5, 'keychain': 3, 'lipgloss': 6, 'wallet': 1},
              'Tustin':  {            'comb': 3, 'keychain': 2,                'wallet': 2}}


        answer = unique_supplier(db)
        print('  db =',db,'\n  unique_supplier =',answer)
        check(answer, {'Irvine':{'brush'}, 'Newport': {'lipgloss'}})
 
 
 
    ##################################################
