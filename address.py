"""
Moduł: addresses
Zarządza danymi adresowymi klientów (plik address.csv).
Zawiera funkcje do aktualizacji adresu przypisanego do konkretnego ID konta.
"""

import pandas as pd

ADDRESS_FILE = "address.csv"


# ==========================================
# FUNKCJE POMOCNICZE (I/O - Zapis / Odczyt)
# ==========================================

def load_addresses():
    """Wczytuje plik z adresami. Jeśli go nie ma, tworzy strukturę kolumn."""
    try:
        return pd.read_csv(ADDRESS_FILE)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return pd.DataFrame(columns=["ID", "Miasto", "Ulica"])


def save_addresses(df):
    """Zapisuje ramkę danych do pliku CSV."""
    df.to_csv(ADDRESS_FILE, index=False)


# ==========================================
# CZYSTE FUNKCJE (Paradygmat funkcyjny)
# ==========================================

def update_address_logic(df, customer_id, new_city, new_street):
    """
    Czysta funkcja aktualizująca adres.
    Nie modyfikuje oryginalnej ramki, zwraca nową (wymóg paradygmatu funkcyjnego).
    """
    # Kopiujemy ramkę danych, by nie modyfikować oryginału
    new_df = df.copy()

    # Warunek: aktualizujemy wiersze, gdzie ID pasuje do podanego
    mask = new_df["ID"] == customer_id

    # Wstawiamy nowe wartości dla znalezionego klienta
    new_df.loc[mask, "Miasto"] = new_city
    new_df.loc[mask, "Ulica"] = new_street

    return new_df


# ==========================================
# GŁÓWNA FUNKCJA MODUŁU
# ==========================================

def update_customer_address(customer_id, city, street):
    """
    Uzupełnia/aktualizuje adres konkretnego klienta na podstawie jego ID.
    Spina w całość odczyt, logikę i zapis.
    """
    # Obsługa wyjątków - upewniamy się, że ID jest liczbą
    try:
        customer_id = int(customer_id)
    except ValueError:
        print("[BŁĄD] ID klienta musi być liczbą całkowitą!")
        return False

    current_df = load_addresses()

    # Sprawdzamy czy klient o podanym ID w ogóle istnieje w bazie adresów
    if customer_id not in current_df["ID"].values:
        print(f"[BŁĄD] Nie znaleziono klienta o ID: {customer_id}.")
        return False

    # Użycie czystej funkcji do stworzenia zaktualizowanej tabeli
    updated_df = update_address_logic(current_df, customer_id, city, street)

    # Zapis efektów ubocznych (I/O)
    save_addresses(updated_df)
    print(f"[SUKCES] Zaktualizowano adres dla klienta ID: {customer_id} -> {city}, ul. {street}")
    return True