"""
### WYMÓG: Wykonaj dokumentację dla co najmniej 2 modułów (To jest moduł 1/2)
Moduł: main
Główny moduł, który administruje zasobami sklepu.
Uruchamia program i przygotowuje puste pliki startowe.
"""

# biblioteką (OS) sprawdzamy czy plik istnieje, i pozwala tworzyc foldery
import os

#Importujemy nasz wlasny plik gui.py, zeby moc polaczyc sie z okienkiem glownym sklepu
import gui

# Zmienne przechowujące nazwy plików
DATABASE_DIR = "DATABASE"
PRODUCTS_FILE = "products.xlsx"
CUSTOMERS_FILE = "customer.csv"
ADDRESS_FILE = "address.csv"


def setup_environment():
    """
    Sprawdza, czy istnieją potrzebne pliki i foldery.
    Jeśli ich nie ma, program sam je utworzy przed startem.
    """
    ### WYMÓG: Dla co najmniej 3 funkcji wykonaj obsługę wyjątków (To jest wyjątek 1/3)
    try:
        # Sprawdza i tworzy folder DATABASE
        if not os.path.exists(DATABASE_DIR):
            os.makedirs(DATABASE_DIR)
            print(f"[INFO] Utworzono folder: {DATABASE_DIR}")

        lista_plikow = [PRODUCTS_FILE, CUSTOMERS_FILE, ADDRESS_FILE]
        for plik in lista_plikow:
            if not os.path.exists(plik):
                # Otwarcie pliku w trybie 'w' (write) automatycznie tworzy pusty plik
                with open(plik, 'w', encoding='utf-8') as f:
                    pass
                print(f"[INFO] Utworzono brakujący plik: {plik}")

    except Exception as e:
        print(f"Błąd podczas tworzenia plików startowych: {e}")


### WYMÓG: Moduł main musi zawierać: def __main__()
def __main__():
    print("Uruchamiam ŻABKA")
    setup_environment()
    gui.start_app()

if __name__ == '__main__':
    __main__()
