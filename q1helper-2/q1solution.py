from collections import defaultdict

def solve_root(f : callable, error : float) -> callable:
    if error <= 0:
        raise AssertionError('Error should be a positive value')
    def find_root(negf:int|float,posf:int|float):
        setattr(find_root, 'iterations', 0)
        if f(posf)<0 or f(negf)>0:
            raise AssertionError('f(posf) must be positive and f(negf) must be negative')
        while (n:=abs(negf-posf))>error:
            midpoint=(negf+posf)/2
            if f(midpoint) < 0:
                negf = (negf+posf)/2
            else:
                posf = (negf+posf)/2
            find_root.iterations+=1    
        return (negf+posf)/2    
    return find_root



def by_diversity(db : {int:{str:int}}) -> [(int,int)]:
    return sorted([(k,len(db[k])) for k in db],key= lambda x: (-x[1],x[0]))


def by_size(db : {int:{str:int}}) -> [int]:
    return sorted([k for k in db],key= lambda x: -sum(db[x].values()))



def by_party(db : {int:{str:int}}) -> [str]:
    return sorted({k2 for k in db for k2 in db[k]},key=lambda y: (-sum([db[k][y] for k in db if y in db[k]]),y))

def registration_by_state(db : {int:{str:int}}, state_zips : {str:{int}}) -> {str:{str:int}}:
    result = defaultdict(dict)
    sum_vote = lambda x,y: sum([db[k][x] for k in y if x in db[k]])
    for state in state_zips:
        for code in state_zips[state]:
            for party in db[code]:
                result[state][party]=sum_vote(party,state_zips[state])
    return result
    # state_info = defaultdict(dict)
    # for state in state_zips:
    #     vote_sum = lambda k:sum(db[x][k] for x in state_zips[state] if k in db[x])
    #     keys = [k2 for k in db for k2 in db[k]]
    #     for key in set(keys):
    #         if vote_sum(key) > 0:state_info[state][key] = vote_sum(key)
    # return dict(state_info)
    #




if __name__ == '__main__':
    # This code is useful for debugging your functions, especially
    #   when they raise exceptions: better than using driver.driver().
    # Feel free to add more tests (including tests showing in the bsc.txt file)
    # Use the driver.driver() code only after you have removed any bugs
    #   uncovered by these test cases.
    import math
    print('\nTesting solve_root')
    def f(x):
        return 3*x**4 + 3*x**3 - 1 
    rooter = solve_root(f, .0001)
    r = rooter(0,1)
    print(f'root 1 is approximately {r} where f({r}) = {f(r)} using {rooter.iterations} iterations')
    r = rooter(-1,-2)
    print(f'root 2 is approximately {r} where f({r}) = {f(r)} using {rooter.iterations} iterations')

    def f(x):
        return 23*math.sqrt(x) - (10*math.log2(x)**2+1000)
    rooter = solve_root(f, .001)
    r = rooter(10000,20000)
    print(f'root is approximately {r} where f({r}) = {f(r)} using {rooter.iterations} iterations')


    print('\nTesting by_diversity')
    db1 = {1: {'d': 15, 'i': 15,          'r': 15},
           2: {'d': 12,                   'r':  8},
           3: {'d': 10, 'i': 30, 'l': 20, 'r': 22},
           4: {'d': 30, 'l': 20,          'r': 30},
           5: {'i': 15, 'l': 15,          'r': 15}}
    print(by_diversity(db1))
    db2 = {1000: {'d': 50, 'i': 27,          'r': 18, 'x': 46},
           2000: {'d': 32,                   'r': 58},
           3000: {'d': 20, 'i': 30, 'l': 20, 'r': 22},
           4000: {'d': 40, 'i': 20, 'l': 40, 'r': 39, 'x': 46},
           5000: {'d': 20, 'i': 30, 'l': 20,          'x': 15},
           6000: {         'i': 30,                   'x': 46},
           7000: {                  'l': 20                  },
           8000: {         'i': 15, 'l': 15, 'r': 15}}
    print(by_diversity(db2))
    
    
    print('\nTesting by_size')
    db1 = {1: {'d': 15, 'i': 15,          'r': 15},
           2: {'d': 12,                   'r':  8},
           3: {'d': 10, 'i': 30, 'l': 20, 'r': 22},
           4: {'d': 30, 'l': 20,          'r': 30},
           5: {'i': 15, 'l': 15,          'r': 15}}
    print(by_size(db1))
    db2 = {1000: {'d': 50, 'i': 27,          'r': 18, 'x': 46},
           2000: {'d': 32,                   'r': 58},
           3000: {'d': 20, 'i': 30, 'l': 20, 'r': 22},
           4000: {'d': 40, 'i': 20, 'l': 40, 'r': 39, 'x': 46},
           5000: {'d': 20, 'i': 30, 'l': 20,          'x': 15},
           6000: {         'i': 30,                   'x': 46},
           7000: {                  'l': 20,                 },
           8000: {         'i': 15, 'l': 15, 'r': 15}}
    print(by_size(db2))


    print('\nTesting by_party')
    db1 = {1: {'d': 15, 'i': 15,          'r': 15},
           2: {'d': 12,                   'r':  8},
           3: {'d': 10, 'i': 30, 'l': 20, 'r': 22},
           4: {'d': 30, 'l': 20,          'r': 30},
           5: {'i': 15, 'l': 15,          'r': 15}}
    print(by_party(db1))
    db2 = {1000: {'d': 50, 'i': 27,          'r': 18, 'x': 46},
           2000: {'d': 32,                   'r': 58},
           3000: {'d': 20, 'i': 30, 'l': 20, 'r': 22},
           4000: {'d': 40, 'i': 20, 'l': 40, 'r': 39, 'x': 46},
           5000: {'d': 20, 'i': 30, 'l': 20,          'x': 15},
           6000: {         'i': 30,                   'x': 46},
           7000: {                  'l': 20,                 },
           8000: {         'i': 15, 'l': 15, 'r': 15}}
    print(by_party(db2))
    
    
    print('\nTesting registration_by_state')
    db1 = {1: {'d': 15, 'i': 15, 'r': 15}, 2: {'d': 12, 'r':  8}, 3: {'d': 10, 'i': 30, 'l': 20, 'r': 22}, 4: {'d': 30, 'l': 20, 'r': 30}, 5: {'i': 15, 'l': 15, 'r': 15}}
    print(registration_by_state(db1,{'CA': {1,3}, 'WA': {2,4,5}}))
    db2 = {1000: {'d': 50, 'i': 27,          'r': 18, 'x': 46},
           2000: {'d': 32,                   'r': 58},
           3000: {'d': 20, 'i': 30, 'l': 20, 'r': 22},
           4000: {'d': 40, 'i': 20, 'l': 40, 'r': 39, 'x': 46},
           5000: {'d': 20, 'i': 30, 'l': 20,          'x': 15},
           6000: {         'i': 30,                   'x': 46},
           7000: {                  'l': 20,                 },
           8000: {         'i': 15, 'l': 15, 'r': 15}}
    print(registration_by_state(db2,{'CA' : {1000,3000,7000}, 'WA': {2000,4000,5000,8000}, 'OR' : {6000}, 'NV' : {}}))


    
    print('\ndriver testing with batch_self_check:')
    import driver
    driver.default_file_name = "bscq1S22.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()           

