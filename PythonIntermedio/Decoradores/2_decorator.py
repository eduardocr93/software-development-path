def only_numbers(func):

    def wrapper(*args, **kwargs):

        for value in args:
            if not isinstance(value, (int, float)):
                raise TypeError("All parameters must be numbers")

        for value in kwargs.values():
            if not isinstance(value, (int, float)):
                raise TypeError("All parameters must be numbers")

        return func(*args, **kwargs)

    return wrapper



try:
    @only_numbers
    def suma(a, b):
        return a + b

    print(suma(3, 5))
    print(suma(3, "5"))

except TypeError as e:
    print(f"Error: {e}")