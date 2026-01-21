import csv

def save_games_csv(filename):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)  
        writer.writerow(["name", "genre", "developer", "esrb_rating"])

        number = int(input("Cuantos video juegos desea ingresar?"))

        for i in range(number):
            print(f"\nGame {i+1}:")
            name = input("Name: ")
            genre = input("Genre: ")
            developer = input("Developer: ")
            esrb_rating = input("ESRB Rating: ")

            writer.writerow([name, genre, developer, esrb_rating])

    print(f"\nFile '{filename}' Creado con Exito")

save_games_csv("video_games.csv")



#-----------------------------------------------------------------------

import csv

def save_games_csv(filename):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter="\t")
        writer.writerow(["name", "genre", "developer", "esrb_rating"])

        number = int(input("Cuantos video juegos desea ingresar?"))

        for i in range(number):
            print(f"\nGame {i+1}:")
            name = input("Name: ")
            genre = input("Genre: ")
            developer = input("Developer: ")
            esrb_rating = input("ESRB Rating: ")

            writer.writerow([name, genre, developer, esrb_rating])

    print(f"\nFile '{filename}' Creado con Exito")

save_games_csv("video_games.csv")

