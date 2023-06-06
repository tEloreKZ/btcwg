import bitcoin
import hashlib
import requests
import sys
import time
from colorama import init, Fore

init(autoreset=True)

def generate_random_wallet_address():
    # Generate a random private key
    private_key = bitcoin.random_key()

    # Derive the public key from the private key
    public_key = bitcoin.privkey_to_pubkey(private_key)

    # Generate the Bitcoin address from the public key
    address = bitcoin.pubkey_to_address(public_key)

    return address

def check_balance(address):
    try:
        url = f"https://chain.api.btc.com/v3/address/{address}"
        response = requests.get(url)
        data = response.json()
        balance = data['data']['balance']
        return balance
    except:
        return None

# Строчка ввода количества генерируемых биткоин кошельков
num_addresses = int(input("Enter the number of Bitcoin wallet addresses to generate: "))

# Подтверждение если запрос превышает 1500 кошельков
if num_addresses > 1500:
    confirmation = input("Generating a large number of addresses can take a while. Continue? (y/n): ")
    if confirmation.lower() != 'y':
        print("Address generation aborted.")
        input("Press Enter to exit.")
        sys.exit()

# Генерация кошельков + таймер + проценты
wallet_addresses = []
start_time = time.time()
for i in range(num_addresses):
    address = generate_random_wallet_address()
    wallet_addresses.append(address)
    elapsed_time = time.time() - start_time
    progress = (i + 1) / num_addresses * 100
    remaining_time = (num_addresses - (i + 1)) * (elapsed_time / (i + 1))
    sys.stdout.write(f"\rGenerating addresses: [{'#' * int(progress // 10)}{' ' * (10 - int(progress // 10))}] {progress:.2f}% | Time Remaining: {remaining_time:.2f} seconds")
    sys.stdout.flush()

    # Сохранение данных в файл принудительно во время генерации
    with open("btc.txt", "w") as file:
        for address in wallet_addresses:
            file.write(address + "\n")
        file.flush()

    # Задержка в секунду между генерацией
    #	if i < num_addresses - 1:
    #    	time.sleep(1)

# Вопрос о фильтрах
balance_check = input("\nDo you want to check the filters of the generated wallet addresses? (y/n): ")

# Фильтр генерирует результаты и сохраняет в btc_balance.txt и btc_balance_bad.txt
with open("btc_balance.txt", "w") as file_good, open("btc_balance_bad.txt", "w") as file_bad:
    file_good.write("BTC Address | Balance (BTC)\n")
    file_good.write("-----------------------------\n")
    file_bad.write("BTC Address\n")
    file_bad.write("-----------------------------\n")
    for address in wallet_addresses:
        if balance_check.lower() == 'y':
            balance = check_balance(address)
            if balance is not None:
                file_good.write(f"{address} | {balance:.8f}\n")
                print(Fore.GREEN + f"Address: {address} | Balance: {balance:.8f} BTC")

            else:
                file_bad.write(f"{address}\n")
                print(Fore.RED + f"Address: {address} | Failed to retrieve balance")
        else:
            file_bad.write(f"{address}\n")

if balance_check.lower() == 'y':
    print("BTC filters check results have been saved to btc_balance.txt.")
print(f"\n{num_addresses} random Bitcoin wallet addresses have been saved to btc.txt.")

# Количество рабочих и не рабочих адресов
num_working = sum(1 for line in open('btc_balance.txt')) - 2  # Subtract 2 for the header lines
num_non_working = sum(1 for line in open('btc_balance_bad.txt')) - 2  # Subtract 2 for the header lines

# Отображение строчек выше
print(f"Working addresses: {Fore.GREEN}{num_working}")
print(f"Non-working addresses: {Fore.RED}{num_non_working}")

input("Generation complete. Press Enter to exit.")
