import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
import tkinter.font as tkfont


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
    tk.Label(main_window, text="Добро пожаловать в FontPro", font=("Georgia", 14, "bold")).pack(pady=10)

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
    font_list = list(tkfont.families())
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
    create_main_window()
