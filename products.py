"""
Moduł: products
Zarządza bazą produktów spożywczych (plik products.xlsx).
Zaprojektowany w duchu programowania funkcyjnego - logika przetwarzania danych
jest oddzielona od odczytu/zapisu plików (efektów ubocznych).
"""

import pandas as pd
import os

PRODUCTS_FILE = "products.xlsx"


# ==========================================
# FUNKCJE POMOCNICZE (I/O - Zapis / Odczyt)
# ==========================================

def load_products(filepath=PRODUCTS_FILE):
    """
    Wczytuje produkty z pliku Excel.
    Jeśli plik jest pusty lub uszkodzony, zwraca nową, pustą ramkę danych.
    """
    # Obsługa wyjątków - nr 2 (kolejny wymóg zaliczony)
    try:
        return pd.read_excel(filepath)
    except (FileNotFoundError, ValueError, Exception):
        # Zwracamy pusty szkielet tabeli, jeśli pliku nie da się odczytać
        return pd.DataFrame(columns=["ID", "Nazwa", "Cena", "Ilosc"])


def save_products(df, filepath=PRODUCTS_FILE):
    """Zapisuje ramkę danych z powrotem do pliku Excel."""
    df.to_excel(filepath, index=False)


# ==========================================
# CZYSTE FUNKCJE (Paradygmat funkcyjny)
# ==========================================

def add_product_logic(df, prod_id, name, price, quantity):
    """
    Czysta funkcja (pure function) wielu zmiennych wejściowych.
    Zwraca nową ramkę danych z dodanym produktem, NIE modyfikując oryginalnej.
    """
    new_product = pd.DataFrame([{
        "ID": prod_id,
        "Nazwa": name,
        "Cena": price,
        "Ilosc": quantity
    }])
    # W programowaniu funkcyjnym łączymy struktury, zamiast je mutować
    return pd.concat([df, new_product], ignore_index=True)


def remove_product_logic(df, value, criterion="ID"):
    """
    Czysta funkcja odfiltrowująca produkty.
    Usuwa produkty względem ID lub Nazwy.
    """
    if criterion == "ID":
        # Filtrujemy wiersze, zostawiając te, gdzie ID nie równa się podanej wartości
        return df[df["ID"] != value]
    elif criterion == "Nazwa":
        return df[df["Nazwa"] != value]
    else:
        return df


def update_stock(product_name, added_quantity):
    """
    Funkcja obsługująca dostawę towaru.
    Zwiększa ilość istniejącego produktu o podaną wartość.
    """
    df = load_products()

    # Sprawdzamy, czy produkt jest w bazie
    if product_name in df["Nazwa"].values:
        # Pobieramy obecną ilość
        current_qty = df.loc[df["Nazwa"] == product_name, "Ilosc"].values[0]
        # Nadpisujemy nową (stara ilość + dostawa)
        df.loc[df["Nazwa"] == product_name, "Ilosc"] = current_qty + added_quantity

        save_products(df)
        return True
    return False


# ==========================================
# GŁÓWNE FUNKCJE MODUŁU (Dla Administratora)
# ==========================================

def add_product(prod_id, name, price, quantity):
    """
    Funkcja 1: Dodawanie nowego produktu do bazy.
    Spina w całość odczyt, logikę funkcyjną i zapis.
    """
    try:
        # Rzutowanie typów, żeby w bazie był porządek
        prod_id = int(prod_id)
        price = float(price)
        quantity = int(quantity)

        current_df = load_products()

        # Sprawdzamy czy ID już przypadkiem nie istnieje
        if prod_id in current_df["ID"].values:
            print(f"[BŁĄD] Produkt o ID {prod_id} już istnieje!")
            return False

        # Wywołanie czystej funkcji
        updated_df = add_product_logic(current_df, prod_id, name, price, quantity)
        save_products(updated_df)

        print(f"[SUKCES] Dodano produkt: {name} (ID: {prod_id}) do bazy.")
        return True

    except ValueError:
        # Obsługa wyjątków - nr 3 (Zabezpieczenie przed wpisaniem liter zamiast cyfr)
        print("[BŁĄD] Nieprawidłowy typ danych! ID i ilość to liczby całkowite, a cena to liczba zmiennoprzecinkowa.")
        return False


def remove_product(value, criterion="ID"):
    """
    Funkcja 2: Usuwanie produktów z bazy względem ID lub Nazwy.
    Opcje argumentu criterion: 'ID' lub 'Nazwa'.
    """
    current_df = load_products()

    # Rzutowanie wartości na int, jeśli usuwamy po ID
    if criterion == "ID":
        try:
            value = int(value)
        except ValueError:
            print("[BŁĄD] Wartość ID musi być liczbą całkowitą!")
            return False

    updated_df = remove_product_logic(current_df, value, criterion)

    # Sprawdzamy czy liczba wierszy się zmieniła (czy coś zostało usunięte)
    if len(current_df) == len(updated_df):
        print(f"[INFO] Nie znaleziono produktu do usunięcia (Kryterium: {criterion}, Wartość: {value}).")
        return False
    else:
        save_products(updated_df)
        print(f"[SUKCES] Pomyślnie usunięto produkt(y) (Kryterium: {criterion}, Wartość: {value}).")
        return True