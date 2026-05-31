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
# FUNKCJE POMOCNICZE (Odczyt / Zapis CSV)
# ==========================================

def load_csv(filepath, columns):
    """Odczytuje plik CSV lub tworzy pustą ramkę danych z podanymi kolumnami."""
    try:
        return pd.read_csv(filepath)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return pd.DataFrame(columns=columns)


def save_csv(df, filepath):
    """Zapisuje ramkę danych do pliku CSV."""
    df.to_csv(filepath, index=False)


# ==========================================
# REJESTRACJA I USUWANIE KLIENTA
# ==========================================

def register_customer(name, surname, birth_year):
    """
    Rejestracja nowego klienta z uwzględnieniem roku urodzenia.
    """
    # DODALIŚMY NOWĄ KOLUMNĘ "Rok_Urodzenia"
    customers_df = load_csv(CUSTOMERS_FILE, ["ID", "Imie", "Nazwisko", "Rok_Urodzenia"])
    addresses_df = load_csv(ADDRESS_FILE, ["ID", "Miasto", "Ulica"])

    while True:
        new_id = random.randint(1000, 9999)
        if new_id not in customers_df["ID"].values:
            break

    # Zapis z rokiem urodzenia
    new_customer = pd.DataFrame([{"ID": new_id, "Imie": name, "Nazwisko": surname, "Rok_Urodzenia": birth_year}])
    new_address = pd.DataFrame([{"ID": new_id, "Miasto": "Brak", "Ulica": "Brak"}])

    customers_df = pd.concat([customers_df, new_customer], ignore_index=True)
    addresses_df = pd.concat([addresses_df, new_address], ignore_index=True)

    save_csv(customers_df, CUSTOMERS_FILE)
    save_csv(addresses_df, ADDRESS_FILE)

    history_file = os.path.join(DATABASE_DIR, f"{new_id}.txt")
    with open(history_file, "w", encoding="utf-8") as f:
        f.write(f"--- Historia zakupów klienta {new_id} ({name} {surname}) ---\n")

    return new_id

def delete_customer(value, criterion="ID"):
    # Tu też zaktualizowaliśmy nagłówki
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
# ==========================================
# AKTUALIZACJA PAKIETU: DEKORATOR I ZAKUPY
# ==========================================

def multi_purchase_decorator(func):
    """
    To jest FUNKCJA WYŻSZEGO RZĘDU (przyjmuje inną funkcję jako argument).
    Jej celem jest "udekorowanie" funkcji zakupowej, by obsługiwała wiele
    produktów na raz (np. cały koszyk zakupowy).
    """

    def wrapper(customer_id, *args):
        """
        To jest FUNKCJA ZAGNIEŻDŻONA.
        Zmienna *args przechowuje krotki z produktami, np.: ("Chleb", 2), ("Mleko", 1).
        """
        print(f"[KOSZYK] Rozpoczynam transakcję dla klienta ID: {customer_id}")

        # Iterujemy przez wszystkie produkty podane w argumentach (dowolna liczba!)
        for product_name, quantity in args:
            # Wywołujemy oryginalną, niezmodyfikowaną funkcję dla każdego z nich
            func(customer_id, product_name, quantity)

        print("[KOSZYK] Transakcja zakończona pomyślnie.\n")

    return wrapper


# Użycie dekoratora na oryginalnej funkcji (wymóg: "nie modyfikując i nie zmieniając nazw funkcji")
# Użycie dekoratora na oryginalnej funkcji
@multi_purchase_decorator
def buy_product(customer_id, product_name, quantity):
    """
    Funkcja zapisuje zakup do pliku i ODEJMUJE towar z magazynu (products.xlsx).
    """
    filepath = os.path.join(DATABASE_DIR, f"{customer_id}.txt")

    if not os.path.exists(filepath):
        print(f"[BŁĄD] Nie znaleziono konta dla ID {customer_id}! Najpierw się zarejestruj.")
        return

    # ---- NOWA LOGIKA: Odejmujemy ze stanu w Excelu ----
    prod_df = products.load_products()

    # 1. Sprawdzamy czy produkt w ogóle jest w sklepie
    if product_name not in prod_df["Nazwa"].values:
        print(f"[BŁĄD] Produkt '{product_name}' nie istnieje w bazie sklepu!")
        return

    # 2. Pobieramy aktualną ilość z magazynu
    current_qty = prod_df.loc[prod_df["Nazwa"] == product_name, "Ilosc"].values[0]

    # 3. Sprawdzamy, czy w sklepie jest wystarczająco towaru
    if current_qty < quantity:
        print(
            f"[BŁĄD] Za mało towaru! Chcesz kupić {quantity}, a na stanie jest tylko {current_qty} szt. '{product_name}'.")
        return

    # 4. Aktualizujemy (odejmujemy) i zapisujemy do Excela
    prod_df.loc[prod_df["Nazwa"] == product_name, "Ilosc"] = current_qty - quantity
    products.save_products(prod_df)
    # ----------------------------------------------------

    # Zapis do paragonu w TXT (robi się to TYLKO, gdy produkt faktycznie udało się zdjąć z magazynu)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(f"[{now}] Zakupiono: {product_name} | Ilość: {quantity}\n")

    print(f"   -> ZAKUP SUKCES: {product_name} (x{quantity}). Zostało na półce: {current_qty - quantity} szt.")