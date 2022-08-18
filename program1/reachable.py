import goody
import prompt
from collections import defaultdict

# Submitter: katyh1(Huang, Katy)
# Partner  : jessieh9(He, Jessie)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming

def read_graph(file : open) -> {str:{str}}:
    line_list = sorted([line.rstrip('\n') for line in file]);file.close() #container of file lines
    graph_dict = defaultdict(set)
    for line in line_list:
        graph_dict[line[0]].add(line[2]) #adding entries to the dictionary
    return graph_dict
        
        
        
def graph_as_str(graph : {str:{str}}) -> str:
    graphs =''
    for node in sorted(graph): 
        graphs += f"  {node} -> {sorted(list(graph[node]))}\n"
    return graphs

        
def reachable(graph : {str:{str}}, start : str, trace : bool = False) -> {str}:
    nodes_reach = set(); exploring = [start]
    while len(exploring)>0:
        if trace: print(f'reached set    = {nodes_reach}\n' f'exploring list = {exploring}')
        move_node =exploring.pop(0);nodes_reach.add(move_node)
        if trace:print(f'moving node {move_node} from the exploring list into the reached set')
        if graph.get(move_node) != None:exploring.extend([node for node in graph.get(move_node) if node not in nodes_reach])                   
        if  graph.get(move_node) != None and trace: print(f'after adding all nodes reachable directly from a but not already in reached, exploring = {exploring}\n');previous_node=move_node
        elif trace: print(f'after adding all nodes reachable directly from a but not already in reached, exploring = {exploring}\n')
    return nodes_reach



if __name__ == '__main__':
    # Write script here
    graph_file = goody.safe_open('Specify the file name representing the graph','r','invalid file')
    graph = read_graph(graph_file)
    graph_file.close()
    print('\nGraph: str (one source node) -> [str] (sorted list of destination nodes)')
    print(graph_as_str(graph))
    while start_node:= prompt.for_string('Specify one start node (or terminate)'):
        if start_node!= 'terminate' and start_node in graph:tracing = prompt.for_bool('Specify choice for tracing algorithm[True]'); print(f'From the start node a, reachable nodes = {reachable(graph,start_node,tracing)}\n')          
        elif start_node not in graph:
            if start_node == 'terminate': break
            else: print(f'  Entry Error: {start_node};  Illegal: not a source node\n  Please enter a legal String\n')

    print()
    import driver
    driver.default_file_name = "bsc1.txt"
    driver.default_show_traceback = True
    driver.default_show_exception = True
    driver.default_show_exception_message = True
    driver.driver()
