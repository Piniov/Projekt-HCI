from django.shortcuts import render
import random
import pyowm
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


def home(request):
    print('Home')
    return render(request, 'home.html')


def about(request):
    print('About')
    return render(request, 'about.html')


def forecast(request):
    owm = pyowm.OWM('94d788527f60c0cab020f0eddc3a0518')
    cities = pd.read_csv('./myproject/weather_forecast/world-cities.csv', usecols = ['name'],squeeze = True)
    countries = pd.read_csv('./myproject/weather_forecast/world-cities.csv', usecols = ['country'],squeeze = True)
    while True:
        city = random.choice(cities)
        nr_index =(list(cities)).index(city)
        country = countries[nr_index]
        try:
           #pobiera temperaturę,procent zachmuzenia,obiętość opadów i czas uzyskania informacji
            observation = owm.weather_at_place(city)
            weather = observation.get_weather()
            temperature =round(weather.get_temperature('celsius')['temp'])
            reception_time = observation.get_reception_time('iso')
            rain_volume = weather.get_rain()
            cloud_coverage = weather.get_clouds()
            try:
                #dołącza wylosowaną nazwę miasta do linku z wikipedii i pobiera pierwszy obraz jaki znajdzie
                html = urlopen('https://en.wikipedia.org/wiki/'+city)
                bs = BeautifulSoup(html, 'html.parser')
                image = bs.find('img', {'src':re.compile('.jpg')})
                link = str(image['src'])
                break
            #jeżeli api nie znajdzie danych pogodowych dla wyloswanego miasta lub nie zadziała link do wikipedii losuje jeszcze raz miasto
            except:
                pass
        except:
            pass
    link_html = 'https://en.wikipedia.org/wiki/'+city
    #renderuje forecast.html i wysyła do niego dane
    return render(request, 'forecast.html',{'temperature': temperature,'city':city, 'link':link,'reception_time':reception_time,'rain_volume':rain_volume, "cloud_coverage":cloud_coverage, "country":country,"link_html":link_html})
