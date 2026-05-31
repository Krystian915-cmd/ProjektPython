"""
### WYMÓG: Wykonaj dokumentację dla co najmniej 2 modułów.
Moduł: customers
Odpowiada za rejestrację klientów, usuwanie ich z bazy
oraz obsługę koszyka zakupowego (z wykorzystaniem dekoratorów).
"""

import pandas as pd
import os
import random
from datetime import datetime
# Importujemy nasz własny moduł produktów, żeby móc zmieniać stan magazynu
import products

# Nazwy plików przypisane do zmiennych
CUSTOMERS_FILE = "customer.csv"
ADDRESS_FILE = "address.csv"
DATABASE_DIR = "DATABASE"


# ==========================================
# FUNKCJE POMOCNICZE (Odczyt / Zapis CSV)
# ==========================================

def load_csv(filepath, columns):
    """
    Wczytuje plik CSV.
    Jeśli pliku nie ma, tworzy pustą tabelę z gotowymi nazwami kolumn.
    """
    ### WYMÓG: Obsługa wyjątków
    try:
        return pd.read_csv(filepath)
    except Exception:
        # Zamiast skomplikowanych błędów, po prostu łapiemy każdy problem (np. brak pliku)
        return pd.DataFrame(columns=columns)


def save_csv(df, filepath):
    """Zapisuje naszą tabelę (DataFrame) do pliku CSV bez numeracji wierszy."""
    df.to_csv(filepath, index=False)


# ==========================================
# REJESTRACJA I USUWANIE KLIENTA
# ==========================================

### WYMÓG: Funkcja wielu zmiennych wejściowych (Przyjmuje 3 argumenty)
def register_customer(name, surname, birth_year):
    """
    Tworzy nowego klienta, losuje mu ID i tworzy jego plik z historią (paragonami).
    """
    # 1. Pobieramy obecne dane z plików
    customers_df = load_csv(CUSTOMERS_FILE, ["ID", "Imie", "Nazwisko", "Rok_Urodzenia"])
    addresses_df = load_csv(ADDRESS_FILE, ["ID", "Miasto", "Ulica"])

    # 2. Losujemy unikalne ID z przedziału 1000-9999
    while True:
        new_id = random.randint(1000, 9999)
        # Sprawdzamy, czy wylosowane ID nie istnieje już w kolumnie "ID"
        if new_id not in customers_df["ID"].values:
            break  # Jeśli nie ma, przerywamy pętlę losującą

    # 3. Tworzymy mini-tabelki (tylko z tym jednym, nowym klientem)
    new_customer = pd.DataFrame([{"ID": new_id, "Imie": name, "Nazwisko": surname, "Rok_Urodzenia": birth_year}])
    new_address = pd.DataFrame([{"ID": new_id, "Miasto": "Brak", "Ulica": "Brak"}])

    # 4. Łączymy stare tabele z nowym klientem (paradygmat funkcyjny - nie psujemy starych danych)
    customers_df = pd.concat([customers_df, new_customer], ignore_index=True)
    addresses_df = pd.concat([addresses_df, new_address], ignore_index=True)

    # 5. Zapisujemy wyniki do plików
    save_csv(customers_df, CUSTOMERS_FILE)
    save_csv(addresses_df, ADDRESS_FILE)

    # 6. Tworzymy pusty plik tekstowy dla tego klienta (na jego paragony) w folderze DATABASE
    history_file = os.path.join(DATABASE_DIR, f"{new_id}.txt")
    with open(history_file, "w", encoding="utf-8") as f:
        f.write(f"--- Historia zakupów klienta {new_id} ({name} {surname}) ---\n")

    return new_id


def delete_customer(value, criterion="ID"):
    """Usuwa klienta z bazy danych."""
    customers_df = load_csv(CUSTOMERS_FILE, ["ID", "Imie", "Nazwisko", "Rok_Urodzenia"])

    if criterion == "ID":
        try:
            value = int(value)
            # Filtrowanie: Zostawiamy w tabeli tylko te wiersze, gdzie ID NIE JEST RÓWNE usuwanej wartości
            customers_df = customers_df[customers_df["ID"] != value]
        except ValueError:
            return False

    elif criterion == "NAME":
        # To samo dla imienia
        customers_df = customers_df[customers_df["Imie"] != value]

    # Nadpisujemy stary plik odchudzoną tabelą
    save_csv(customers_df, CUSTOMERS_FILE)
    return True


# =======================================================================
# DEKORATOR I ZAKUPY - NAJWAŻNIEJSZA CZĘŚĆ PROJEKTU POD KĄTEM WYMOGÓW!
# =======================================================================

### WYMÓG: Utwórz funkcję wyższego rzędu
### (To taka funkcja, która jako argument w nawiasie przyjmuje INNĄ funkcję np. 'func')
def multi_purchase_decorator(func):
    """
    Dekorator rozszerzający możliwości zwykłej funkcji kupowania.
    Pozwala kupić wiele produktów naraz (cały koszyk).
    """

    ### WYMÓG: Utwórz funkcję zagnieżdżoną
    ### (Czyli funkcję zdefiniowaną wewnątrz innej funkcji)
    def wrapper(customer_id, *args):
        # *args to paczka. Tutaj wpadają krotki z produktami z pliku gui.py
        # np. [("Woda", 2), ("Chleb", 1)]

        # Pętla for "rozpakowuje" koszyk i dla każdej pozycji wywołuje starą,
        # pojedynczą funkcję zakupu.
        for product_name, quantity in args:
            func(customer_id, product_name, quantity)

    # Funkcja wyższego rzędu musi zwrócić funkcję zagnieżdżoną
    return wrapper


### WYMÓG: Użyj dekoratora (Znak @ - podmienia starą funkcję na tę z wrappera)
### WYMÓG: Klient ma możliwość zakupu dowolnej liczby produktów równocześnie.
@multi_purchase_decorator
def buy_product(customer_id, product_name, quantity):
    """
    Oryginalna, podstawowa funkcja realizująca zakup JEDNEGO produktu.
    Sprawdza magazyn, odejmuje sztuki i drukuje paragon.
    """
    filepath = os.path.join(DATABASE_DIR, f"{customer_id}.txt")

    if not os.path.exists(filepath):
        return  # Jeśli klient nie ma swojego pliku txt, przerywamy

    # Wczytujemy plik Excela z towarami (z modułu products)
    prod_df = products.load_products()

    # 1. Sprawdzamy czy dany produkt istnieje w kolumnie "Nazwa"
    if product_name not in prod_df["Nazwa"].values:
        return

    # 2. Pobieramy obecną ilość towaru z magazynu.
    # .loc[] szuka wiersza, gdzie nazwa się zgadza, wchodzi w kolumnę "Ilosc" i bierze wartość .values[0]
    current_qty = prod_df.loc[prod_df["Nazwa"] == product_name, "Ilosc"].values[0]

    # 3. Zabezpieczenie: Sprawdzamy czy klient nie chce kupić więcej, niż mamy w sklepie
    if current_qty < quantity:
        return  # Za mało towaru, więc przerywamy

    # 4. Odejmowanie towaru. Wpisujemy w kratkę Excela nową wartość (stary stan minus to co kupiono)
    prod_df.loc[prod_df["Nazwa"] == product_name, "Ilosc"] = current_qty - quantity

    # 5. Zapisujemy zaktualizowany stan magazynu z powrotem do pliku xlsx
    products.save_products(prod_df)

    # 6. Dopisujemy pozycję do pliku TXT klienta (tzw. "Paragon")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(f"[{now}] Zakupiono: {product_name} | Ilość: {quantity}\n")