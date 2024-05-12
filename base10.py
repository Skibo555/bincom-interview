import random


def generate_four_digit():
    rand_num = random.randint(1234, 5000)
    return rand_num


def convert_to_binary(random_number):
    binary = ''

    if random_number == 0:
        return "0"
    while random_number > 0:
        remainder = random_number % 2
        binary = str(remainder) + binary
        random_number //= 2
    return binary

result = convert_to_binary(generate_four_digit())
print(result)