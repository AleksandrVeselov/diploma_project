import openpyxl
from django.core.management import BaseCommand
import pandas as pd

from navigation.models import GasStation


def filter_func(symbol):
    required_symbols = '0123456789.'
    if symbol in required_symbols:
        return True
    else:
        return False


class Command(BaseCommand):

    def handle(self, *args, **options):
        """Команда для заполнения таблицы АЗС данными из файла spisokAZS.xlsx"""

        # чтение данных из файла
        workbook = openpyxl.load_workbook("spisokAZS.xlsx")
        worksheet = workbook.active

        azs = []  # список словарей с данными об АЗС
        for w in worksheet:

            # если есть дизельное топливо 1 или 2 типа
            if w[4].value or w[5].value:

                # если есть 1 и 2 тип, выбираем наименьшую стоимость
                if w[4].value and w[5].value:
                    price1 = ''.join(filter(filter_func, w[4].value[0:4]))
                    price2 = ''.join(filter(filter_func, w[5].value[0:4]))
                    price_diesel_fuel = min([float(price1), float(price2)])

                # если есть 1 тип
                elif w[4].value:
                    price_diesel_fuel = ''.join(filter(filter_func, w[4].value[0:4]))

                # если есть 2 тип
                elif w[5].value:
                    price_diesel_fuel = ''.join(filter(filter_func, w[5].value[0:4]))

                # добавляем азс в список
                azs.append({'latitude': w[2].value,
                            'longitude': w[3].value,
                            'address': w[1].value,
                            'price_diesel_fuel': price_diesel_fuel,
                            'altitude': 2})

        azs_for_create = [] # список экземпляров класса GasStation
        for a in azs:
            azs_for_create.append(GasStation(**a))

        # Добавление продуктов в базу данных
        GasStation.objects.bulk_create(azs_for_create)
