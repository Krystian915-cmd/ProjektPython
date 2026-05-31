"""
### WYMÓG: Wykonaj dokumentację dla co najmniej 2 modułów.
Moduł: address
Zarządza danymi adresowymi klientów w pliku CSV.
Napisany w paradygmacie funkcyjnym (czyste funkcje).
"""

import pandas as pd

ADDRESS_FILE = "address.csv"


# ==========================================
# 1. FUNKCJE ZAPISU I ODCZYTU (Wejście / Wyjście)
# Te funkcje odpowiadają tylko za kontakt z dyskiem.
# ==========================================

def load_addresses():
    """
    Wczytuje plik CSV z adresami.
    Jeśli pliku nie ma, zwraca pustą strukturę z kolumnami ID, Miasto, Ulica.
    """
    ### WYMÓG: Obsługa wyjątków
    try:
        return pd.read_csv(ADDRESS_FILE)
    except Exception:
        # Jeśli plik nie istnieje, tworzymy pustą tabelę z kolumnami startowymi
        return pd.DataFrame(columns=["ID", "Miasto", "Ulica"])


def save_addresses(df):
    """Zapisuje tabelę z adresami z powrotem do pliku CSV."""
    df.to_csv(ADDRESS_FILE, index=False)


# ==========================================
# 2. CZYSTA FUNKCJA (Wymóg: Paradygmat funkcyjny)
# Tutaj pokazujesz profesorowi, że rozumiesz czyste funkcje!
# ==========================================

### WYMÓG: Możesz programować wyłącznie w paradygmacie funkcyjnym
### WYMÓG: Utwórz funkcję wielu zmiennych wejściowych (Przyjmuje 4 argumenty)
def update_address_logic(stara_tabela, customer_id, new_city, new_street):
    """
    Czysta funkcja (Pure Function) aktualizująca adres.
    NIE MODYFIKUJE oryginalnej tabeli z zewnątrz, tylko robi jej kopię,
    wprowadza zmiany i zwraca jako zupełnie NOWY wynik.
    """
    # .copy() robi niezależną kopię tabeli, żeby nie psuć oryginalnych danych
    nowa_tabela = stara_tabela.copy()

    # Szukamy w tabeli wiersza, w którym kolumna "ID" zgadza się z naszym customer_id.
    # Wchodzimy w kolumny "Miasto" oraz "Ulica" i przypisujemy im nowe wartości.
    nowa_tabela.loc[nowa_tabela["ID"] == customer_id, "Miasto"] = new_city
    nowa_tabela.loc[nowa_tabela["ID"] == customer_id, "Ulica"] = new_street

    # Zwracamy nową, zmodyfikowaną tabelę jako wynik
    return nowa_tabela


# ==========================================
# 3. GŁÓWNA FUNKCJA (Dla Klienta podczas rejestracji)
# ==========================================

def update_customer_address(customer_id, city, street):
    """
    Funkcja wywoływana automatycznie z pliku gui.py zaraz po rejestracji klienta.
    Uzupełnia puste pola 'Brak' na prawdziwe Miasto i Ulicę podane w formularzu.
    """
    try:
        # Upewniamy się, że ID to liczba całkowita
        customer_id = int(customer_id)

        current_df = load_addresses()

        # Sprawdzamy, czy wylosowane ID klienta w ogóle znajduje się w pliku address.csv
        if customer_id not in current_df["ID"].values:
            return False

        # Wywołujemy naszą czystą funkcję logiki biznesowej z punktu 2
        updated_df = update_address_logic(current_df, customer_id, city, street)

        # Zapisujemy nowo powstałą tabelę na dysk komputera
        save_addresses(updated_df)
        return True

    except Exception:
        # Jeśli wystąpi jakikolwiek nieprzewidziany błąd, funkcja po prostu zwróci False
        return False