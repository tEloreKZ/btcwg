import requests
import json
from datetime import datetime
from colorama import Fore, init

init(autoreset=True)

# Открываем файл с балансами BTC
with open('btc_balance.txt', 'r') as file:
    btc_balances = file.readlines()

# Создаем файл для записи положительных балансов
output_file = 'btc_good_balance.txt'

# Получаем текущую цену BTC в USD
response = requests.get('https://api.btc.com/v3/exchange_rate')
exchange_data = json.loads(response.text)
btc_usd_price = exchange_data['data']['price']

# Создаем текущую дату и время
current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Открываем файл для записи результатов
with open(output_file, 'w') as file:
    # Записываем дату и время создания
    file.write(f'Дата и время создания: {current_datetime}\n\n')

    # Переменные для подсчета количества кошельков с балансом больше 0 и меньше 0
    balance_greater_than_zero = 0
    balance_less_than_zero = 0

    # Проверяем балансы и записываем только положительные балансы в файл
    for balance in btc_balances:
        address = balance.strip()
        response = requests.get(f'https://chain.api.btc.com/v3/address/{address}')
        address_data = json.loads(response.text)
        btc_balance = address_data['data']['balance']
        btc_balance_usd = float(btc_balance) * btc_usd_price

        if float(btc_balance) > 0:
            balance_greater_than_zero += 1
            file.write(f'Адрес: {address}\n')
            file.write(f'Баланс BTC: {btc_balance}\n')
            file.write(f'Стоимость BTC в USD: {btc_balance_usd}\n')
            file.write('\n')
            print(f'{Fore.GREEN}Адрес: {address}')
            print(f'Баланс BTC: {btc_balance}')
            print(f'Стоимость BTC в USD: {btc_balance_usd}\n')
        else:
            balance_less_than_zero += 1
            print(f'{Fore.RED}Адрес: {address}')
            print(f'Баланс BTC: {btc_balance}')
            print(f'Стоимость BTC в USD: {btc_balance_usd}\n')

    # Записываем итоговую информацию
    file.write(f'Итоговая информация:\n')
    file.write(f'Количество кошельков с балансом больше 0: {balance_greater_than_zero}\n')
    file.write(f'Количество кошельков с балансом меньше 0: {balance_less_than_zero}\n')

    # Выводим итоговую информацию
    print(f'\nИтоговая информация:')
    print(f'Количество кошельков с балансом больше 0: {balance_greater_than_zero}')
    print(f'Количество кошельков с балансом меньше 0: {balance_less_than_zero}')

# Выводим сообщение об успешном выполнении
print(f'\nПроверка баланса BTC завершена. Результаты сохранены в файл {output_file}.')

# Удаление переменных
del btc_balances, btc_usd_price, balance_greater_than_zero, balance_less_than_zero, current_datetime, exchange_data
