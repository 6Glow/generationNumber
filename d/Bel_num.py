import random


def generate_phone_number():
    operators = ["29", "25", "33", "44"]
    operator_code = random.choice(operators)
    region_code = random.randint(1, 9)
    unique_number = random.randint(100000, 999999)

    phone_number = f"+375 {operator_code} {region_code}{unique_number}"
    return phone_number


# Пример использования функции
number = generate_phone_number()
print(number)