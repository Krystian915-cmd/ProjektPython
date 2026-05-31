"""
Moduł: address
Zarządza danymi adresowymi klientów w pliku CSV.
Napisany w paradygmacie funkcyjnym (czyste funkcje).
"""

import pandas as pd

ADDRESS_FILE = "address.csv"

def load_addresses():
    """
    Wczytuje plik CSV z adresami.
    Jeśli pliku nie ma, zwraca pustą strukturę z kolumnami ID, Miasto, Ulica.
    Obsługa wyjątków
    """
    try:
        return pd.read_csv(ADDRESS_FILE)
    except Exception:
        return pd.DataFrame(columns=["ID", "Miasto", "Ulica"])


def save_addresses(df):
    """Zapisuje tabelę z adresami (CSV.)"""
    df.to_csv(ADDRESS_FILE, index=False)

# ==========================================
#         CZYSTA FUNKCJA (Paradygmat funkcyjny)
# ==========================================

def update_address_logic(stara_tabela, customer_id, new_city, new_street): # Przyjmuje 4 argumenty
    """
    Czysta funkcja (Pure Function) aktualizująca adres.
    Nie modyfikuje oryginalnej tabeli z zewnątrz, tylko robi jej kopię,
    wprowadza zmiany i zwraca jako nowy wynik.
    """
    # .copy() robi niezalezna kopie tabeli, zeby nie zepsuc oryginalnych danych
    nowa_tabela = stara_tabela.copy()
    nowa_tabela.loc[nowa_tabela["ID"] == customer_id, "Miasto"] = new_city
    nowa_tabela.loc[nowa_tabela["ID"] == customer_id, "Ulica"] = new_street
    return nowa_tabela

# ==========================================
#             GŁÓWNA FUNKCJA
# ==========================================

def update_customer_address(customer_id, city, street):
    """
    Funkcja wywoływana automatycznie z pliku gui.py zaraz po rejestracji klienta.
    Uzupełnia puste pola ( Miasto / ulica ).
    """
    try:
        customer_id = int(customer_id)
        current_df = load_addresses()
        
        if customer_id not in current_df["ID"].values:
            return False

        # Wykorzystujemy czystą funkcje 
        updated_df = update_address_logic(current_df, customer_id, city, street)
        save_addresses(updated_df)
        return True

    except Exception:
        return False
