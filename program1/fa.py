import goody

# Submitter: katyh1(Huang, Katy)
# Partner  : jessieh9(He, Jessie)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming

def read_fa(file : open) -> {str:{str:str}}:
    result = {}
    for line in file:
        comp=line.rstrip().split(';')
        name = [x for x in comp[1:] if comp.index(x)%2==0];state = [x for x in comp[1:] if comp.index(x)%2==1]
        result[comp[0]]= dict(zip(state,name))
    return result


def fa_as_str(fa : {str:{str:str}}) -> str:
    result = ''
    for name in sorted(fa): 
        result += f"  {name} transitions: {sorted((state,fa[name][state]) for state in fa[name])}\n"
    return result

    
def process(fa : {str:{str:str}}, state : str, inputs : [str]) -> [None]:
    lst = [state]
    for x in inputs:
        if x in fa[state]:
            lst.append((x,fa[state][x]))    
            state = fa[state][x]
        else:
            lst.append((x,None))
            break
    return lst


def interpret(fa_result : [None]) -> str:
    result = f'Start state = {fa_result[0]}\n'
    for i in fa_result[1:]:
        if i[1] == None:
            result += f'  Input = {i[0]}; illegal input: simulation terminated\n'
        else:
            result += f'  Input = {i[0]}; new state = {i[1]}\n'
    result += f'Stop state = {fa_result[-1][1]}\n'
    return result



if __name__ == '__main__':
    # Write script here
    file_name = goody.safe_open('Specify the file name representing the Finite Automaton','r','invalid file');fa_dict = read_fa(file_name)
    file_name.close()
    print('\nSpecified details of this Finite Automaton');print(fa_as_str(fa_dict))
    multiple_start_file = goody.safe_open('Specify the file name representing multiple start-states and their inputs','r','invalid file')
    print()
    for line in multiple_start_file:
        print('Computed FA trace from its start-state')
        comp = line.rstrip().split(';');start = comp[0];result = process(fa_dict,start,comp[1:])      
        print(interpret(result))
    multiple_start_file.close()
        
    
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc3.txt"
    driver.default_show_traceback = True
    driver.default_show_exception = True
    driver.default_show_exception_message = True
    driver.driver()
