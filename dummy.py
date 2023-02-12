def decorator(argument):
    def real_decorator(function):
        def wrapper(*args):
            for arg in args:
                assert type(arg)==int,f'{arg} is not an interger'
            result = function(*args)
            result = result + argument
            return result
        return wrapper
    return real_decorator


@decorator(2)
def adder(*args):
    print(args)
    sum=0
    for i in args:
        sum+=i
    return sum


print(adder(3,4))