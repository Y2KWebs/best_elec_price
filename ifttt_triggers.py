
from time import sleep
import requests
import pprint
from datetime import datetime,date

def fetch(date):
    try:
        url = f"https://apidatos.ree.es/es/datos/mercados/precios-mercados-tiempo-real?start_date={date}T00:00&end_date={date}T23:59&time_trunc=hour"
        response = requests.get(url)
        response.raise_for_status()
        precios = response.json()
        precios_por_hora=precios["included"][0]["attributes"]["values"]
        precios_por_hora.sort(key=lambda x: x['value'])
        return precios_por_hora
    except requests.exceptions.HTTPError as errh:
        print ("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print ("Something went wrong:", err)

def nivelar(precio,pocicion):
    min_horas_baratas=4 #Como minimo cuantas horas mas baratas del dia independientemente del precio
    precio_max_barato=50 #50 equivale a 0.005 kwh
    if precio<=precio_max_barato or pocicion<min_horas_baratas:
        requests.post("https://maker.ifttt.com/trigger/cheap_hour_starts/json/with/key/ro424fPne08N2QWP3w9P4")
    else:
        requests.post("https://maker.ifttt.com/trigger/expensive_hour_starts/json/with/key/ro424fPne08N2QWP3w9P4")


def nivel_ahora():
    precios_ordenados=fetch(str(date.today()))
    hora_actual=datetime.now().hour
    posicion=0
    for precio in precios_ordenados:
        hora=datetime.strptime(precio['datetime'], '%Y-%m-%dT%H:%M:%S.000+02:00').hour
        if hora_actual==hora:
            nivelar(precio['value'],posicion)
        posicion+=1

nivel_ahora()


    










