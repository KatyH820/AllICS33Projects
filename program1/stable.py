import prompt
import goody


# Submitter: katyh1(Huang, Katy)
# Partner  : jessieh9(He, Jessie)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming

# Use these global variables to index the list associated with each name in the dictionary.
# e.g., if men is a dictionary, men['m1'][match] is the woman who matches man 'm1', and 
# men['m1'][prefs] is the list of preference for man 'm1'.
# It would seems that this list might be better represented as a named tuple, but the
# preference list it contains is mutated, which is not allowed in a named tuple. 

match = 0   # Index 0 of list associate with name is match (str)
prefs = 1   # Index 1 of list associate with name is preferences (list of str)


def read_match_preferences(open_file : open) -> {str:[str,[str]]}:
    pref_dict = {}
    for line in open_file:
        name= line.rstrip('\n').split(';')
        pref_dict[name[0]]= [None, name[1:]]
    open_file.close()
    return pref_dict


def dict_as_str(d : {str:[str,[str]]}, key : callable=None, reverse : bool=False) -> str:
    preference = ''
    for name in sorted(d,key=key,reverse=reverse): 
        preference += f"  {name} -> {d[name]}\n"
    return preference


def who_prefer(order : [str], p1 : str, p2 : str) -> str:
    return p1 if order.index(p1) < order.index(p2) else p2


def extract_matches(men : {str:[str,[str]]}) -> {(str,str)}:
    return {(name,men[name][match]) for name in men}


def make_match(men : {str:[str,[str]]}, women : {str:[str,[str]]}, trace : bool = False) -> {(str,str)}:
    men_copy = men.copy()
    unmatched_men = set(men.keys())
    if trace:print('Women Preferences (unchanging)');print(dict_as_str(women))
    while len(unmatched_men)>0:
        if trace:print('Men Preferences (current)');print(dict_as_str(men));print(f'unmatched men = {unmatched_men}\n')
        man = unmatched_men.pop()
        woman = men_copy[man][prefs].pop(0)
        if women[woman][match] is None:
            men_copy[man][match] = woman
            women[woman][match]=man
            if trace:print(f'{man} proposes to {woman}, who is currently unmatched, accepting proposal\n')
        elif women[woman][match] is not None and who_prefer(women[woman][prefs],man,women[woman][match])==man:
            men_copy[man][match] = woman
            unmatched_men.add(women[woman][match])
            women[woman][match]=man
            if trace:print(f'{man} proposes to {woman}, who is currently matched, accepting the proposal (likes new match better)\n')
        else:
            if trace:print(f'{man} proposes to {woman}, who is currently matched, rejecting the proposal (likes current match better)\n')
            unmatched_men.add(man)
    return extract_matches(men_copy)
        
        
        
        
        
  


  
    
if __name__ == '__main__':
    # Write script here
    men_file = goody.safe_open('Specify the file name representing the preferences for men','r','invalid file')
    women_file = goody.safe_open('Specify the file name representing the preferences for women','r','invalid file')
    men = read_match_preferences(men_file)
    women = read_match_preferences(women_file)
    men_file.close()
    women_file.close()
    print('\nMen Preferences')
    print(dict_as_str(men))
    print('Women Preferences')  
    print(dict_as_str(women)) 
    tracing = prompt.for_bool('Specify choice for tracing algorithm[True]')
    print()
    matches = make_match(men,women,tracing)
    if tracing: print(f'Tracing terminated, the final matches: {matches}\n')
    print(f'The final matches: {matches}')
       
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc2.txt"
    driver.default_show_traceback = True
    driver.default_show_exception = True
    driver.default_show_exception_message = True
    driver.driver()
