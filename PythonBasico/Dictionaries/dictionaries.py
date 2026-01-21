hotel = {
    "name": "Paradise Hotel",
    "star_rating": 5,
    "rooms": [
        {
            "number": 101,
            "floor": 1,
            "price_per_night": 80.0
        },
        {
            "number": 202,
            "floor": 2,
            "price_per_night": 120.0
        },
        {
            "number": 303,
            "floor": 3,
            "price_per_night": 150.0
        }
    ]
}
print (hotel)

#---------------------------------------------------------

list_a = ["first_name", "last_name", "role", "country"]
list_b = ["Eduardo", "Luna", "Software Engineer", "Costa Rica"]
lists_information = {}
for i in range(len(list_a)):
    lists_information[list_a[i]] = list_b[i]
print(lists_information)

#---------------------------------------------------------
list_of_keys = ["access_level", "age"]
employee = {"name": "John",
            "email": "john@ecorp.com",
            "access_level": 5,
            "age": 28}
deleted_items = {}
for key in list_of_keys:
    deleted_items[key]=employee.pop(key)
print(employee)
print(deleted_items)
