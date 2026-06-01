
ModuĹ: gui
ZarzÄdza interfejsem graficznym.
Motyw: Nowoczesny Dark Mode (Grafit + Neonowa ZieleĹ Ĺťabki).
"""

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os
from PIL import Image, ImageTk, ImageDraw  
import products
import customers
import address
import monitor

# ==========================================
# KONFIGURACJA STYLU (MOTYW POS DARK MODE)
# ==========================================
BG_COLOR = "#1E1E1E"  # Ciemny grafit (gĹĂłwne tĹo)
CARD_BG = "#2D2D30"  # Nieco jaĹniejszy grafit (kafelki i ramki)
ENTRY_BG = "#333337"  # TĹo dla pĂłl tekstowych
TEXT_LIGHT = "#FFFFFF"  # BiaĹy tekst gĹĂłwny
TEXT_GRAY = "#AAAAAA"  # Szary tekst pomocniczy
ACCENT_GREEN = "#00E676"  # Neonowa zieleĹ (gĹĂłwny akcent)
BTN_TEXT = "#000000"  # Czarny tekst na zielonych przyciskach
BTN_SECONDARY = "#3E3E42"  # Kolor dla przyciskĂłw "PowrĂłt" itp.

F_MAIN = ("Segoe UI", 11)
F_BOLD = ("Segoe UI", 11, "bold")
F_HEADER = ("Segoe UI", 18, "bold")
F_PRICE = ("Segoe UI", 11, "bold")

ADMIN_PIN = "1234"
current_customer_id = None
current_customer_is_adult = False
CURRENT_YEAR = 2026


# ==========================================
# FUNKCJA GENERUJÄCA ZAOKRÄGLONE PRZYCISKI
# ==========================================
def create_rounded_button(parent, text, font, bg_color, fg_color, command, width_px, height_px, radius=10, textvariable=None):
    """
    Dynamicznie generuje gĹadki, zaokrÄglony przycisk przy uĹźyciu biblioteki PIL.
    Wymiary podawane sÄ bezpoĹrednio w pikselach (px).
    """
    img = Image.new("RGBA", (width_px, height_px), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([0, 0, width_px, height_px], radius=radius, fill=bg_color)
    photo = ImageTk.PhotoImage(img)
    
    try:
        p_bg = parent.cget("bg")
    except:
        p_bg = BG_COLOR
        
    btn = tk.Button(parent, font=font, fg=fg_color, image=photo, compound="center",
                    relief="flat", bg=p_bg, activebackground=p_bg,
                    activeforeground=fg_color, bd=0, highlightthickness=0, command=command)
    
    if textvariable:
        btn.config(textvariable=textvariable)
    else:
        btn.config(text=text)
        
    btn.image = photo  
    return btn


def start_app():
    root = tk.Tk()
    root.title("Sklep Ĺťabka Online ")
    root.geometry("600x800")
    root.configure(bg=BG_COLOR)

    # Konfiguracja nowoczesnego wyglÄdu dla paska przewijania (Scrollbar)
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Vertical.TScrollbar",
                    troughcolor=BG_COLOR,      
                    background=CARD_BG,        
                    arrowcolor=ACCENT_GREEN,   
                    bordercolor=BG_COLOR,      
                    lightcolor=CARD_BG,
                    darkcolor=CARD_BG,
                    gripcount=0,
                    thickness=14)              

    # ==========================================
    # LOGIKA PRZEĹÄCZANIA EKRANĂW
    # ==========================================
    def hide_all_frames():
        for frame in (frame_main, frame_admin_login, frame_admin_panel,
                      frame_customer_menu, frame_new_customer,
                      frame_reg_customer, frame_shopping):
            frame.pack_forget()

    def show_frame(frame):
        hide_all_frames()
        frame.pack(fill="both", expand=True, pady=10)

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
    # EKRAN 1: MENU GĹĂWNE (POPRAWIONE LOGO)
    # ==========================================
    try:
        # Dynamiczne pobranie ĹcieĹźki do folderu 'images' dla Logo
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(BASE_DIR, "images", "Zabka_logo_.jpg")
        
        img_logo = Image.open(logo_path)
        img_logo = img_logo.resize((200, 140))  
        logo_tk = ImageTk.PhotoImage(img_logo)
        lbl_logo = tk.Label(frame_main, image=logo_tk, bg=BG_COLOR)
        lbl_logo.image = logo_tk
        lbl_logo.pack(pady=30)
    except FileNotFoundError:
        pass
        
    create_rounded_button(frame_main, "Strefa Klienta", F_BOLD, ACCENT_GREEN, BTN_TEXT, 
                          lambda: show_frame(frame_customer_menu), 260, 50, 15).pack(pady=10)
                          
    create_rounded_button(frame_main, "Panel Administratora", F_BOLD, BTN_SECONDARY, TEXT_LIGHT, 
                          lambda: show_frame(frame_admin_login), 260, 50, 15).pack(pady=10)

    # ==========================================
    # EKRAN 2: LOGOWANIE ADMINA
    # ==========================================
    tk.Label(frame_admin_login, text="LOGOWANIE ADMINA", font=F_HEADER, bg=BG_COLOR, fg=ACCENT_GREEN).pack(pady=40)
    tk.Label(frame_admin_login, text="WprowadĹş kod PIN:", font=F_MAIN, bg=BG_COLOR, fg=TEXT_LIGHT).pack(pady=5)

    entry_pin = create_styled_entry(frame_admin_login, width=15)
    entry_pin.config(show="â˘")
    entry_pin.pack(pady=10, ipady=5)

    def verify_pin():
        if entry_pin.get() == ADMIN_PIN:
            entry_pin.delete(0, tk.END)
            show_frame(frame_admin_panel)
        else:
            messagebox.showerror("BĹÄd", "ZĹy PIN!")

    create_rounded_button(frame_admin_login, "Zaloguj", F_BOLD, ACCENT_GREEN, BTN_TEXT, verify_pin, 200, 42, 12).pack(pady=20)
    create_rounded_button(frame_admin_login, "PowrĂłt", F_MAIN, BTN_SECONDARY, TEXT_LIGHT, lambda: show_frame(frame_main), 200, 42, 12).pack()

    # ==========================================
    # EKRAN 3: PANEL ADMINISTRATORA
    # ==========================================
    tk.Label(frame_admin_panel, text="PANEL ADMINISTRATORA", font=F_HEADER, bg=BG_COLOR, fg=ACCENT_GREEN).pack(pady=20)

    # --- SEKCJA: DODAJ / AKTUALIZUJ PRODUKT ---
    frame_add = tk.LabelFrame(frame_admin_panel, text="Dodaj / Aktualizuj Produkt", font=F_BOLD, bg=BG_COLOR,
                              fg=TEXT_LIGHT, bd=1, relief="solid", padx=15, pady=10)
    frame_add.pack(pady=15, fill="x", padx=25)

    frame_add.grid_columnconfigure(0, weight=1)
    frame_add.grid_columnconfigure(1, weight=2)
    frame_add.grid_columnconfigure(2, weight=1)
    frame_add.grid_columnconfigure(3, weight=2)

    entry_prod_id = create_styled_entry(frame_add, width=12)
    entry_prod_name = create_styled_entry(frame_add, width=12)
    entry_prod_price = create_styled_entry(frame_add, width=12)
    entry_prod_qty = create_styled_entry(frame_add, width=12)

    tk.Label(frame_add, text="ID:", font=F_MAIN, bg=BG_COLOR, fg=TEXT_LIGHT).grid(row=0, column=0, sticky="e", padx=5, pady=8)
    entry_prod_id.grid(row=0, column=1, sticky="ew", padx=5, pady=8, ipady=3)
    
    tk.Label(frame_add, text="Nazwa:", font=F_MAIN, bg=BG_COLOR, fg=TEXT_LIGHT).grid(row=0, column=2, sticky="e", padx=5, pady=8)
    entry_prod_name.grid(row=0, column=3, sticky="ew", padx=5, pady=8, ipady=3)
    
    tk.Label(frame_add, text="Cena:", font=F_MAIN, bg=BG_COLOR, fg=TEXT_LIGHT).grid(row=1, column=0, sticky="e", padx=5, pady=8)
    entry_prod_price.grid(row=1, column=1, sticky="ew", padx=5, pady=8, ipady=3)
    
    tk.Label(frame_add, text="IloĹÄ:", font=F_MAIN, bg=BG_COLOR, fg=TEXT_LIGHT).grid(row=1, column=2, sticky="e", padx=5, pady=8)
    entry_prod_qty.grid(row=1, column=3, sticky="ew", padx=5, pady=8, ipady=3)

    def handle_add():
        try:
            products.add_product(int(entry_prod_id.get()), entry_prod_name.get(), float(entry_prod_price.get()),
                                 int(entry_prod_qty.get()))
            messagebox.showinfo("Sukces", "PomyĹlnie dodano produkt do bazy!")
            for entry in (entry_prod_id, entry_prod_name, entry_prod_price, entry_prod_qty):
                entry.delete(0, tk.END)
        except:
            messagebox.showerror("BĹÄd", "SprawdĹş wprowadzone dane!")

    create_rounded_button(frame_add, "Zapisz do bazy", F_BOLD, ACCENT_GREEN, BTN_TEXT, handle_add, 200, 42, 12).grid(row=2, column=0, columnspan=4, pady=15)

    # --- SEKCJA: ZARZÄDZANIE KLIENTAMI ---
    frame_del = tk.LabelFrame(frame_admin_panel, text="ZarzÄdzanie Klientami", font=F_BOLD, bg=BG_COLOR, fg=TEXT_LIGHT,
                              bd=1, relief="solid", padx=15, pady=15)
    frame_del.pack(pady=15, fill="x", padx=25)

    frame_del.grid_columnconfigure(0, weight=2)
    frame_del.grid_columnconfigure(1, weight=2)
    frame_del.grid_columnconfigure(2, weight=3)

    entry_del_cust = create_styled_entry(frame_del, width=12)

    tk.Label(frame_del, text="Podaj ID klienta:", font=F_MAIN, bg=BG_COLOR, fg=TEXT_LIGHT).grid(row=0, column=0, sticky="e", padx=5)
    entry_del_cust.grid(row=0, column=1, sticky="ew", padx=10, ipady=3)
    
    def handle_delete_customer():
        cid = entry_del_cust.get()
        if cid:
            if customers.delete_customer(cid):
                messagebox.showinfo("Sukces", f"UsuniÄto klienta o ID: {cid}")
                entry_del_cust.delete(0, tk.END)
            else:
                messagebox.showerror("BĹÄd", "Nie udaĹo siÄ usunÄÄ klienta. SprawdĹş ID.")
        else:
            messagebox.showwarning("BĹÄd", "WprowadĹş ID klienta!")

    create_rounded_button(frame_del, "UsuĹ Klienta", F_BOLD, "#D32F2F", TEXT_LIGHT, handle_delete_customer, 130, 36, 10).grid(row=0, column=2, sticky="w", padx=5)

    # --- DOLNE PRZYCISKI PANELU ---
    create_rounded_button(frame_admin_panel, "đ Statystyki Sklepu", F_BOLD, BTN_SECONDARY, TEXT_LIGHT, 
                          lambda: messagebox.showinfo("Statystyki", monitor.generate_statistics_report()), 260, 50, 15).pack(pady=20)
              
    create_rounded_button(frame_admin_panel, "Wyloguj", F_MAIN, BTN_SECONDARY, TEXT_LIGHT, 
                          lambda: show_frame(frame_main), 260, 42, 12).pack(pady=5)

    # ==========================================
    # EKRAN 4: MENU KLIENTA
    # ==========================================
    tk.Label(frame_customer_menu, text="STREFA KLIENTA", font=F_HEADER, bg=BG_COLOR, fg=ACCENT_GREEN).pack(pady=40)
    
    create_rounded_button(frame_customer_menu, "Nowy Klient (Zarejestruj siÄ)", F_BOLD, ACCENT_GREEN, BTN_TEXT, 
                          lambda: show_frame(frame_new_customer), 300, 50, 15).pack(pady=10)
                          
    create_rounded_button(frame_customer_menu, "Zarejestrowany Klient (Zaloguj)", F_BOLD, BTN_SECONDARY, TEXT_LIGHT, 
                          lambda: show_frame(frame_reg_customer), 300, 50, 15).pack(pady=10)
                          
    create_rounded_button(frame_customer_menu, "PowrĂłt", F_MAIN, BTN_SECONDARY, TEXT_LIGHT, 
                          lambda: show_frame(frame_main), 300, 50, 15).pack(pady=20)

    # ==========================================
    # EKRAN 5: REJESTRACJA
    # ==========================================
    tk.Label(frame_new_customer, text="REJESTRACJA", font=F_HEADER, bg=BG_COLOR, fg=ACCENT_GREEN).pack(pady=10)

    def add_register_field(text):
        tk.Label(frame_new_customer, text=text, font=F_MAIN, bg=BG_COLOR, fg=TEXT_GRAY).pack(pady=(5, 0))
        e = create_styled_entry(frame_new_customer, width=30)
        e.pack(pady=2, ipady=3)
        return e

    entry_new_name = add_register_field("ImiÄ:")
    entry_new_surname = add_register_field("Nazwisko:")
    entry_new_city = add_register_field("Miasto:")
    entry_new_street = add_register_field("Ulica:")
    entry_new_birth = add_register_field("Rok urodzenia (np. 1995):")

    def handle_register():
        global current_customer_id, current_customer_is_adult
        name, surname, city, street, birth_year = entry_new_name.get(), entry_new_surname.get(), entry_new_city.get(), entry_new_street.get(), entry_new_birth.get()

        if all([name, surname, city, street, birth_year]):
            try:
                age = CURRENT_YEAR - int(birth_year)
                current_customer_is_adult = (age >= 18)
                current_customer_id = customers.register_customer(name, surname, int(birth_year))
                address.update_customer_address(current_customer_id, city, street)
                status_wiek = "PeĹnoletni" if current_customer_is_adult else "NiepeĹnoletni"
                messagebox.showinfo("Sukces",
                                    f"Zarejestrowano!\nTwoje ID: {current_customer_id}\nStatus: {status_wiek}")
                build_shopping_screen()
                show_frame(frame_shopping)
            except ValueError:
                messagebox.showerror("BĹÄd", "Rok urodzenia musi byÄ liczbÄ!")
        else:
            messagebox.showwarning("BĹÄd", "WypeĹnij wszystkie pola!")

    create_rounded_button(frame_new_customer, "ZaĹĂłĹź konto i kupuj", F_BOLD, ACCENT_GREEN, BTN_TEXT, handle_register, 250, 48, 14).pack(pady=20)
    create_rounded_button(frame_new_customer, "PowrĂłt", F_MAIN, BTN_SECONDARY, TEXT_LIGHT, lambda: show_frame(frame_customer_menu), 250, 42, 12).pack()

    # ==========================================
    # EKRAN 6: LOGOWANIE KLIENTA
    # ==========================================
    tk.Label(frame_reg_customer, text="LOGOWANIE", font=F_HEADER, bg=BG_COLOR, fg=ACCENT_GREEN).pack(pady=40)
    tk.Label(frame_reg_customer, text="WprowadĹş ID klienta:", font=F_MAIN, bg=BG_COLOR, fg=TEXT_LIGHT).pack(pady=5)

    entry_login_id = create_styled_entry(frame_reg_customer, width=15)
    entry_login_id.pack(pady=10, ipady=5)

    def handle_login():
        global current_customer_id, current_customer_is_adult
        try:
            cid = int(entry_login_id.get())
            df = customers.load_csv(customers.CUSTOMERS_FILE, ["ID", "Imie", "Nazwisko", "Rok_Urodzenia"])
            user_row = df[df["ID"] == cid]

            if not user_row.empty:
                current_customer_id = cid
                age = CURRENT_YEAR - int(user_row["Rok_Urodzenia"].values[0])
                current_customer_is_adult = (age >= 18)
                build_shopping_screen()
                show_frame(frame_shopping)
            else:
                messagebox.showerror("BĹÄd", "Brak ID w bazie!")
        except ValueError:
            messagebox.showerror("BĹÄd", "ID musi byÄ liczbÄ!")

    create_rounded_button(frame_reg_customer, "Zaloguj do sklepu", F_BOLD, ACCENT_GREEN, BTN_TEXT, handle_login, 220, 46, 14).pack(pady=20)
    create_rounded_button(frame_reg_customer, "PowrĂłt", F_MAIN, BTN_SECONDARY, TEXT_LIGHT, lambda: show_frame(frame_customer_menu), 220, 42, 12).pack()

    # ==========================================
    # EKRAN 7: SKLEP WIZUALNY (RESPONSYWNY KOSZYK ĹťABKI)
    # ==========================================
    def build_shopping_screen():
        for widget in frame_shopping.winfo_children():
            widget.destroy()

        wiek_info = "(Konto +18)" if current_customer_is_adult else "(Konto <18)"

        # ----------------------------------------------------
        # 1. PASEK GĂRNY
        # ----------------------------------------------------
        top_bar = tk.Frame(frame_shopping, bg=CARD_BG)
        top_bar.pack(side="top", fill="x")

        tk.Label(top_bar, text="ĹťABKA", font=F_HEADER, bg=CARD_BG, fg=ACCENT_GREEN).pack(pady=(10, 0))
        tk.Label(top_bar, text=f"Zalogowano: ID {current_customer_id} {wiek_info}", font=("Segoe UI", 9), bg=CARD_BG,
                 fg=TEXT_GRAY).pack(pady=(0, 10))

        df = products.load_products()
        if df.empty:
            tk.Label(frame_shopping, text="Brak asortymentu w bazie.", font=F_MAIN, bg=BG_COLOR, fg="#FF5555").pack(pady=20)
            create_rounded_button(frame_shopping, "Wyloguj", F_MAIN, BTN_SECONDARY, TEXT_LIGHT, lambda: show_frame(frame_main), 200, 42, 12).pack()
            return

        # ----------------------------------------------------
        # 2. PASEK DOLNY
        # ----------------------------------------------------
        bottom_bar = tk.Frame(frame_shopping, bg=BG_COLOR)
        bottom_bar.pack(side="bottom", fill="x", pady=10)

        # ----------------------------------------------------
        # 3. ĹRODKOWY OBSZAR PRZEWIJANY
        # ----------------------------------------------------
        canvas_container = tk.Frame(frame_shopping, bg=BG_COLOR)
        canvas_container.pack(side="top", fill="both", expand=True)

        canvas = tk.Canvas(canvas_container, bg=BG_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_container, orient="vertical", command=canvas.yview, style="Vertical.TScrollbar")
        
        scrollable_frame = tk.Frame(canvas, bg=BG_COLOR)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        cart_vars = {}
        prices_map = {}

        products_grid = tk.Frame(scrollable_frame, bg=BG_COLOR)
        products_grid.pack(pady=5)  

        cards = []  

        for index, row in df.iterrows():
            p_name = row["Nazwa"]
            p_price = float(row["Cena"])
            p_stock = row["Ilosc"]

            cart_vars[p_name] = tk.IntVar(value=0)
            prices_map[p_name] = p_price

            card = tk.Frame(products_grid, bg=CARD_BG, padx=10, pady=10, relief="flat")
            cards.append(card)

            # POPRAWIONE: Szukanie obrazkĂłw produktĂłw wewnÄtrz podfolderu 'images'
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            image_filename = os.path.join(BASE_DIR, "images", f"{p_name.lower()}.jpg")
            
            if os.path.exists(image_filename):
                img = Image.open(image_filename).resize((80, 80))
                photo = ImageTk.PhotoImage(img)
                img_label = tk.Label(card, image=photo, bg=CARD_BG)
                img_label.image = photo
                img_label.pack(pady=2)
            else:
                tk.Label(card, text="Brak zdjÄcia", bg=ENTRY_BG, fg=TEXT_GRAY, font=("Segoe UI", 9), width=12,
                         height=5).pack(pady=2)

            tk.Label(card, text=f"{p_name}", font=F_BOLD, bg=CARD_BG, fg=TEXT_LIGHT).pack(pady=(5, 0))
            tk.Label(card, text=f"{p_price:.2f} zĹ", font=F_PRICE, bg=CARD_BG, fg=ACCENT_GREEN).pack()
            tk.Label(card, text=f"DostÄpne: {p_stock}", font=("Segoe UI", 8), bg=CARD_BG, fg=TEXT_GRAY).pack(pady=2)

            ctrl_frame = tk.Frame(card, bg=CARD_BG)
            ctrl_frame.pack(pady=5)

            def change_qty(name, delta, max_stock):
                global current_customer_is_adult
                zakazane_slowa = ["piwo", "wĂłdka", "wino", "alkohol", "energetyk", "monster", "tiger", "wojanek"]
                is_restricted = any(slowo in name.lower() for slowo in zakazane_slowa)

                if delta > 0 and is_restricted and not current_customer_is_adult:
                    messagebox.showwarning("Weryfikacja wieku",
                                           "Produkt przeznaczony wyĹÄcznie dla osĂłb peĹnoletnich (+18).")
                    return

                current_val = cart_vars[name].get()
                new_val = current_val + delta
                if 0 <= new_val <= max_stock:
                    cart_vars[name].set(new_val)
                    update_total_price()

            create_rounded_button(ctrl_frame, " â ", F_BOLD, ENTRY_BG, TEXT_LIGHT, 
                                  lambda n=p_name, ms=p_stock: change_qty(n, -1, ms), 35, 35, 8).pack(side="left", padx=5)
                                  
            tk.Label(ctrl_frame, textvariable=cart_vars[p_name], font=F_BOLD, width=3, bg=CARD_BG, fg=TEXT_LIGHT).pack(side="left")
            
            create_rounded_button(ctrl_frame, " + ", F_BOLD, ENTRY_BG, TEXT_LIGHT, 
                                  lambda n=p_name, ms=p_stock: change_qty(n, 1, ms), 35, 35, 8).pack(side="left", padx=5)

        btn_checkout_text = tk.StringVar()
        btn_checkout_text.set("POTWIERDĹš ZAKUP (0.00 zĹ)")

        def update_total_price():
            total = sum(cart_vars[name].get() * prices_map[name] for name in cart_vars)
            btn_checkout_text.set(f"POTWIERDĹš ZAKUP ({total:.2f} zĹ)")

        def rearrange_cards(event=None):
            canvas_width = canvas.winfo_width()
            if canvas_width < 100:  
                canvas_width = 580
            
            card_space = 175  
            columns = max(1, canvas_width // card_space)
            
            for idx, c in enumerate(cards):
                r = idx // columns
                col = idx % columns
                c.grid(row=r, column=col, padx=8, pady=8)

        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
            rearrange_cards()

        canvas.bind("<Configure>", on_canvas_configure)

        def handle_checkout():
            items_to_buy = [(name, var_obj.get()) for name, var_obj in cart_vars.items() if var_obj.get() > 0]
            if not items_to_buy:
                messagebox.showwarning("Koszyk", "Koszyk jest pusty.")
                return

            receipt_text = f"--- PARAGON ---\n\n"
            receipt_text += f"Klient ID: {current_customer_id}\n"
            receipt_text += f"---------------------------------\n"

            total_sum = 0.0
            for name, qty in items_to_buy:
                item_total = qty * prices_map[name]
                total_sum += item_total
                receipt_text += f" {name} (x{qty}) \t\t {item_total:.2f} zĹ\n"

            receipt_text += f"---------------------------------\n"
            receipt_text += f" DO ZAPĹATY: \t\t {total_sum:.2f} zĹ\n\n"

            customers.buy_product(current_customer_id, *items_to_buy)
            messagebox.showinfo("Transakcja zrealizowana", receipt_text)
            
            canvas.unbind_all("<MouseWheel>")
            build_shopping_screen()

        def handle_logout():
            canvas.unbind_all("<MouseWheel>")
            globals().update(current_customer_id=None)
            show_frame(frame_main)

        # ----------------------------------------------------
        # PRZYCISKI AKCJI (DOLNY ZABLOKOWANY PANEL)
        # ----------------------------------------------------
        create_rounded_button(bottom_bar, "", F_BOLD, ACCENT_GREEN, BTN_TEXT, handle_checkout, 
                              320, 52, 15, textvariable=btn_checkout_text).pack(pady=5)
        
        create_rounded_button(bottom_bar, "Wyloguj", F_MAIN, BTN_SECONDARY, TEXT_LIGHT, handle_logout, 320, 42, 12).pack(pady=5)

    show_frame(frame_main)
    root.mainloop()


if __name__ == "__main__":
    start_app()
