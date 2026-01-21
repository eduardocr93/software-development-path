import csv


countries_list = [
	{
		'name': 'Grand Theft Auto IV',
		'gender': 'Accion',
		'developer': 'Rockstar Games,',
		'ESRB_classify': 'M',
	},
	{
		'name': 'The Elder Scrolls IV: Oblivion',
		'gender': 'RPG',
		'developer': 'Bethesda,',
		'ESRB_classify': 'M',
	},
	{
		'name': 'Tony Hawks Pro Skater 2',
		'gender': 'Deportes',
		'developer': 'Activision,',
		'ESRB_classify': 'T',
	},
]

def write_csv_file(file_path, data, headers):
  with open(file_path, 'w', encoding='utf-8') as file:
    writer = csv.DictWriter(file, headers)
    writer.writeheader()
    writer.writerows(data)

write_csv_file('video_games.csv', countries_list, countries_list[0].keys())


#---------------------------------------------------

import csv

video_games_list = [
    {
        'nombre': 'Grand Theft Auto IV',
        'genero': 'Accion',
        'desarrollador': 'Rockstar Games',
        'clasificacion': 'M',
    },
    {
        'nombre': 'The Elder Scrolls IV: Oblivion',
        'genero': 'RPG',
        'desarrollador': 'Bethesda',
        'clasificacion': 'M',
    },
    {
        'nombre': "Tony Hawk's Pro Skater 2",
        'genero': 'Deportes',
        'desarrollador': 'Activision',
        'clasificacion': 'T',
    },
]

def write_csv_file(file_path, data, headers):
    with open(file_path, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, headers, delimiter='\t')
        writer.writeheader()
        writer.writerows(data)

write_csv_file('video_games2.csv', video_games_list, video_games_list[0].keys())





