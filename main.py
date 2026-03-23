import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
from firebase_config import save_user_to_firebase, check_user_in_firebase


def okno_vybora():
    window = tk.Tk()
    window.title("Выбор действия")
    window.geometry("400x350")
    icon = PhotoImage(file="logo.png")
    window.iconphoto(False, icon)
    tk.Button(window, text="Войти", command=lambda: (window.destroy(), create_login_window())).pack(pady=5)
    tk.Button(window, text="Зарегистрироваться",
              command=lambda: (window.destroy(), create_registration_window())).pack(pady=5)

    window.mainloop()


def create_registration_window():
    reg_window = tk.Tk()
    reg_window.title("Регистрация")
    reg_window.geometry("400x350")
    icon = PhotoImage(file="logo.png")
    reg_window.iconphoto(False, icon)

    # Поля регистрации
    tk.Label(reg_window, text="Логин:").pack(pady=5)
    login_entry = tk.Entry(reg_window, width=30)
    login_entry.pack(pady=5)

    tk.Label(reg_window, text="Пароль:").pack(pady=5)
    password_entry = tk.Entry(reg_window, width=30, show="*")
    password_entry.pack(pady=5)

    tk.Label(reg_window, text="Подтвердите пароль:").pack(pady=5)
    confirm_entry = tk.Entry(reg_window, width=30, show="*")
    confirm_entry.pack(pady=5)

    def register_user():
        login = login_entry.get()
        password = password_entry.get()
        confirm = confirm_entry.get()

        # Валидация
        if not login or not password:
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return

        if password != confirm:
            messagebox.showerror("Ошибка", "Пароли не совпадают!")
            return

        # Отправка данных в Firebase
        if save_user_to_firebase(login, password):
            messagebox.showinfo("Успех", "Регистрация прошла успешно!")
            reg_window.destroy()
            create_login_window()
        else:
            messagebox.showerror("Ошибка", "Не удалось сохранить данные. Попробуйте позже.")

    tk.Button(reg_window, text="Зарегистрироваться", command=register_user).pack(pady=10)

    reg_window.mainloop()


def create_login_window():
    login_window = tk.Tk()
    login_window.title("Вход")
    login_window.geometry("300x200")
    icon = PhotoImage(file="logo.png")
    login_window.iconphoto(False, icon)

    tk.Label(login_window, text="Логин:").pack(pady=5)
    login_entry = tk.Entry(login_window, width=30)
    login_entry.pack(pady=5)

    tk.Label(login_window, text="Пароль:").pack(pady=5)
    password_entry = tk.Entry(login_window, width=30, show="*")
    password_entry.pack(pady=5)

    def login_action():
        login = login_entry.get()
        password = password_entry.get()

        if check_user_in_firebase(login, password):
            messagebox.showinfo("Успех", "Авторизация пройдена!")
            login_window.destroy()
            create_main_window()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль!")

    tk.Button(login_window, text="Вход", command=login_action).pack(pady=10)

    login_window.mainloop()


def create_search_window(main_window, font_var, preview_label, font_list):
    """Создаёт окно поиска шрифтов"""
    search_window = tk.Toplevel(main_window)
    search_window.title("Поиск шрифтов")
    search_window.geometry("400x500")
    search_window.resizable(False, False)
    icon = PhotoImage(file="logo.png")
    search_window.iconphoto(False, icon)

    # Поле поиска
    tk.Label(search_window, text="Введите название шрифта:").pack(pady=5)
    search_entry = tk.Entry(search_window, width=40)
    search_entry.pack(pady=5)

    # Список результатов поиска
    listbox = tk.Listbox(search_window, height=20, width=50)
    listbox.pack(pady=10, fill=tk.BOTH, expand=True)

    # Статус — сколько найдено шрифтов
    status_label = tk.Label(search_window, text="Найдено шрифтов: 0")
    status_label.pack(pady=5)

    def update_list(event=None):
        """Обновляет список при вводе в поле поиска"""
        search_text = search_entry.get().lower()
        listbox.delete(0, tk.END)

        # Фильтруем список по введённому тексту
        filtered_fonts = [font for font in font_list if search_text in font.lower()]
        for font in filtered_fonts:
            listbox.insert(tk.END, font)
        status_label.config(text=f"Найдено шрифтов: {len(filtered_fonts)}")

    def select_font():
        """Обрабатывает выбор шрифта из списка"""
        selection = listbox.curselection()
        if selection:
            selected_font = listbox.get(selection[0])
            font_var.set(selected_font)
            preview_label.config(font=(selected_font, 12))
            search_window.destroy()  # Закрываем окно поиска после выбора

    # Привязываем обновление списка к вводу текста
    search_entry.bind("<KeyRelease>", update_list)

    # Двойной клик по элементу списка для быстрого выбора
    listbox.bind("<Double-Button-1>", lambda event: select_font())

    # Кнопка выбора шрифта
    select_button = tk.Button(
        search_window,
        text="Выбрать шрифт",
        command=select_font
    )
    select_button.pack(pady=5)

    # Заполняем список изначально всеми шрифтами
    update_list()


def create_main_window():
    main_window = tk.Tk()
    main_window.title("FontPro")
    main_window.geometry("500x400")
    icon = PhotoImage(file="logo.png")
    main_window.iconphoto(False, icon)

    # Заголовок
    tk.Label(main_window, text="Добро пожаловать в FontPro", font=("Minecraft Rus", 14, "bold")).pack(pady=10)

    def limit_input(action, value_if_allowed):
        # action == '1' означает вставку (insert), '0' — удаление (delete)
        if action == '1':
            # Разрешаем ввод, только если длина после вставки <= 50
            return len(value_if_allowed) <= 50
        # При удалении всегда разрешаем
        return True

    # Создаём функцию валидации
    vcmd = (main_window.register(limit_input), '%d', '%P')

    # Поле для ввода текста
    tk.Label(main_window, text="Введите текст:").pack(pady=5)
    text_entry = tk.Entry(
        main_window,
        width=50,
        validate='key',
        validatecommand=vcmd
    )
    text_entry.pack(pady=10)

    # Полный список шрифтов
    font_list = ["System", "Terminal", "Fixedsys", "Modern", "Roman", "Script", "Courier", "MS Serif", "MS Sans Serif",
                 "Small Fonts", "Adobe Devanagari", "David CLM", "Nachlieli CLM", "Frank Ruhl Hofshi", "Miriam Libre",
                 "GOST type A (plotter)", "GOST type B (plotter)", "Symbol type A (plotter)", "Symbol type B (plotter)",
                 "Marlett", "Arial", "Arabic Transparent", "Arial Baltic", "Arial CE", "Arial CYR", "Arial Greek",
                 "Arial TUR", "Arial Cyr", "Arial Black", "Bahnschrift Light", "Bahnschrift SemiLight", "Bahnschrift",
                 "Bahnschrift SemiBold", "Bahnschrift Light SemiCondensed", "Bahnschrift SemiLight SemiConde",
                 "Bahnschrift SemiCondensed", "Bahnschrift SemiBold SemiConden", "Bahnschrift Light Condensed",
                 "Bahnschrift SemiLight Condensed", "Bahnschrift Condensed", "Bahnschrift SemiBold Condensed",
                 "Calibri", "Calibri Light", "Cambria", "Cambria Math", "Candara", "Candara Light", "Comic Sans MS",
                 "Consolas", "Constantia", "Corbel", "Corbel Light", "Courier New", "Courier New Baltic",
                 "Courier New CE", "Courier New CYR", "Courier New Greek", "Courier New TUR", "Courier",
                 "Courier New Cyr", "Ebrima", "Franklin Gothic Medium", "Gabriola", "Gadugi", "Georgia", "Impact",
                 "Ink Free", "Javanese Text", "Leelawadee UI", "Leelawadee UI Semilight", "Lucida Console",
                 "Lucida Sans Unicode", "Malgun Gothic", "@Malgun Gothic", "Malgun Gothic Semilight",
                 "@Malgun Gothic Semilight", "Microsoft Himalaya", "Microsoft JhengHei", "@Microsoft JhengHei",
                 "Microsoft JhengHei UI", "@Microsoft JhengHei UI", "Microsoft JhengHei Light",
                 "@Microsoft JhengHei Light", "Microsoft JhengHei UI Light", "@Microsoft JhengHei UI Light",
                 "Microsoft New Tai Lue", "Microsoft PhagsPa", "Microsoft Sans Serif", "Microsoft Tai Le",
                 "Microsoft YaHei", "@Microsoft YaHei", "Microsoft YaHei UI", "@Microsoft YaHei UI",
                 "Microsoft YaHei Light", "@Microsoft YaHei Light", "Microsoft YaHei UI Light",
                 "@Microsoft YaHei UI Light", "Microsoft Yi Baiti", "MingLiU-ExtB", "@MingLiU-ExtB", "PMingLiU-ExtB",
                 "@PMingLiU-ExtB", "MingLiU_HKSCS-ExtB", "@MingLiU_HKSCS-ExtB", "Mongolian Baiti", "MS Gothic",
                 "@MS Gothic", "MS UI Gothic", "@MS UI Gothic", "MS PGothic", "@MS PGothic", "MV Boli", "Myanmar Text",
                 "Nirmala UI", "Nirmala UI Semilight", "Palatino Linotype", "Segoe MDL2 Assets", "Segoe Print",
                 "Segoe Script", "Segoe UI", "Segoe UI Black", "Segoe UI Emoji", "Segoe UI Historic", "Segoe UI Light",
                 "Segoe UI Semibold", "Segoe UI Semilight", "Segoe UI Symbol", "SimSun", "@SimSun", "NSimSun",
                 "@NSimSun", "SimSun-ExtB", "@SimSun-ExtB", "Sitka Small", "Sitka Text", "Sitka Subheading",
                 "Sitka Heading", "Sitka Display", "Sitka Banner", "Sylfaen", "Symbol", "Tahoma", "Times New Roman",
                 "Times New Roman Baltic", "Times New Roman CE", "Times New Roman CYR", "Times New Roman",
                 "Times New Roman TUR", "Times New Roman Cyr", "Trebuchet MS", "Ubuntu", "Verdana",
                 "Webdings", "Wingdings", "Wingdings 2", "Wingdings 3", "Yu Gothic", "@Yu Gothic", "Yu Gothic UI",
                 "@Yu Gothic UI", "Yu Gothic UI Semibold", "@Yu Gothic UI Semibold", "Yu Gothic Light",
                 "@Yu Gothic Light", "Yu Gothic UI Light", "@Yu Gothic UI Light", "Yu Gothic Medium",
                 "Yu Gothic UI Semilight", "@Yu Gothic UI Semilight", "HoloLens MDL2 Assets", "Book Antiqua",
                 "Century", "Dubai", "Dubai Light", "Dubai Medium", "Century Gothic", "Leelawadee", "Microsoft Uighur",
                 "MT Extra", "Wingdings 2", "Wingdings 3", "Arial Narrow", "Bookman Old Style", "Bookshelf Symbol 7",
                 "Garamond", "Monotype Corsiva", "MS Reference Sans Serif", "MS Reference Specialty", "ZWAdobeF",
                 "DejaVu Math TeX Gyre", "Reem Kufi", "Liberation Sans Narrow", "OpenSymbol", "Noto Serif Georgian",
                 "Noto Sans Lao", "Noto Serif Armenian", "Noto Sans Georgian Bold", "Noto Sans Arabic",
                 "Linux Biolinum G", "Noto Naskh Arabic", "Noto Sans", "Scheherazade", "Liberation Mono",
                 "Noto Serif Lao", "Noto Sans Armenian", "David Libre", "Noto Sans Lisu", "Noto Kufi Arabic", "Amiri",
                 "Caladea", "Noto Sans Hebrew", "Carlito", "Noto Serif Hebrew", "Alef", "Gentium Basic", "Noto Serif",
                 "Amiri Quran", "Frank Ruehl CLM", "Miriam CLM", "Miriam Mono CLM", "DejaVu Sans", "DejaVu Sans Light",
                 "DejaVu Sans Condensed", "DejaVu Sans Mono", "DejaVu Serif", "DejaVu Serif Condensed",
                 "Gentium Book Basic", "Liberation Sans", "Liberation Serif", "Linux Libertine Display G",
                 "Linux Libertine G", "Rubik", "Noto Sans Georgian", "SimSun-ExtG", "@SimSun-ExtG", "Minecraft Rus",
                 "@Minecraft Rus", "Fraunces 9pt Thin", "Fraunces 9pt Light", "Fraunces 9pt", "Fraunces 9pt SemiBold",
                 "Fraunces 9pt Black", "Fraunces 9pt SuperSoft Thin", "Nobile", "Nobile Medium", "Fraunces 144pt Thin",
                 "Fraunces 144pt SemiBold", "Inter Thin", "Inter ExtraLight", "Inter Light", "Inter", "Inter Medium",
                 "Inter SemiBold", "Inter ExtraBold", "Inter Black", "Petrona Thin", "Petrona ExtraLight",
                 "Petrona Light", "Petrona", "Petrona Medium", "Petrona SemiBold", "Petrona ExtraBold", "Petrona Black",
                 "Syne", "Syne Medium", "Syne SemiBold", "Syne ExtraBold", "GOST Type AU", "GOST type A", "GOST type B",
                 "GOST Type BU", "Symbol type A", "Symbol type B", "Go Noto Kurrent-Regular",
                 "@Go Noto Kurrent-Regular", "Go Noto Kurrent-Bold", "@Go Noto Kurrent-Bold", "Roboto Mono Thin",
                 "Roboto Mono Light", "Roboto Mono", "Roboto Mono Medium", "GLYPHICONS Halflings", "Muli SemiBold",
                 "Font Awesome 5 Free Solid", "slick", "Font Awesome 5 Free Regular", "Font Awesome 5 Brands Regular",
                 "Roboto", "Acquest Script", "JetBrains Mono", "JetBrains Mono Thin", "Ubuntu", "Patrick Hand",
                 "Manrope ExtraLight", "Manrope Light", "Manrope", "Manrope Medium", "Manrope SemiBold",
                 "Manrope ExtraBold", "@Yu Gothic Medium", "Roman Greek"]

    font_var = tk.StringVar()
    font_dropdown = ttk.Combobox(main_window, textvariable=font_var, values=font_list, state="readonly", width=30)
    font_dropdown.set("Выберите шрифт")
    font_dropdown.pack(pady=10)

    # Ярлык для предпросмотра (будет менять шрифт)
    preview_label = tk.Label(main_window, text="", wraplength=400, justify="left")
    preview_label.pack(pady=20)

    # Кнопка открытия окна поиска шрифтов
    search_button = tk.Button(
        main_window,
        text="Открыть окно поиска шрифтов",
        command=lambda: create_search_window(main_window, font_var, preview_label, font_list)
    )
    search_button.pack(pady=5)

    # Кнопка "Предпросмотр"
    def preview_text():
        text = text_entry.get()
        font = font_var.get()
        if text and font != "Выберите шрифт":
            # Устанавливаем текст и шрифт для preview_label
            preview_label.config(
                text=text,
                font=(font, 12)  # 12 — размер шрифта (можно изменить)
            )
        else:
            messagebox.showwarning("Предупреждение", "Введите текст и выберите шрифт!")
            preview_label.config(text="")  # Очищаем ярлык

    tk.Button(main_window, text="Предпросмотр", command=preview_text).pack(pady=5)

    # Кнопка "Копировать название шрифта"
    def copy_font_name():
        font = font_var.get()
        if font != "Выберите шрифт":
            main_window.clipboard_clear()
            main_window.clipboard_append(font)
            messagebox.showinfo("Успех", f"Название шрифта '{font}' скопировано в буфер обмена!")
        else:
            messagebox.showwarning("Предупреждение", "Выберите шрифт!")

    tk.Button(main_window, text="Копировать название шрифта", command=copy_font_name).pack(pady=5)

    # Кнопка "Копировать текст с этим шрифтом"
    def copy_text_with_font():
        text = text_entry.get()
        font = font_var.get()
        if text and font != "Выберите шрифт":
            copied_text = f"[{font}] {text}"
            main_window.clipboard_clear()
            main_window.clipboard_append(copied_text)
            messagebox.showinfo("Успех", "Текст с указанием шрифта скопирован в буфер обмена!")
        else:
            messagebox.showwarning("Предупреждение", "Введите текст и выберите шрифт!")

    tk.Button(main_window, text="Копировать текст с этим шрифтом", command=copy_text_with_font).pack(pady=5)

    main_window.mainloop()


if __name__ == "__main__":
    # Инициализируем Firebase при запуске
    from firebase_config import initialize_firebase

    initialize_firebase()
    # Запускаем окно регистрации при старте программы
    okno_vybora()
