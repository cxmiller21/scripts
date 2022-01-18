import csv
import local_module

print(local_module.myModule('world!'))

def count_string(list):
    return len(list)

def basic_rev(string):
    return string[::-1]

def other_rev(string):
    new_string = []
    index = count_string(string)
    while index:
        index -= 1
        new_string.append(string[index])
    return ''.join(new_string)

string = 'Hello World'
print(basic_rev(string))
print(other_rev(string))

with open('demo.txt', 'w') as f:
    f.write(f'{string}-something else')
    
# CSV's
headers = ['taco', 'hotdog', 'hamburger']
data = ['y', 'n', 'y']

with open('taco.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerow(data)
