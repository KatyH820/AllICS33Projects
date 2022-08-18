import goody
from collections import defaultdict

# Submitter: katyh1(Huang, Katy)
# Partner  : jessieh9(He, Jessie)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming

def read_ndfa(file : open) -> {str:{str:{str}}}:
    outer_dict = dict()
    for lines in file:
        line = lines.rstrip().split(';')
        inner_tuples = zip([key for key in line[1:] if line.index(key) % 2 == 1], [state for state in line[1:] if line.index(state) %2 == 0])        
        inner_dict = defaultdict(set)
        for key, value in inner_tuples:
            inner_dict[key].add(value)
        outer_dict[line[0]] =  inner_dict
    return outer_dict 


def ndfa_as_str(ndfa : {str:{str:{str}}}) -> str:
    string = ''
    for state in sorted(ndfa):
        string += f'  {state} transitions: {sorted([(transition, sorted(ndfa[state][transition])) for transition in ndfa[state]])}\n'
    return string

       
def process(ndfa : {str:{str:{str}}}, state : str, inputs : [str]) -> [None]:
    result = [state]
    state = [state]
    for uinput in inputs:
        state_set = set()
        for x in state:
            if uinput in ndfa[x]:             
                state_set.update(ndfa[x][uinput])
        result.append((uinput,state_set))
        if state_set == set() :
            return result
        state = state_set
    return result


def interpret(result : [None]) -> str:
    string=f"Start state = {result[0]}\n"
    for transition in result[1:]:
        string+=f"  Input = {transition[0]}; new possible states = {sorted(transition[1])}\n"
    string+=f'Stop state(s) = {sorted(transition[1])}\n'
    return string





if __name__ == '__main__':
    # Write script here
    file = goody.safe_open('Specify the file name representing the Non-Deterministic Finite Automaton', 'r', 'Invalid file')
    ndfa_dict = read_ndfa(file)
    file.close()
    ndfa_str = ndfa_as_str(ndfa_dict)
    print('\nSpecified details of this Non-Deterministic Finite Automaton')
    print(ndfa_str)
    input_file = goody.safe_open('Specify the file name representing multiple start-states and their inputs','r','Invalid file')
    print()
    for line in input_file:
        print('Computed FA trace from its start-state')
        comp = line.rstrip().split(';');start = comp[0];result = process(ndfa_dict,start,comp[1:])      
        print(interpret(result))
    input_file.close()
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc4.txt"
    driver.default_show_traceback = True
    driver.default_show_exception = True
    driver.default_show_exception_message = True
    driver.driver()
