"""
Moduł: monitor
Służy do podglądu statystyk sklepu. Administrator wywołuje go z poziomu GUI.
"""

import pandas as pd
import products
import customers


def generate_statistics_report():
    """
    Pobiera dane z baz CSV i Excel, a następnie liczy proste statystyki.
    Zwraca gotowy tekst do wyświetlenia w okienku.
    """
    # Obsługa wyjątków
    try:
        cust_df = customers.load_csv(customers.CUSTOMERS_FILE, ["ID", "Imie", "Nazwisko", "Rok_Urodzenia"])
        prod_df = products.load_products()

        # ==========================================
        # Funkcja wbudowana len() liczy, ile jest wierszy w tabeli
        # ==========================================
        liczba_klientow = len(cust_df)
        liczba_produktow = len(prod_df)

        if liczba_produktow > 0:
            suma_sztuk = prod_df["Ilosc"].sum()
            srednia_cena = prod_df["Cena"].mean()
            max_cena = prod_df["Cena"].max()
            min_cena = prod_df["Cena"].min()
        else:
            suma_sztuk = 0
            srednia_cena = 0.0
            max_cena = 0.0
            min_cena = 0.0

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

        return raport

    except Exception as e:
        return "Błąd generowania statystyk! "
