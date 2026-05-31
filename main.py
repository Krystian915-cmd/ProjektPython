"""
Moduł: main
Główny moduł administracyjny sklepu online Żabka.
Zarządza zasobami początkowymi programu, weryfikuje istnienie bazy danych
oraz uruchamia całą aplikację.
"""

import os
import gui

# Zmienne globalne (w paradygmacie funkcyjnym staramy się ich unikać,
# ale stałe konfiguracyjne są jak najbardziej w porządku)
DATABASE_DIR = "DATABASE"
PRODUCTS_FILE = "products.xlsx"
CUSTOMERS_FILE = "customer.csv"
ADDRESS_FILE = "address.csv"


def setup_environment():
    """
    Funkcja przygotowująca środowisko pracy programu.
    Sprawdza czy istnieje folder DATABASE i pliki z bazą.
    Jeśli nie, to je tworzy.
    """
    # Obsługa wyjątków - nr 1 (wymóg projektowy)
    try:
        # Tworzenie folderu DATABASE, jeśli nie istnieje
        if not os.path.exists(DATABASE_DIR):
            os.makedirs(DATABASE_DIR)
            print(f"[INFO] Utworzono folder: {DATABASE_DIR}")

        # Tworzenie pustych plików baz danych, jeśli ich nie ma (na razie jako atrapy,
        # w kolejnych modułach zajmiemy się ich nagłówkami za pomocą np. pandas)
        for file in [PRODUCTS_FILE, CUSTOMERS_FILE, ADDRESS_FILE]:
            if not os.path.exists(file):
                with open(file, 'w', encoding='utf-8') as f:
                    pass  # Zwykłe stworzenie pustego pliku
                print(f"[INFO] Utworzono brakujący plik: {file}")

    except PermissionError:
        print("[BŁĄD KRYTYCZNY] Brak uprawnień do tworzenia plików w tym folderze.")
    except Exception as e:
        print(f"[BŁĄD NIEZNANY] Wystąpił problem podczas startu: {e}")


def __main__():
    """
    Główna funkcja uruchamiająca program (według specyfikacji zadania).
    Spina ze sobą przygotowanie środowiska i start interfejsu/konsoli.
    """
    print("=" * 40)
    print(" WITAJ W SYSTEMIE SKLEPU ŻABKA ONLINE")
    print("=" * 40)

    print("[SYSTEM] Inicjalizacja zasobów...")
    setup_environment()

    print("[SYSTEM] Zasoby gotowe. Przechodzenie do logowania...")
    gui.start_app()
    # Tutaj w przyszłości wywołamy np.: gui_module.start_app()
    # Na ten moment dajemy prosty komunikat:
    print("[SYSTEM] Moduł główny załadowany pomyślnie. Oczekiwanie na kolejne moduły.")


# Uruchomienie programu
if __name__ == '__main__':
    __main__()