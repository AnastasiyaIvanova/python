# декоратор подсчитывает количество вызовов ф-ии
count = 0
def counter(func):

    def wrapper(*args):
        global count
        count += 1
        res = func(*args)
        print ("{0} была вызвана: {1}x".format(func.__name__, count))
        return res
    count = 0
    return wrapper

@counter
def read(*nums):
    res = 0
    for i in nums:
        res += i
    return res
 
print(read(1,3,4,2,4))
print(read(7,2,10))