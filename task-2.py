import time
import re
import hyperloglog
import pandas as pd

def load_ip_addresses(filename: str) -> list[str]:
    ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
    ip_addresses = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                match = ip_pattern.search(line)
                if match:
                    ip_addresses.append(match.group())
    except FileNotFoundError:
        print(f"Файл {filename} не знайдено.")
    return ip_addresses

def count_unique_ips_set(ip_addresses: list[str]) -> int:
    return len(set(ip_addresses))

def count_unique_ips_hyperloglog(ip_addresses: list[str], precision: int = 0.01) -> int:
    hll = hyperloglog.HyperLogLog(precision)
    for ip in ip_addresses:
        hll.add(ip)
    return int(len(hll))

def compare_methods(filename: str):
    ip_addresses = load_ip_addresses(filename)
    if not ip_addresses:
        return
    
    start_time = time.time()
    exact_count = count_unique_ips_set(ip_addresses)
    exact_time = time.time() - start_time
    
    start_time = time.time()
    approx_count = count_unique_ips_hyperloglog(ip_addresses)
    approx_time = time.time() - start_time
    
    data = {
        "Метод": ["Точний підрахунок", "HyperLogLog"],
        "Унікальні елементи": [exact_count, approx_count],
        "Час виконання (сек.)": [exact_time, approx_time]
    }
    df = pd.DataFrame(data)
    print("Результати порівняння:")
    print(df)

if __name__ == "__main__":
    compare_methods("lms-stage-access.log")
