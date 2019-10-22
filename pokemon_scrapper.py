from requests import get
from bs4 import BeautifulSoup
from pprint import pprint
import csv
import sqlite3


pokemon_data = []
pokemon_type=[]
pokemon_weakness=[]


conn = sqlite3.connect('pokemon.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS pokemon
             (Pokemon text, Serial integer, Type text, Weakness text, Description text)''')


for p in range(1,803):
    url = get('https://www.pokemon.com/us/pokedex/'+ str(p))
    if url.status_code == 200:
        #print("Connected",url.url)
        source = BeautifulSoup(url.text, "lxml")

        
        pokemon = source.find('div', class_='pokedex-pokemon-pagination-title').text.split()[0]
        print(pokemon,'\n')
        
        
        pokemon_id = source.find('div', class_='pokedex-pokemon-pagination-title').text.split()[1]
        print(pokemon_id,'\n')
        

        type_of = source.find('div', class_='dtm-type').text.split()
        print('Pokemon Type:\n')
        for types in type_of:
            if types != "Type":
                print(types)
                pokemon_type.append(types)
                
        
        weakness_of = source.find('div', class_='dtm-weaknesses').text.split()
        print('\nPokemon Weakness:\n')
        for weak in weakness_of:
            if weak != 'Weaknesses':            
                print(weak)
                #c.execute("INSERT INTO pokemon (Weakness) VALUES (?)",(weak))        
                pokemon_weakness.append(weak)
                

        print('\nDescription:\n')
        description1 = source.find('p', class_='version-x').text.split(' ' * 18)[1]
        description2 = source.find('p', class_='version-y').text.split(' ' * 18)[1]
        pokemon_description = description1 + "\n" + description2 
        if len(description1) != len(description2):
            print(pokemon_description)
        else:
            pokemon_description = description1
            print(pokemon_description)
            
        print('*' * 80)
        
        pokemon_data = [pokemon_data, pokemon_id, pokemon_type, pokemon_weakness, pokemon_description]
        
        #c.execute("INSERT INTO pokemon(d, f, g, h, j)VALUES(?, ?, ?, ?, ?)", (pokemon_data, pokemon_id, pokemon_type, pokemon_weakness, pokemon_description)        pokemon_type.clear()
        #conn.commit()

        pokemon_type.clear
        pokemon_weakness.clear()
        pokemon_data.clear()
    
    elif url.status_code == 404:
        print(url.url, "Not Found")


c.close()
conn.close()
