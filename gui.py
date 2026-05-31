"""
Moduł: gui
Zarządza interfejsem graficznym dla użytkownika.
"""

import tkinter as tk
from tkinter import messagebox
import os
from PIL import Image, ImageTk

import products
import customers
import address
import monitor

# ==========================================
# KONFIGURACJA STYLU (Kolory i czcionki przypisane do zmiennych,
# żeby nie wpisywać ich ręcznie za każdym razem)
# ==========================================
BG_COLOR = "#1E1E1E"  # (główne tło)
CARD_BG = "#2D2D30"  #  (kafelki i ramki)
ENTRY_BG = "#333337"  # Tło dla pól tekstowych
TEXT_LIGHT = "#FFFFFF"  # Biały tekst główny
TEXT_GRAY = "#AAAAAA"  # Szary tekst pomocniczy
ACCENT_GREEN = "#00E676"  # (główny akcent, przyciski)
BTN_TEXT = "#000000"  # przyciski
BTN_SECONDARY = "#3E3E42"  # przyciski "Powrót" itp.

F_MAIN = ("Segoe UI", 11)
F_BOLD = ("Segoe UI", 11, "bold")
F_HEADER = ("Segoe UI", 18, "bold")
F_PRICE = ("Segoe UI", 11, "bold")

ADMIN_PIN = "1234"
current_customer_id = None  
current_customer_is_adult = False  
CURRENT_YEAR = 2026

#=======================
### Interfejs graficzny
#=======================

def start_app():
    root = tk.Tk()
    root.title("Sklep Żabka")
    root.geometry("600x800") 
    root.configure(bg=BG_COLOR)  

    # ==========================================
    #  Przelaczanie ekranow
    # ==========================================
    def hide_all_frames():
        # Używamy .pack_forget() - to komenda tkintera do ukrywania elementów.
        lista_ramek = [frame_main, frame_admin_login, frame_admin_panel,
                       frame_customer_menu, frame_new_customer,
                       frame_reg_customer, frame_shopping]
        for ramka in lista_ramek:
            ramka.pack_forget()

    def show_frame(frame):
        hide_all_frames()
        frame.pack(fill="both", expand=True, pady=10)

    # Funkcja pomocnicza: nie trzeba pisac w kółko tego samego
    def create_styled_entry(parent, width=20, justify="center"):
        return tk.Entry(parent, font=F_MAIN, bg=ENTRY_BG, fg=TEXT_LIGHT,
                        insertbackground=TEXT_LIGHT, relief="flat", width=width, justify=justify)

    frame_main = tk.Frame(root, bg=BG_COLOR)
    frame_admin_login = tk.Frame(root, bg=BG_COLOR)
    frame_admin_panel = tk.Frame(root, bg=BG_COLOR)
    frame_customer_menu = tk.Frame(root, bg=BG_COLOR)
    frame_new_customer = tk.Frame(root, bg=BG_COLOR)
    frame_reg_customer = tk.Frame(root, bg=BG_COLOR)
    frame_shopping = tk.Frame(root, bg=BG_COLOR)

    # ==========================================
    #              MENU GŁÓWNE
    # ==========================================
    try:
        img_logo = Image.open("images/Zabka_logo_.jpg")
        img_logo = img_logo.resize((200, 140))
        logo_tk = ImageTk.PhotoImage(img_logo)
        lbl_logo = tk.Label(frame_main, image=logo_tk, bg=BG_COLOR)
        lbl_logo.image = logo_tk 
        lbl_logo.pack(pady=30)
    except FileNotFoundError:
        pass

    # Komenda lambda: "wstrzymuje" wywołanie funkcji. Gdyby jej nie było, funkcja show_frame
    # odpaliłaby się od razu przy rysowaniu przycisku, zamiast po jego kliknięciu.
    tk.Button(frame_main, text="Strefa Klienta", font=F_BOLD, width=25, height=2, bg=ACCENT_GREEN, fg=BTN_TEXT,
              relief="flat", command=lambda: show_frame(frame_customer_menu)).pack(pady=10)
    tk.Button(frame_main, text="Panel Administratora", font=F_BOLD, width=25, height=2, bg=BTN_SECONDARY, fg=TEXT_LIGHT,
              relief="flat", command=lambda: show_frame(frame_admin_login)).pack(pady=10)

    
    # ==========================================
    #                 LOGOWANIE ADMINA
    # ==========================================
    
    tk.Label(frame_admin_login, text="LOGOWANIE ADMINA", font=F_HEADER, bg=BG_COLOR, fg=ACCENT_GREEN).pack(pady=40)
    tk.Label(frame_admin_login, text="Wprowadź kod PIN:", font=F_MAIN, bg=BG_COLOR, fg=TEXT_LIGHT).pack(pady=5)

    entry_pin = create_styled_entry(frame_admin_login, width=15)
    entry_pin.config(show="•") 
    entry_pin.pack(pady=10, ipady=5)

    def verify_pin():
        if entry_pin.get() == ADMIN_PIN:
            entry_pin.delete(0, tk.END) 
            show_frame(frame_admin_panel)
        else:
            messagebox.showerror("Błąd", "Zły PIN!")

    tk.Button(frame_admin_login, text="Zaloguj", font=F_BOLD, width=20, bg=ACCENT_GREEN, fg=BTN_TEXT, relief="flat",
              command=verify_pin).pack(pady=20)
    tk.Button(frame_admin_login, text="Powrót", font=F_MAIN, bg=BTN_SECONDARY, fg=TEXT_LIGHT, relief="flat",
              command=lambda: show_frame(frame_main)).pack()

    tk.Label(frame_admin_panel, text="PANEL ADMINISTRATORA", font=F_HEADER, bg=BG_COLOR, fg=ACCENT_GREEN).pack(pady=10)

    frame_add = tk.LabelFrame(frame_admin_panel, text="Dodaj / Aktualizuj Produkt", font=F_BOLD, bg=BG_COLOR,
                              fg=TEXT_LIGHT, bd=1, relief="solid")
    frame_add.pack(pady=10, fill="x", padx=20, ipady=10)

    # Używamy .grid() zamiast .pack() - to układa elementy w tabeli (wiersze i kolumny)
    tk.Label(frame_add, text="ID:", bg=BG_COLOR, fg=TEXT_LIGHT).grid(row=0, column=0, pady=5)
    entry_prod_id = create_styled_entry(frame_add, width=10)
    entry_prod_id.grid(row=0, column=1)

    tk.Label(frame_add, text="Nazwa:", bg=BG_COLOR, fg=TEXT_LIGHT).grid(row=0, column=2, pady=5)
    entry_prod_name = create_styled_entry(frame_add, width=15)
    entry_prod_name.grid(row=0, column=3)

    tk.Label(frame_add, text="Cena:", bg=BG_COLOR, fg=TEXT_LIGHT).grid(row=1, column=0, pady=5)
    entry_prod_price = create_styled_entry(frame_add, width=10)
    entry_prod_price.grid(row=1, column=1)

    tk.Label(frame_add, text="Ilość:", bg=BG_COLOR, fg=TEXT_LIGHT).grid(row=1, column=2, pady=5)
    entry_prod_qty = create_styled_entry(frame_add, width=15)
    entry_prod_qty.grid(row=1, column=3)

    def handle_add():
        ###  Obsługa wyjątków
        try:
            products.add_product(int(entry_prod_id.get()), entry_prod_name.get(), float(entry_prod_price.get()),
                                 int(entry_prod_qty.get()))
            messagebox.showinfo("Dodano", "Dodano produkt do bazy")
        except Exception:
            messagebox.showerror("Błąd", "Złe wprowadzone dane. Użyj cyfr dla ID, ceny i ilości.")

    tk.Button(frame_add, text="Zapisz do bazy", font=F_BOLD, bg=ACCENT_GREEN, fg=BTN_TEXT, relief="flat",
              command=handle_add).grid(row=2, column=0, columnspan=4, pady=15)

    frame_del = tk.LabelFrame(frame_admin_panel, text="Zarządzanie Klientami", font=F_BOLD, bg=BG_COLOR, fg=TEXT_LIGHT,
                              bd=1, relief="solid")
    frame_del.pack(pady=10, fill="x", padx=20, ipady=10)

    tk.Label(frame_del, text="Podaj ID:", bg=BG_COLOR, fg=TEXT_LIGHT).pack(side="left", padx=10)
    entry_del_cust = create_styled_entry(frame_del, width=10)
    entry_del_cust.pack(side="left", padx=5)

    tk.Button(frame_del, text="Usuń Klienta", font=F_BOLD, bg="#D32F2F", fg=TEXT_LIGHT, relief="flat",
              command=lambda: customers.delete_customer(entry_del_cust.get())).pack(side="left", padx=10)

    tk.Button(frame_admin_panel, text="Statystyki Sklepu", font=F_BOLD, bg=BTN_SECONDARY, fg=TEXT_LIGHT,
              relief="flat",
              command=lambda: messagebox.showinfo("Statystyki", monitor.generate_statistics_report())).pack(pady=15)
    tk.Button(frame_admin_panel, text="Wyloguj", font=F_MAIN, bg=BTN_SECONDARY, fg=TEXT_LIGHT, relief="flat",
              command=lambda: show_frame(frame_main)).pack(pady=5)

    tk.Label(frame_customer_menu, text="STREFA KLIENTA", font=F_HEADER, bg=BG_COLOR, fg=ACCENT_GREEN).pack(pady=40)
    tk.Button(frame_customer_menu, text="Nowy Klient (Zarejestruj się)", font=F_BOLD, width=30, height=2,
              bg=ACCENT_GREEN, fg=BTN_TEXT, relief="flat", command=lambda: show_frame(frame_new_customer)).pack(pady=10)
    tk.Button(frame_customer_menu, text="Zarejestrowany Klient (Zaloguj)", font=F_BOLD, width=30, height=2,
              bg=BTN_SECONDARY, fg=TEXT_LIGHT, relief="flat", command=lambda: show_frame(frame_reg_customer)).pack(
        pady=10)
    tk.Button(frame_customer_menu, text="Powrót", font=F_MAIN, bg=BTN_SECONDARY, fg=TEXT_LIGHT, relief="flat",
              command=lambda: show_frame(frame_main)).pack(pady=20)

    # ==========================================
    #                 REJESTRACJA
    # ==========================================
    tk.Label(frame_new_customer, text="REJESTRACJA", font=F_HEADER, bg=BG_COLOR, fg=ACCENT_GREEN).pack(pady=10)

    def add_register_field(text):
        tk.Label(frame_new_customer, text=text, font=F_MAIN, bg=BG_COLOR, fg=TEXT_GRAY).pack(pady=(5, 0))
        e = create_styled_entry(frame_new_customer, width=30)
        e.pack(pady=2, ipady=3)
        return e

    entry_new_name = add_register_field("Imię:")
    entry_new_surname = add_register_field("Nazwisko:")
    entry_new_city = add_register_field("Miasto:")
    entry_new_street = add_register_field("Ulica:")
    entry_new_birth = add_register_field("Rok urodzenia:")

    def handle_register():
        # global pozwala na modyfikację zmiennych, które zadeklarowaliśmy na samej górze pliku
        global current_customer_id, current_customer_is_adult

        name = entry_new_name.get()
        surname = entry_new_surname.get()
        city = entry_new_city.get()
        street = entry_new_street.get()
        birth_year = entry_new_birth.get()

        if name != "" and surname != "" and city != "" and street != "" and birth_year != "":
            ###Obsługa wyjątków
            try:
                age = CURRENT_YEAR - int(birth_year)
                if age >= 18:
                    current_customer_is_adult = True
                    status_wiek = "Pełnoletni"
                else:
                    current_customer_is_adult = False
                    status_wiek = "Niepełnoletni"

                # Rejestrujemy w pliku .csv
                current_customer_id = customers.register_customer(name, surname, int(birth_year))
                address.update_customer_address(current_customer_id, city, street)

                messagebox.showinfo("Sukces",
                                    f"Zarejestrowano!\nTwoje ID: {current_customer_id}\nStatus: {status_wiek}")

                build_shopping_screen()
                show_frame(frame_shopping)
            except ValueError:
                messagebox.showerror("Błąd", "Rok urodzenia musi być liczbą.")
        else:
            messagebox.showwarning("Błąd", "Wypełnij wszystkie pola.")

    tk.Button(frame_new_customer, text="Załóż konto i kupuj", font=F_BOLD, width=25, bg=ACCENT_GREEN, fg=BTN_TEXT,
              relief="flat", command=handle_register).pack(pady=20)
    tk.Button(frame_new_customer, text="Powrót", font=F_MAIN, bg=BTN_SECONDARY, fg=TEXT_LIGHT, relief="flat",
              command=lambda: show_frame(frame_customer_menu)).pack()

    # ==========================================
    #             LOGOWANIE KLIENTA
    # ==========================================
    tk.Label(frame_reg_customer, text="LOGOWANIE", font=F_HEADER, bg=BG_COLOR, fg=ACCENT_GREEN).pack(pady=40)
    tk.Label(frame_reg_customer, text="Wprowadź ID klienta:", font=F_MAIN, bg=BG_COLOR, fg=TEXT_LIGHT).pack(pady=5)

    entry_login_id = create_styled_entry(frame_reg_customer, width=15)
    entry_login_id.pack(pady=10, ipady=5)

    def handle_login():
        global current_customer_id, current_customer_is_adult
        try:
            cid = int(entry_login_id.get())
            # Odczytujemy dane klientów za pomocą biblioteki pandas
            df = customers.load_csv(customers.CUSTOMERS_FILE, ["ID", "Imie", "Nazwisko", "Rok_Urodzenia"])
            user_row = df[df["ID"] == cid]

            if not user_row.empty:
                current_customer_id = cid
                age = CURRENT_YEAR - int(user_row["Rok_Urodzenia"].values[0])
                if age >= 18:
                    current_customer_is_adult = True
                else:
                    current_customer_is_adult = False

                build_shopping_screen()
                show_frame(frame_shopping)
            else:
                messagebox.showerror("Błąd", "Brak ID w bazie.")
        except ValueError:
            messagebox.showerror("Błąd", "ID musi być liczbą.")

    tk.Button(frame_reg_customer, text="Zaloguj do sklepu", font=F_BOLD, width=20, bg=ACCENT_GREEN, fg=BTN_TEXT,
              relief="flat", command=handle_login).pack(pady=20)
    tk.Button(frame_reg_customer, text="Powrót", font=F_MAIN, bg=BTN_SECONDARY, fg=TEXT_LIGHT, relief="flat",
              command=lambda: show_frame(frame_customer_menu)).pack()

    # ==========================================
    #             SKLEP WIZUALNY 
    # ==========================================
    def build_shopping_screen():
        # Metoda (destroy) sprawia, ze przy ponownym logowaniu sklep wygenerowal sie na nowo #
        for widget in frame_shopping.winfo_children():
            widget.destroy()

        if current_customer_is_adult == True:
            wiek_info = "Pełnoletni"
        else:
            wiek_info = "Niepełnoletni"

        top_bar = tk.Frame(frame_shopping, bg=CARD_BG)
        top_bar.pack(fill="x", pady=(0, 10))

        tk.Label(top_bar, text="ŻABKA", font=F_HEADER, bg=CARD_BG, fg=ACCENT_GREEN).pack(pady=(10, 0))
        tk.Label(top_bar, text=f"Zalogowano: ID {current_customer_id} {wiek_info}", font=("Segoe UI", 9), bg=CARD_BG,
                 fg=TEXT_GRAY).pack(pady=(0, 10))

        # Ładujemy Excela z produktami
        df = products.load_products()
        if df.empty:
            tk.Label(frame_shopping, text="Brak produktu w bazie.", font=F_MAIN, bg=BG_COLOR, fg="#FF5555").pack(
                pady=20)
            tk.Button(frame_shopping, text="Wyloguj", font=F_MAIN, bg=BTN_SECONDARY, fg=TEXT_LIGHT, relief="flat",
                      command=lambda: show_frame(frame_main)).pack()
            return

        cart_vars = {}  # Przechowuje zmienne ilościowe (woda)
        prices_map = {}  # Przechowuje ceny produktów 

        products_grid = tk.Frame(frame_shopping, bg=BG_COLOR)
        products_grid.pack(pady=5)

        row_idx = 0
        col_idx = 0

        # StringVar() to zmienna tkintera. Jeśli zmodyfikujesz ją w kodzie,
        # automatycznie zaktualizuje się tekst na przycisku "Kup"
        btn_checkout_text = tk.StringVar()
        btn_checkout_text.set("POTWIERDŹ ZAKUP (0.00 zł)")

        def update_total_price():
            total = 0.0
            for nazwa_produktu in cart_vars:
                ilosc = cart_vars[nazwa_produktu].get()
                cena = prices_map[nazwa_produktu]
                total = total + (ilosc * cena)
                
            btn_checkout_text.set(f"POTWIERDŹ ZAKUP ({total:.2f} zł)")

        for index, row in df.iterrows():
            p_name = row["Nazwa"]
            p_price = float(row["Cena"])
            p_stock = row["Ilosc"]

            # tk.IntVar() śledzi ilość wyklikaną przez klienta (+/-)
            cart_vars[p_name] = tk.IntVar(value=0)
            prices_map[p_name] = p_price

            card = tk.Frame(products_grid, bg=CARD_BG, padx=10, pady=10, relief="flat")
            card.grid(row=row_idx, column=col_idx, padx=8, pady=8)

            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            image_filename = os.path.join(BASE_DIR, "images", f"{p_name.lower()}.jpg")
            if os.path.exists(image_filename):
                img = Image.open(image_filename).resize((80, 80))
                photo = ImageTk.PhotoImage(img)
                img_label = tk.Label(card, image=photo, bg=CARD_BG)
                img_label.image = photo
                img_label.pack(pady=2)
            else:
                tk.Label(card, text="Brak zdjęcia", bg=ENTRY_BG, fg=TEXT_GRAY, font=("Segoe UI", 9), width=12,
                         height=5).pack(pady=2)

            tk.Label(card, text=f"{p_name}", font=F_BOLD, bg=CARD_BG, fg=TEXT_LIGHT).pack(pady=(5, 0))
            tk.Label(card, text=f"{p_price:.2f} zł", font=F_PRICE, bg=CARD_BG, fg=ACCENT_GREEN).pack()
            tk.Label(card, text=f"Dostępne: {p_stock}", font=("Segoe UI", 8), bg=CARD_BG, fg=TEXT_GRAY).pack(pady=2)

            ctrl_frame = tk.Frame(card, bg=CARD_BG)
            ctrl_frame.pack(pady=5)

            # Funkcja sterująca  + i -
            def change_qty(name, delta, max_stock):
                global current_customer_is_adult

                zakazane_slowa = ["piwo", "wódka", "wino", "alkohol", "energetyk", "monster", "tiger"]
                is_restricted = False
                for slowo in zakazane_slowa:
                    if slowo in name.lower():
                        is_restricted = True
                        break 

                if delta > 0 and is_restricted and not current_customer_is_adult:
                    messagebox.showwarning("Weryfikacja wieku",
                                           "Produkt przeznaczony wyłącznie dla osób pełnoletnich (+18).")
                    return 

                # dodanie delty (+1 lub -1)
                current_val = cart_vars[name].get()
                new_val = current_val + delta

                # Zabezpieczenie przed wpisaniem wartości mniejszej od 0, lub większej niż magazyn
                if new_val >= 0 and new_val <= max_stock:
                    cart_vars[name].set(new_val)
                    update_total_price()  
                    
            # Przyciski +/-. Użyto funkcji lambda z argumentami, aby
            # przypisać dany przycisk do konkretnego produktu z pętli.
            tk.Button(ctrl_frame, text=" − ", font=F_BOLD, bg=ENTRY_BG, fg=TEXT_LIGHT, relief="flat",
                      command=lambda n=p_name, ms=p_stock: change_qty(n, -1, ms)).pack(side="left", padx=5)
            tk.Label(ctrl_frame, textvariable=cart_vars[p_name], font=F_BOLD, width=3, bg=CARD_BG, fg=TEXT_LIGHT).pack(
                side="left")
            tk.Button(ctrl_frame, text=" + ", font=F_BOLD, bg=ENTRY_BG, fg=TEXT_LIGHT, relief="flat",
                      command=lambda n=p_name, ms=p_stock: change_qty(n, 1, ms)).pack(side="left", padx=5)

            # Algorytm zawijania wierszy (maksymalnie 3 kafelki w jednej poziomej linii)
            col_idx += 1
            if col_idx > 2:
                col_idx = 0
                row_idx += 1

        def handle_checkout():
            items_to_buy = []
            for nazwa_produktu in cart_vars:
                ilosc = cart_vars[nazwa_produktu].get()
                if ilosc > 0:
                    items_to_buy.append((nazwa_produktu, ilosc))

            if len(items_to_buy) == 0:
                messagebox.showwarning("Koszyk", "Koszyk jest pusty.")
                return

            receipt_text = f"--- PARAGON ---\n\n"
            receipt_text += f"Klient ID: {current_customer_id}\n"
            receipt_text += f"---------------------------------\n"

            total_sum = 0.0
            for name, qty in items_to_buy:
                item_total = qty * prices_map[name]
                total_sum += item_total
                receipt_text += f" {name} (x{qty}) \t\t {item_total:.2f} zł\n"

            receipt_text += f"---------------------------------\n"
            receipt_text += f" DO ZAPŁATY: \t\t {total_sum:.2f} zł\n\n"

            ### Wykorzystanie funkcji wielu zmiennych wejściowych
            ### (*) rozpakowuje listę na pojedyncze argumenty.
            customers.buy_product(current_customer_id, *items_to_buy)
            messagebox.showinfo("Transakcja zrealizowana", receipt_text)

            build_shopping_screen()

        # Główny przycisk KUP. Podpięty do zmiennej btn_checkout_text, by aktualizował kwotę
        tk.Button(frame_shopping, textvariable=btn_checkout_text, command=handle_checkout, font=F_BOLD, bg=ACCENT_GREEN,
                  fg=BTN_TEXT, relief="flat", width=30, height=2).pack(pady=15)

        def wyloguj_klienta():
            global current_customer_id
            current_customer_id = None
            show_frame(frame_main)

        tk.Button(frame_shopping, text="Wyloguj", font=F_MAIN, bg=BTN_SECONDARY, fg=TEXT_LIGHT, relief="flat",
                  command=wyloguj_klienta).pack(pady=5)

    show_frame(frame_main)
    root.mainloop()


if __name__ == "__main__":
    start_app()
