"""
### WYMÓG: Moduł monitorowania liczby danych (Wskazanie ze specyfikacji)
Moduł: monitor
Służy do podglądu statystyk sklepu. Administrator wywołuje go z poziomu GUI.
"""

import pandas as pd
# Importujemy nasze moduły, żeby mieć dostęp do funkcji wczytujących pliki
import products
import customers


def generate_statistics_report():
    """
    Pobiera dane z baz CSV i Excel, a następnie liczy proste statystyki.
    Zwraca gotowy tekst do wyświetlenia w okienku.
    """
    ### WYMÓG: Obsługa wyjątków (Kolejne zabezpieczenie przed awarią)
    try:
        # 1. Wczytujemy aktualne bazy danych do zmiennych
        cust_df = customers.load_csv(customers.CUSTOMERS_FILE, ["ID", "Imie", "Nazwisko", "Rok_Urodzenia"])
        prod_df = products.load_products()

        # ==========================================
        # WYMÓG: Liczba użytkowników i dostępnych produktów
        # ==========================================
        # Funkcja wbudowana len() po prostu liczy, ile jest wierszy w tabeli
        liczba_klientow = len(cust_df)
        liczba_produktow = len(prod_df)

        # ==========================================
        # WYMÓG: Średnia / Max / Min
        # ==========================================
        # Zabezpieczenie przed pustym sklepem (gdybyśmy dzielili przez 0, program by wybuchł)
        if liczba_produktow > 0:
            # Używamy najprostszych wbudowanych komend z biblioteki Pandas:
            # .sum() - sumuje wszystko, .mean() - wyciąga średnią, .max() / .min() - szuka największej/najmniejszej
            suma_sztuk = prod_df["Ilosc"].sum()
            srednia_cena = prod_df["Cena"].mean()
            max_cena = prod_df["Cena"].max()
            min_cena = prod_df["Cena"].min()
        else:
            # Jeśli nie ma towaru, wszędzie wstawiamy zera
            suma_sztuk = 0
            srednia_cena = 0.0
            max_cena = 0.0
            min_cena = 0.0

        # Tworzymy raport za pomocą formatowania tekstu (tzw. f-string).
        # Zapis {srednia_cena:.2f} oznacza: "Wstaw tu zmienną, ale zaokrąglij ją do 2 miejsc po przecinku".
        raport = (
            f"--- STATYSTYKI SKLEPU ŻABKA ---\n\n"
            f" Zarejestrowanych klientów: {liczba_klientow}\n"
            f" Liczba różnych produktów: {liczba_produktow}\n"
            f" Łącznie sztuk na magazynie: {suma_sztuk}\n"
            f"-------------------------------\n"
            f" Średnia cena produktu: {srednia_cena:.2f} zł\n"
            f" Najdroższy produkt kosztuje: {max_cena:.2f} zł\n"
            f" Najtańszy produkt kosztuje: {min_cena:.2f} zł\n"
        )

        # Zwracamy gotowy tekst (trafi on prosto do okienka MessageBox w gui.py)
        return raport

    except Exception as e:
        # Jeśli coś pójdzie nie tak (np. plik zepsuty), zwracamy po prostu ładny komunikat o błędzie
        return "Błąd podczas generowania statystyk! Sprawdź pliki bazy danych."