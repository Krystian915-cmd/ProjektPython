"""
Moduł: monitor
Odpowiada za monitorowanie zasobów sklepu i generowanie statystyk.
Wykorzystuje funkcje wbudowane w pandas do szybkiej analizy danych.
"""

import pandas as pd
import products
import customers


# ==========================================
# CZYSTE FUNKCJE ANALITYCZNE
# ==========================================

def get_total_customers(customers_df):
    """Zwraca całkowitą liczbę zarejestrowanych klientów."""
    return len(customers_df)


def get_total_products(products_df):
    """Zwraca liczbę unikalnych produktów w bazie."""
    return len(products_df)


def get_total_stock(products_df):
    """Zwraca łączną sumę wszystkich sztuk towaru na magazynie."""
    if products_df.empty:
        return 0
    return products_df["Ilosc"].sum()


def get_average_price(products_df):
    """Zwraca średnią cenę produktu w sklepie."""
    if products_df.empty:
        return 0.0
    return round(products_df["Cena"].mean(), 2)


# ==========================================
# GŁÓWNA FUNKCJA RAPORTUJĄCA
# ==========================================

def generate_statistics_report():
    """
    Pobiera dane z plików i wylicza wszystkie statystyki.
    Zwraca sformatowany tekst raportu gotowy do wyświetlenia.
    """
    # Wczytujemy aktualny stan baz danych korzystając z funkcji z innych modułów
    # Wymaga to zaimportowania tych modułów na górze pliku
    cust_df = customers.load_csv(customers.CUSTOMERS_FILE, ["ID", "Imie", "Nazwisko"])
    prod_df = products.load_products()

    # Wyliczanie statystyk za pomocą czystych funkcji
    total_cust = get_total_customers(cust_df)
    total_prod = get_total_products(prod_df)
    total_stock = get_total_stock(prod_df)
    avg_price = get_average_price(prod_df)

    # Budowanie gotowego tekstu raportu
    report = (
        f"📊 RAPORT STATYSTYCZNY SKLEPU ŻABKA\n"
        f"------------------------------------\n"
        f"👥 Zarejestrowanych klientów: {total_cust}\n"
        f"📦 Różnych produktów w ofercie: {total_prod}\n"
        f"🛒 Łączna liczba sztuk na magazynie: {total_stock}\n"
        f"💰 Średnia cena produktu: {avg_price} PLN\n"
    )

    return report


# Prosty test modułu
if __name__ == "__main__":
    print(generate_statistics_report())