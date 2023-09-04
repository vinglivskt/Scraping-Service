import codecs
import os, sys
from django.db import DatabaseError

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django

django.setup()

from scraping.parser import *
from scraping.parser import habr
from scraping.models import Vacancy, City, Language

parsers = (
    (hh, 'https://rostov.hh.ru/search/vacancy?text=python&area=76'),
    (rabota, 'https://rostov.rabota.ru/vacancy/?query=python'),
    (habr, 'https://career.habr.com/vacancies/programmist_python')

)
city = City.objects.filter(slug='moskva').first()
language = Language.objects.filter(slug='python').first()

jobs, errors = [], []
for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e
for job in jobs:
    v = Vacancy(**job, city=city, language=language)
    try:
        v.save()
    except DatabaseError:
        pass

# h = codecs.open('../work.txt', 'w', 'utf-8')
# h.write(str(jobs))
# h.close()
