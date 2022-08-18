'''
Created on Apr 16, 2022

@author: katyhuang
'''
import re
def contract(string):
    return re.sub(r'o+','o',string)

print(contract('It is a goooooooal! A gooal'))

def grep(pat_str,file_name):
    file= open(file_name)
    return [(file_name,num+1,line.strip()) for num,line in enumerate(file) if re.match(pat_str, line)]
    file.close()

print(grep('^home','huck.txt'))

m = re.search(r'(?P<fname>\w+) (?P<lname>\w+)','Katy Huang')
print(m.groupdict())
