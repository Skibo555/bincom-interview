import random
# user_input = input("Please, enter a number you want to search. e.g 3, 5 10 ")

def recursive_search():
    user_input = int(input("Please, enter a number you want to search. e.g 3, 5 10 "))
    list_to_search = [random.randrange(0, 10) for _ in range(10)]
    print(list_to_search)
    if user_input in list_to_search:
        return "You got it right!"
    else:
        print("Have another try!")
        return recursive_search()

print(recursive_search())