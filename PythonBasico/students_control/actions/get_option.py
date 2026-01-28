def get_option(min_value=None, max_value=None):
    try:
        option = int(input("Select option: "))
        if min_value and max_value:
            if min_value <= option <= max_value:
                return option
            else:
                print("Option out of range.")
                return None
        return option
    except ValueError:
        print("Select a valid number.")
        return None
