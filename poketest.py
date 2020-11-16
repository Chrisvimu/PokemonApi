import requests
import numpy

#Class to store each pokemon for the tournament.
class Pokemon:
    def __init__(self, pokedex, name = "", types = "", hp = 0, attack = 0, defense = 0, sataack = 0, sdefense = 0, speed = 0):
        #stats & info
        self.pokedex = pokedex
        self.name = name
        self.types = types
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.Sattack = sataack
        self.Sdefense = sdefense
        self.speed = speed
        #for combat
        self.fainted = False
        self.currenthp = hp
    def __repr__(self):
        return f"{self.pokedex}' '{self.name}' '{self.types}' '{self.hp}' '{self.attack}' '{self.defense}' '{self.Sattack}' '{self.Sdefense}' '{self.speed}' '{self.fainted}' '{self.currenthp}"

#Check type effectiveness
#Not Finished
def TypeEffectivness(attacktype, defensetype):
    typecheck = {
                'bug': {'dark': 2.0, 'fairy': 0.5, 'fighting': 0.5, 'fire': 0.5, 'flying': 0.5, 'ghost': 0.5, 'grass': 2.0, 'poison': 0.5, 'psychic': 2.0, 'steel': 0.5},
                'fire': {'fire': 0.5, 'grass': 2.0, 'water': 0.5},
                'fire': {'fire': 0.5, 'grass': 2.0, 'water': 0.5},
                'fire': {'fire': 0.5, 'grass': 2.0, 'water': 0.5},
                'fire': {'fire': 0.5, 'grass': 2.0, 'water': 0.5},
                'fire': {'fire': 0.5, 'grass': 2.0, 'water': 0.5}, 
                'grass': {'fire': 0.5, 'grass': 0.5, 'water': 2.0}, 
                'water': {'fire': 2.0, 'grass': 0.5, 'water': 0.5}}

#Selecting contestants at random for tournament
def Contestants():
    x = numpy.random.randint(1,151, size = 8)
    return x
     

#Gets pokemon information from pokemonApi
def getpokemon(pokenumber):
    url = 'https://pokeapi.co/api/v2/pokemon/'+str(pokenumber)
    response = requests.get(url)

    if response.status_code == 200:
        payload = response.json()
        name = payload["name"]
        types = payload["types"][0]['type']['name']
        hp = [stat for stat in payload['stats'] if stat['stat']['name']=='hp'][0]['base_stat']
        attack = [stat for stat in payload['stats'] if stat['stat']['name']=='attack'][0]['base_stat']
        defense = [stat for stat in payload['stats'] if stat['stat']['name']=='defense'][0]['base_stat']
        sattack = [stat for stat in payload['stats'] if stat['stat']['name']=='special-attack'][0]['base_stat']
        sdefense = [stat for stat in payload['stats'] if stat['stat']['name']=='special-defense'][0]['base_stat']
        speed = [stat for stat in payload['stats'] if stat['stat']['name']=='speed'][0]['base_stat']

        #Creacion instancia clase pokemon
        pkmn = Pokemon(pokenumber,name,types,hp,attack,defense,sattack,sdefense,speed)
        print(pkmn)
        return pkmn

#Filling pokemon list with the contestants
def Pokeindex(index):
    pokeList = []
    for x in index:
        pkmn = getpokemon(x)
        pokeList.append(pkmn)
    return pokeList

#Determine which pokemon has advantage by type
#using TypeEffectivness(type1, type2):

#Pokemon Initiative
def Initiative(pokemonA:Pokemon, pokemonB:Pokemon):
    speedA = pokemonA.speed
    speedB = pokemonB.speed    
    if speedA > speedB:
        return pokemonA.name
    else:
        return pokemonB.name
#TO DO
#implementar multiplicador para 

#Check what stats will be used
def HitStat(pkmn1:Pokemon, pkmn2:Pokemon):
    if pkmn1.Sattack > pkmn1.attack:
        hit = (pkmn2.Sdefense - pkmn1.Sattack)
    else:
        hit = (pkmn2.defense - pkmn1.attack)
    return hit

#fainted managment
#def Fainted(hp)
#Revisar como hacer esta funcion, para evitar repetir cosas uwu

#damage calcs
def Damage(pkmn1:Pokemon, pkmn2:Pokemon):
    
    hit = HitStat(pkmn1,pkmn2)

    if hit >=1:
        pkmn2.currenthp -= hit
        print(pkmn1.name+" golpea a "+pkmn2.name+" por "+str(hit)+" de dano")
        if pkmn2.currenthp <= 0:
            pkmn2.fainted = True
            print("==================================|| "+ pkmn2.name + " *c muere* ||=======================================")
        return hit
    else:
        pkmn2.currenthp -= 1
        print(pkmn1.name+" golpea a "+pkmn2.name+" por 1 de dano")
        if pkmn2.currenthp <= 0:
            pkmn2.fainted = True
            print("==================================|| "+ pkmn2.name + " *c muere* ||=======================================")
        return 1
 
#Pokemon combat
def PokeCombat(pkmnA:Pokemon, pkmnB:Pokemon, Initiative):
    x = Initiative
    y = 0
    while pkmnA.fainted == False and pkmnB.fainted == False:
        print("=====================================|| Round : " +str(y)+" ||==========================================")
        if pkmnA.name == x:
            hit = Damage(pkmnA, pkmnB)
            x = pkmnB.name
        if pkmnB.name == x:
            hit = Damage(pkmnB, pkmnA)
            x = pkmnA.name
            y += 1

#Delete fainted pokemons from list
def deletus(pokeList):
    NewpokeList = [Pokemon for Pokemon in pokeList if Pokemon.fainted == False]
    return NewpokeList

#Crear torneo
def Tournament(pokeList):
    n = 0
    while n in range(len(pokeList)):
        pokemonA = pokeList[n]
        n += 1
        pokemonB = pokeList[n]
        n += 1
        firstmove = Initiative(pokemonA, pokemonB)
        print(firstmove + " tiene la ventaja, y realiza el primer movimiento")
        PokeCombat(pokemonA,pokemonB,firstmove)

if __name__ == '__main__':
    pokeList = Pokeindex(Contestants())
    print("se han seleccionado los concursantes")
    Tournament(pokeList)
    pokeList = deletus(pokeList)
    #No se como hacer este loop, se me rompe la vida uwu
    print(pokeList)


