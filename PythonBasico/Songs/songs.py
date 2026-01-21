import os

def read_songs(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            songs = f.readlines()
        return [s.strip() for s in songs]
    except FileNotFoundError:
        print("Archivo no existe.")
        return []
    except Exception as e:
        print("Error:", e)
        return []


def sort_songs(songs):
    return sorted(songs)


def save_songs(file_path, songs):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            for s in songs:
                f.write(s + "\n")
        print(f"Canciones ordenadas y guardadas en: {file_path}")
    except Exception as e:
        print("Error al guardar el archivo:", e)


def main():
    input_path = r"C:\Users\Eduardo\Desktop\Lyfter\Python\canciones.txt"
    output_path = r"C:\Users\Eduardo\Desktop\Lyfter\Python\canciones_ordenadas.txt"

    songs = read_songs(input_path)
    if not songs:
        return

    sorted_songs = sort_songs(songs)

    save_songs(output_path, sorted_songs)


if __name__ == "__main__":
    main()
