from datetime import date

class User():
    def __init__(self, date_of_birth: date):
        self.date_of_birth = date_of_birth

    @property
    def age(self):
        today = date.today()
        years = today.year - self.date_of_birth.year

        if(today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
            years-=1

        return years
    

def adult_only(func):
    def wrapper(user):
        if not isinstance(user, User):
            raise TypeError("First parameter must be a User")

        if user.age < 18:
            raise ValueError("User is not an adult (must be 18+).")

        return func(user)

    return wrapper

@adult_only
def enter_club(user: User):
    return f" Welcome! You are {user.age} years old."

try:
    adult = User(date(1993, 5, 5))
    minor = User(date(2010, 5, 5))

    print(enter_club(adult))
    #print(enter_club(minor))
    
except ValueError as e:
    print(f"Error: {e}")