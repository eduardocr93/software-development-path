import json

file_name = r"C:\Users\Eduardo\Desktop\Lyfter\Python\pokemones.json"

def read_pokemons():
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_pokemons(pokemons):
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(pokemons, f, indent=4, ensure_ascii=False)

def get_pokemon_data():
    name = input("Nombre del Pokémon: ")
    pokemon_type = input("Tipo del Pokémon: ")

    print("Introduce las estadísticas base:")
    hp = int(input("HP: "))
    attack = int(input("Attack: "))
    defense = int(input("Defense: "))
    sp_attack = int(input("Sp. Attack: "))
    sp_defense = int(input("Sp. Defense: "))
    speed = int(input("Speed: "))

    return name, pokemon_type, hp, attack, defense, sp_attack, sp_defense, speed

def create_pokemon(name, pokemon_type, hp, attack, defense, sp_attack, sp_defense, speed):
    return {
        "name": {"english": name},
        "type": [pokemon_type],
        "base": {
            "HP": hp,
            "Attack": attack,
            "Defense": defense,
            "Sp. Attack": sp_attack,
            "Sp. Defense": sp_defense,
            "Speed": speed
        }
    }

def add_pokemon():
    name, pokemon_type, hp, attack, defense, sp_attack, sp_defense, speed = get_pokemon_data()

    new_pokemon = create_pokemon(name, pokemon_type, hp, attack, defense, sp_attack, sp_defense, speed)

    pokemons = read_pokemons()
    pokemons.append(new_pokemon)

    save_pokemons(pokemons)

    print(f" Pokémon {name} agregado correctamente.")

if __name__ == "__main__":
    add_pokemon()