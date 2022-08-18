import goody
from goody import irange
import prompt
from random import choice
from collections import defaultdict

# Submitter: katyh1(Huang, Katy)
# Partner  : jessieh9(He, Jessie)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming

# For use in read_corpus: leave unchanged in this file
def word_at_a_time(file : open):
    for line in file:
        for item in line.strip().split():
            yield item


def read_corpus(os : int, file : open) -> {(str):[str]}:
    words = word_at_a_time(file)
    result = defaultdict(list)
    pre_read = []
    while True:
        pre_read = pre_read[1:]
        try:    
            for i in irange(os+1):
                pre_read.append(next(words))
        except StopIteration:
            pass
        if len(pre_read) >os:
            value = pre_read[os if len(pre_read)-1>=os else -1]
            if value not in result[tuple(pre_read[:os])]:
                result[tuple(pre_read[:os])].append(value)
        else:
            return dict(result)



def corpus_as_str(corpus : {(str):[str]}) -> str:
    string = '';min = 10000; max= 0
    for i in sorted(corpus):
        string+= f'  {i} can be followed by any of {corpus[i]}\n'
        if len(corpus[i]) > max:max = len(corpus[i])
        elif len(corpus[i]) < min:min = len(corpus[i])
    string += f'min/max list lengths = {min}/{max}\n'
    return string


def produce_text(corpus : {(str):[str]}, start : [str], count : int) -> [str]:
    recent = start[:]
    generate = start[:]
    while len(generate)<=count+1:
        if (recent[0],recent[1]) in corpus:
            text = choice(corpus[(recent[0],recent[1])])
            generate.append(text)
            recent.append(text)
            del recent[0]
        else:
            generate.append(None)
            return generate
    return generate



if __name__ == '__main__':
    # Write script here
    os = prompt.for_int('Specify the order statistic')
    file = goody.safe_open('Specify the file name representing the text to process','r','Invalid file')
    corpus_dict = read_corpus(os, file)
    file.close()
    print('Corpus')
    print(corpus_as_str(corpus_dict))
    print(f'Specify {os} words starting the list')
    start = [prompt.for_string(f'Specify word {i}') for i in irange(os)]
    count = prompt.for_int('Specify # of words to append at the end of the started list')
    text = produce_text(corpus_dict,start,count)
    print(f'Random text = {text}')
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc5.txt"
    driver.default_show_traceback = True
    driver.default_show_exception = True
    driver.default_show_exception_message = True
    driver.driver()
