"""
### WYMÓG: Wykonaj dokumentację dla co najmniej 2 modułów (To jest moduł 2/2)
Moduł: products
Odpowiada za zarządzanie bazą produktów (plik Excel).
Napisany w paradygmacie funkcyjnym (oddzielenie logiki od zapisu/odczytu).
"""

import pandas as pd

PRODUCTS_FILE = "products.xlsx"


# ==========================================
# 1. FUNKCJE WEJŚCIA/WYJŚCIA (I/O - Zapis/Odczyt)
# Te funkcje tylko gadają z dyskiem komputera.
# ==========================================

### WYMÓG: Wykonaj dokumentację dla co najmniej 3 funkcji (To jest funkcja 1/3)
def load_products():
    """
    Wczytuje tabelę produktów z pliku Excel.
    Jeśli pliku nie ma, tworzy pustą tabelę gotową do pracy.
    """
    ### WYMÓG: Obsługa wyjątków (2) - Brak pliku na dysku
    try:
        # Próbujemy odczytać plik
        return pd.read_excel(PRODUCTS_FILE)
    except Exception:
        # Jeśli plik nie istnieje (np. przy pierwszym uruchomieniu),
        # program się nie wywala, tylko zwraca puste kolumny.
        return pd.DataFrame(columns=["ID", "Nazwa", "Cena", "Ilosc"])


def save_products(df):
    """Zapisuje naszą tabelę (DataFrame) z powrotem do pliku Excel."""
    # index=False sprawia, że Excel nie dodaje brzydkiej kolumny z numeracją wierszy (0, 1, 2...)
    df.to_excel(PRODUCTS_FILE, index=False)


# ==========================================
# 2. CZYSTE FUNKCJE (Serce Paradygmatu Funkcyjnego)
# Tutaj udowadniasz, że rozumiesz polecenie!
# ==========================================

### WYMÓG: Możesz programować wyłącznie w paradygmacie funkcyjnym
### WYMÓG: Utwórz funkcję wielu zmiennych wejściowych (Przyjmuje aż 5 argumentów)
def add_product_logic(df, prod_id, name, price, quantity):
    """
    Czysta funkcja (Pure Function).
    NIE ZMIENIA oryginalnej tabeli (df), tylko tworzy nową, złączoną z nowym produktem.
    """
    # Tworzymy mini-tabelkę z jednym, nowym produktem
    new_product = pd.DataFrame([{
        "ID": prod_id,
        "Nazwa": name,
        "Cena": price,
        "Ilosc": quantity
    }])

    # W programowaniu funkcyjnym nie "dopisujemy" do starych danych (nie mutujemy ich).
    # Zamiast tego bierzemy stare, bierzemy nowe, kleimy je razem (concat) i zwracamy jako NOWY wynik.
    return pd.concat([df, new_product], ignore_index=True)


def remove_product_logic(df, value, criterion="ID"):
    """
    Czysta funkcja do filtrowania produktów.
    Odrzuca to, co chcemy usunąć i zwraca nową tabelę.
    """
    if criterion == "ID":
        # Zwróć tylko te wiersze, w których ID NIE JEST RÓWNE (!=) podanej wartości
        return df[df["ID"] != value]
    elif criterion == "Nazwa":
        # Zwróć tylko te wiersze, w których Nazwa NIE JEST RÓWNA (!=) podanej wartości
        return df[df["Nazwa"] != value]
    else:
        return df


# ==========================================
# 3. GŁÓWNE FUNKCJE (Spinają wszystko w całość)
# ==========================================

def update_stock(product_name, added_quantity):
    """
    Funkcja do dostawy towaru (zwiększa ilość na magazynie).
    """
    df = load_products()

    # Sprawdzamy czy dany produkt w ogóle istnieje w kolumnie "Nazwa"
    if product_name in df["Nazwa"].values:
        # Znajdź wiersz z tym produktem, wejdź w kolumnę "Ilosc" i dodaj dostawę (+=)
        df.loc[df["Nazwa"] == product_name, "Ilosc"] += added_quantity

        save_products(df)
        return True

    return False


def add_product(prod_id, name, price, quantity):
    """
    Funkcja wywoływana przez Administratora z poziomu GUI.
    """
    ### WYMÓG: Obsługa wyjątków (3) - Błędne typy danych
    try:
        # Upewniamy się, że ID i ilość to liczby całkowite, a cena to ułamek.
        # Jak ktoś wpisze tekst np. "Dwa", to int() wyrzuci błąd i przejdziemy do 'except'
        prod_id = int(prod_id)
        price = float(price)
        quantity = int(quantity)

        current_df = load_products()

        # Zabezpieczenie: Sprawdzamy, czy takie ID już nie istnieje w bazie
        if prod_id in current_df["ID"].values:
            return False

        # Wywołujemy naszą czystą funkcję (z punktu 2), żeby skleić dane
        updated_df = add_product_logic(current_df, prod_id, name, price, quantity)

        # Zapisujemy nowy wynik na dysk
        save_products(updated_df)
        return True

    except Exception:
        # Przechwytujemy błędy (np. wpisanie tekstu w pole z ceną)
        return False