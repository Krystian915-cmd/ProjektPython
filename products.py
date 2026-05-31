"""
Moduł: products
Odpowiada za zarządzanie bazą produktów (plik Excel).
Napisany w paradygmacie funkcyjnym (oddzielenie logiki od zapisu/odczytu).
"""

import pandas as pd
PRODUCTS_FILE = "products.xlsx"



def load_products():
    """
    Wczytuje tabelę produktów z pliku Excel.
    Jeśli pliku nie ma, tworzy pustą tabelę gotową do pracy.
    """
    try:
        return pd.read_excel(PRODUCTS_FILE)
    except Exception:
        # program sie nie wywala, tylko zwraca puste kolumny 
        return pd.DataFrame(columns=["ID", "Nazwa", "Cena", "Ilosc"])


def save_products(df):
    """Zapisuje naszą tabelę (DataFrame) z powrotem do pliku Excel."""
    df.to_excel(PRODUCTS_FILE, index=False)


# ==========================================
#            Paradygmat funkcyjny - # 5 argumentów 
# ==========================================

def add_product_logic(df, prod_id, name, price, quantity): 
    """
    NIE ZMIENIA oryginalnej tabeli (df), tylko tworzy nową, złączoną z nowym produktem.
    """
    new_product = pd.DataFrame([{
        "ID": prod_id,
        "Nazwa": name,
        "Cena": price,
        "Ilosc": quantity
    }])

    # W programowaniu funkcyjnym nie "dopisujemy" do starych danych (nie mutujemy ich).
    # Bierzemy stare, bierzemy nowe, kleimy je razem (concat) i zwracamy jako NOWY wynik.
    return pd.concat([df, new_product], ignore_index=True)

def remove_product_logic(df, value, criterion="ID"):
    """
    Filtruje produkty
    Odrzuca to, co chcemy usunąć i zwraca nową tabelę.
    Zwraca tylko wiersze, ktore nazwa nie jest rowna podanej wartosci
    """
    if criterion == "ID":
        return df[df["ID"] != value]
    elif criterion == "Nazwa":
        return df[df["Nazwa"] != value]
    else:
        return df


# ==========================================
#               Spinamy wszystko w całość 
# ==========================================

def update_stock(product_name, added_quantity):
    """
    Funkcja do dostawy towaru (zwiększa ilość na magazynie).
    """
    df = load_products()
    if product_name in df["Nazwa"].values:
        df.loc[df["Nazwa"] == product_name, "Ilosc"] += added_quantity
        save_products(df)
        return True
    return False


def add_product(prod_id, name, price, quantity):
    """
    Funkcja wywoływana przez Administratora GUI.
    Błędne typy danych - Obsługa wyjątków
    """
    try:
        prod_id = int(prod_id)
        price = float(price)
        quantity = int(quantity)
        current_df = load_products()
        if prod_id in current_df["ID"].values:
            return False

        updated_df = add_product_logic(current_df, prod_id, name, price, quantity)

        save_products(updated_df)
        return True
    except Exception:
        #Przechwytujemy błędy
        return False
