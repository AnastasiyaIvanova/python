a = 0
while a < 101:
    if((a % 3 == 0) and (a % 5 == 0)):
        print('FizzBuzz')
    elif(a % 3 == 0):
        print('Fizz')
    elif(a % 5 == 0):
        print('Buzz')
    else: print(a)
    a = a + 1

d =  {'key1': 'value1', 'key2': 'value2'}
d = {v:k for k, v in d.items()}
print(d)

def f(l):
    n = []
    for i in l:
        if i not in n:
            n.append(i)
    return n
print (f([1, 1, 2, 3, 5, 4, 5, 5, 6]))

