# I can only solve this with a recursive function

def fib_sequence(n):
    if n <= 1:
        return n
    else:
        return fib_sequence(n-1) + fib_sequence(n-2)

for numbers in range(50):
    print(fib_sequence(numbers))