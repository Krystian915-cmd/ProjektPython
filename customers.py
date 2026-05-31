"""
Moduł: customers
Odpowiada za rejestrację klientów, usuwanie ich z bazy
oraz obsługę koszyka zakupowego (z wykorzystaniem dekoratorów).
"""

import pandas as pd
import os
import random
from datetime import datetime
import products

CUSTOMERS_FILE = "customer.csv"
ADDRESS_FILE = "address.csv"
DATABASE_DIR = "DATABASE"


# ==========================================
#             (Odczyt / Zapis CSV)
# ==========================================

def load_csv(filepath, columns):
    """
    Wczytuje plik CSV.  
    Jeśli pliku nie ma, tworzy nową pustą tabelę.
    """
    try:
        return pd.read_csv(filepath)
    except Exception:
        return pd.DataFrame(columns=columns)


def save_csv(df, filepath):
    """Zapisuje naszą tabelę do pliku CSV bez numeracji wierszy."""
    df.to_csv(filepath, index=False)


# ==========================================
#             REJESTRACJA I USUWANIE 
# ==========================================

def register_customer(name, surname, birth_year):
    """
    Tworzy nowego klienta, losuje mu ID i tworzy jego plik z historią (paragonami).
    """
    customers_df = load_csv(CUSTOMERS_FILE, ["ID", "Imie", "Nazwisko", "Rok_Urodzenia"])
    addresses_df = load_csv(ADDRESS_FILE, ["ID", "Miasto", "Ulica"])
    while True:
        new_id = random.randint(1000, 9999)
        if new_id not in customers_df["ID"].values:
            break 
            
    new_customer = pd.DataFrame([{"ID": new_id, "Imie": name, "Nazwisko": surname, "Rok_Urodzenia": birth_year}])
    new_address = pd.DataFrame([{"ID": new_id, "Miasto": "Brak", "Ulica": "Brak"}])

    # Łączymy stare tabele z nowym klientem (paradygmat ) funkcyjny - nie psujemy starych danych 
    customers_df = pd.concat([customers_df, new_customer], ignore_index=True)
    addresses_df = pd.concat([addresses_df, new_address], ignore_index=True)

    save_csv(customers_df, CUSTOMERS_FILE)
    save_csv(addresses_df, ADDRESS_FILE)

    history_file = os.path.join(DATABASE_DIR, f"{new_id}.txt")
    with open(history_file, "w", encoding="utf-8") as f:
        f.write(f"--- Historia zakupów klienta {new_id} ({name} {surname}) ---\n")

    return new_id


def delete_customer(value, criterion="ID"):
    """Usuwa klienta z bazy danych.
    Filtrowanie: Zostawiamy w tabeli tylko te wiersze, gdzie ID NIE JEST RÓWNE usuwanej wartości
    """
    customers_df = load_csv(CUSTOMERS_FILE, ["ID", "Imie", "Nazwisko", "Rok_Urodzenia"])

    if criterion == "ID":
        try:
            value = int(value)
            customers_df = customers_df[customers_df["ID"] != value]
        except ValueError:
            return False

    elif criterion == "NAME":
        customers_df = customers_df[customers_df["Imie"] != value]

    save_csv(customers_df, CUSTOMERS_FILE)
    return True


# ======================================================
#                         DEKORATOR
# ======================================================

### Funkcja wyższego rzędu
def multi_purchase_decorator(func):
    """
    Dekorator pozwala kupic wiele produktów 
    Dekorator rozszerzający możliwości zwykłej funkcji kupowania.
    Pozwala kupić wiele produktów naraz (cały koszyk).
    """

    ### funkcja zagnieżdżona - czyli funkcja w funkcji
    def wrapper(customer_id, *args):
        # Tutaj wpadają krotki z produktami z pliku gui.py
        # np. [("Woda", 2), ("Chleb", 1)]
        for product_name, quantity in args:
            func(customer_id, product_name, quantity)

    return wrapper


### Użycie dekoratora (Znak @ - podmienia starą funkcję na tę z wrappera)
@multi_purchase_decorator
def buy_product(customer_id, product_name, quantity):
    """
    Realizuje zakup jednego produktu
    Sprawdza magazyn, odejmuje sztuki i drukuje paragon.
    """
    filepath = os.path.join(DATABASE_DIR, f"{customer_id}.txt")

    if not os.path.exists(filepath):
        return 

    prod_df = products.load_products()

    if product_name not in prod_df["Nazwa"].values:
        return

    # .loc[] szuka wiersza, gdzie nazwa się zgadza, wchodzi w kolumnę "Ilosc" i bierze wartość .values[0]
    current_qty = prod_df.loc[prod_df["Nazwa"] == product_name, "Ilosc"].values[0]

    if current_qty < quantity:
        return 

    prod_df.loc[prod_df["Nazwa"] == product_name, "Ilosc"] = current_qty - quantity
    products.save_products(prod_df)

    #Paragon
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(f"[{now}] Zakupiono: {product_name} | Ilość: {quantity}\n")
