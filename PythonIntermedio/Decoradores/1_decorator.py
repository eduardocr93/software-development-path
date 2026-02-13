def print_params_and_return(func):

    def wrapper(*args, **kwargs):
        
        print("=== PARAMS ===")
        print("args:", args)      
        print("kwargs:", kwargs)    

        result = func(*args, **kwargs)

        print("=== RETURN ===")
        print(result)

        return result

    return wrapper


@print_params_and_return
def saludar(nombre, mensaje="Hola"):
    return f"{mensaje}, {nombre}!"

saludar("Eduardo", mensaje="Qué tal")
saludar("Eduardo")