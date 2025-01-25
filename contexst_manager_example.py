file = open('example.txt', 'w')
try:
    file.write('FC 25')
    file.write('FC 24')
finally:
    file.close()


with open('example_2.txt', 'w') as file:
    file.write = ('FC 25')
    file.write = ('FC 24')