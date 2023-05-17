from time import sleep
import json
import requests
import pprint
from datetime import datetime, date

def encender(color):
    color_map = {
        "rojo": "luz roja",
        "verde": "luz verde",
        "azul": "luz azul",
        "apagar": ""
    }
    print(color_map.get(color, "luz apagada"))

def fetch(date):
    try:
        url = f"https://apidatos.ree.es/es/datos/mercados/precios-mercados-tiempo-real?start_date={date}T00:00&end_date={date}T23:59&time_trunc=hour"
        response = requests.get(url)
        response.raise_for_status()
        precios = response.json()
        precios_por_hora=precios["included"][0]["attributes"]["values"]
        precios_por_hora.sort(key=lambda x: x['value'])
        print(precios_por_hora)
        return precios_por_hora
    except requests.exceptions.HTTPError as errh:
        print ("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print ("Something went wrong:", err)

def nivelar(precio, posicion):
    print(precio,posicion)
    max_horas_baratas=4
    precio_max_barato=50
    precio_min_caro=150
    if precio <= precio_max_barato or posicion < max_horas_baratas:
        return "verde"
    elif precio > precio_min_caro:
        return "rojo"
    else:
        return "azul"
    
hora_actual = datetime.now().hour


def niveles_ahora():

    niveles={}
    precios_ordenados=fetch(date.today())
    hora_actual=datetime.now().hour
    for x in range(3):
        posicion=0
        for precio in precios_ordenados:
            hora=datetime.strptime(precio['datetime'], '%Y-%m-%dT%H:%M:%S.000+02:00').hour
            if hora_actual+x==hora:
                niveles[x]=nivelar(precio['value'],posicion)
            posicion+=1
    return niveles


niveles_luces = niveles_ahora()

while True:
    for nivel in niveles_luces:
        encender(niveles_luces[nivel])
        sleep(0.2)
        encender("apagar")
        sleep(0.2)
    sleep(1)
    if datetime.now().hour != hora_actual:
        niveles_luces = niveles_ahora()
        hora_actual = datetime.now().hour





    
