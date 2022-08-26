

from django.conf import settings
import os
import django
import sys
import random
import requests
from bs4 import BeautifulSoup

sys.path.append('.')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nomad.settings.dev")
django.setup()

from core.models import Company

Name = []
response = requests.get(
    'https://www.shopify.com/fr/outils/generateur-de-nom-d-entreprise/rechercher?query=company&button=&tool=business_name_generator#ToolContent')
if response.ok:
    soup = BeautifulSoup(response.text, "html.parser")
    button = soup.findAll('button')
    for titre in button:
        if titre.get("data-shop-name") != None:
            Name.append(titre.get("data-shop-name"))


Type = [0, 1, 2, 3, 4]
all_zipcodes = list(settings.ZIPCODE_JSON.keys())
City = settings.ZIPCODE_JSON
for i in range(50):
    name = random.choice(Name)
    siret = random.randrange(100000000, 999999999)
    type = random.choice(Type)
    zipcode = random.choice(all_zipcodes)
    address = "avenue jean moulin"
    city = City[zipcode][0]['city']

    Company.objects.create(name=f"{name} {i}", siret=siret,
                           type=type, zipcode=zipcode, address=address, city=city)
