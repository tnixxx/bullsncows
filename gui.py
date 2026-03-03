import sv_ttk
import tkinter as tk
from tkinter import ttk, messagebox

from game_logic import GameLogic
from settings import Settings
from stats import Stats
from i18n import _, I18n

class SettingsDialog(tk.Toplevel):
    """Диалог настроек игры."""
    
    def __init__(self, parent, settings):
        super().__init__(parent)
        self.parent = parent
        self.settings = settings
        self.title(_("settings_title"))
        self.geometry("350x300")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        sv_ttk.set_theme(self.settings.get("theme"))
        self.create_widgets()
    
    def create_widgets(self):
        frame = ttk.Frame(self, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        # Длина числа
        ttk.Label(frame, text=_("number_length")).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.length_var = tk.IntVar(value=self.settings.get("number_length"))
        length_spin = ttk.Spinbox(frame, from_=3, to=6, textvariable=self.length_var, width=5)
        length_spin.grid(row=0, column=1, sticky=tk.W, padx=5)

        # Разрешить повторы
        self.repeats_var = tk.BooleanVar(value=self.settings.get("allow_repeats"))
        ttk.Checkbutton(frame, text=_("allow_repeats"), variable=self.repeats_var).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)

        # Тема
        ttk.Label(frame, text=_("theme")).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.theme_var = tk.StringVar(value=self.settings.get("theme"))
        theme_combo = ttk.Combobox(frame, textvariable=self.theme_var, values=["light", "dark"], state="readonly", width=10)
        theme_combo.grid(row=2, column=1, sticky=tk.W, padx=5)

        # Язык
        ttk.Label(frame, text=_("language")).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.lang_var = tk.StringVar(value=self.settings.get("language"))
        lang_combo = ttk.Combobox(frame, textvariable=self.lang_var, values=["ru", "en"], state="readonly", width=10)
        lang_combo.grid(row=3, column=1, sticky=tk.W, padx=5)

        # Кнопки
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text=_("ok"), command=self.ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=_("cancel"), command=self.destroy).pack(side=tk.LEFT)

    def ok(self):
        self.settings.set("number_length", self.length_var.get())
        self.settings.set("allow_repeats", self.repeats_var.get())
        new_theme = self.theme_var.get()
        self.settings.set("theme", new_theme)
        new_lang = self.lang_var.get()
        if new_lang != self.settings.get("language"):
            self.settings.set("language", new_lang)
            I18n().set_language(new_lang)
            self.parent.update_texts()  
        sv_ttk.set_theme(new_theme)
        self.parent.update_treeview_colors(new_theme)
        self.destroy()

class GameWindow(tk.Tk):
    """Главное окно игры."""
    
    def __init__(self):
        super().__init__()
        self.title(_("app_title"))   
        self.settings = Settings()
        I18n().set_language(self.settings.get("language"))
        self.stats = Stats()
        # Устанавливаем размер и положение окна из настроек
        self.geometry(f"{self.settings.get('window_width')}x{self.settings.get('window_height')}+{self.settings.get('window_x')}+{self.settings.get('window_y')}")
        self.minsize(600, 400)

        sv_ttk.set_theme(self.settings.get("theme"))   # единственный вызов

        # Инициализация игровой логики
        self.game = GameLogic(
            length=self.settings.get('number_length'),
            allow_repeats=self.settings.get('allow_repeats')
        )

        self.create_menu()
        self.create_widgets()
        self.update_treeview_colors(self.settings.get("theme"))  # сразу настраиваем цвета

        # Привязываем событие закрытия окна для сохранения геометрии
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_menu(self):
        menubar = tk.Menu(self)
        
        # Меню "Игра"
        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label="Новая игра", command=self.new_game, accelerator="F2")
        game_menu.add_command(label="Настройки", command=self.open_settings)
        game_menu.add_separator()
        game_menu.add_command(label="Выход", command=self.on_closing)
        menubar.add_cascade(label="Игра", menu=game_menu)
        
        # Меню "Статистика"
        stats_menu = tk.Menu(menubar, tearoff=0)
        stats_menu.add_command(label="Показать статистику", command=self.show_stats)
        stats_menu.add_command(label="Сбросить статистику", command=self.reset_stats)
        menubar.add_cascade(label="Статистика", menu=stats_menu)
        
        # Меню "Справка"
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Правила", command=self.show_rules)
        help_menu.add_command(label="О программе", command=self.show_about)
        menubar.add_cascade(label="Справка", menu=help_menu)
        
        self.config(menu=menubar)
        
        # Горячие клавиши
        self.bind("<F2>", lambda e: self.new_game())
        self.bind("<Return>", lambda e: self.check_guess())
    
    def create_widgets(self):
        # Основной фрейм
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Верхняя панель с полем ввода и кнопками
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=5)

        # Прогресс-бар
        self.progress = ttk.Progressbar(main_frame, orient="horizontal", length=200, mode="determinate")
        self.progress.pack(pady=5)
        
        self.label_your_number = ttk.Label(input_frame, text=_("your_number"))
        self.label_your_number.pack(side=tk.LEFT, padx=5)
        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(input_frame, textvariable=self.entry_var, width=10, font=("Courier", 14))
        self.entry.pack(side=tk.LEFT, padx=5)
        self.entry.focus()
        
        self.check_btn = ttk.Button(input_frame, text=_("check"), command=self.check_guess)
        self.check_btn.pack(side=tk.LEFT, padx=5)
        
        self.hint_btn = ttk.Button(input_frame, text=_("hint"), command=self.hint)
        self.hint_btn.pack(side=tk.LEFT, padx=5)
        
        self.auto_btn = ttk.Button(input_frame, text=_("auto"), command=self.auto_solve)
        self.auto_btn.pack(side=tk.LEFT, padx=5)
        
        # Таблица истории ходов
        columns = ("move", "guess", "bulls", "cows")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=15)
        self.tree.heading("move", text=_("move"))
        self.tree.heading("guess", text=_("guess"))
        self.tree.heading("bulls", text=_("bulls"))
        self.tree.heading("cows", text=_("cows"))
                
        # Устанавливаем ширину колонок
        self.tree.column("move", width=50, anchor=tk.CENTER)
        self.tree.column("guess", width=100, anchor=tk.CENTER)
        self.tree.column("bulls", width=70, anchor=tk.CENTER)
        self.tree.column("cows", width=70, anchor=tk.CENTER)

        # Настройка стилей для Treeview
        style = ttk.Style()
        style.configure("Treeview", background="#ffffff", foreground="#000000", 
                        fieldbackground="#ffffff", rowheight=25)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), 
                        background="#dddddd", foreground="#000000")
        style.map("Treeview", background=[("selected", "#347083")])  # цвет выделенной строки
        style.configure("Error.TEntry", fieldbackground="#ffcccc", foreground="#000000")


        # Теги для чередования строк
        self.tree.tag_configure('oddrow', background='#f2f2f2')
        self.tree.tag_configure('evenrow', background='#ffffff')
        
        # Добавляем скроллбар
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Строка состояния
        self.status_var = tk.StringVar()
        self.status_var.set(_("status_new_game"))
        status_bar = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def new_game(self):
        """Начинает новую игру."""
        self.game = GameLogic(
            length=self.settings.get('number_length'),
            allow_repeats=self.settings.get('allow_repeats')
        )
        # Очищаем таблицу
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.entry_var.set("")
        self.status_var.set(_("status_new_game"))
        self.entry.focus()
        self.stats.add_game_played()  # Увеличиваем счётчик игр
    
    def check_guess(self):
        """Обрабатывает нажатие кнопки Проверить."""
        if self.game.game_over:
            messagebox.showinfo(_("game_over"), _("game_over_msg"))
            return

        guess = self.entry_var.get().strip()
        try:
            bulls, cows = self.game.check_guess(guess)
        except ValueError as e:
            messagebox.showerror(_("input_error_digits"))
            return

        # Добавляем запись в таблицу с чередованием фона
        move_num = len(self.game.history)
        tag = 'evenrow' if move_num % 2 == 0 else 'oddrow'
        self.tree.insert("", tk.END, values=(move_num, guess, bulls, cows), tags=(tag,))
        self.tree.see(self.tree.get_children()[-1])

        self.entry_var.set("")
        self.status_var.set(f"Ход {move_num}: Быки: {bulls}, Коровы: {cows}")

        # Обновляем прогресс-бар
        progress_value = (bulls / self.game.length) * 100
        self.progress["value"] = progress_value

        if self.game.game_over:
            self.stats.add_game_won(move_num)
            self.show_win_dialog(move_num, self.game.secret)
            self.status_var.set(f"Победа! Число {self.game.secret}")
    
    def hint(self):
        """Выдаёт подсказку."""
        if self.game.game_over:
            messagebox.showinfo("Игра окончена", "Игра завершена. Начните новую игру.")
            return
        hint_text = self.game.hint()
        if hint_text:
            self.stats.add_hint()
            messagebox.showinfo(_("hint_dialog"), hint_text)
        else:
            messagebox.showinfo(_("hint_dialog"), _("hint_all_guessed"))
    
    def auto_solve(self):
        """Автоматическое решение."""
        if self.game.game_over:
            messagebox.showinfo("Игра окончена", "Игра уже завершена.")
            return
        answer = self.game.auto_solve()
        self.stats.add_auto_solve()
        # Показываем ответ
        messagebox.showinfo(_("auto_solve_title"), _("auto_solve_text", secret=answer))
        # Завершаем игру, как победу (но не считаем в статистику побед, а только авторешение)
        self.game.game_over = True
        self.status_var.set(_("status_auto_solve", secret=answer))
    
    def open_settings(self):
        """Открывает диалог настроек."""
        SettingsDialog(self, self.settings)
    
    def show_stats(self):
        data = self.stats.get_data()
        avg = f"{data['average_moves']:.2f}" if data['games_won'] > 0 else "-"
        best = str(data['best_score']) if data['best_score'] else "-"
        text = _("stats_text",
                played=data['games_played'],
                won=data['games_won'],
                avg=avg,
                best=best,
                hints=data['hints_used'],
                auto=data['auto_solves'])
        messagebox.showinfo(_("stats_title"), text)

    def reset_stats(self):
        """Сбрасывает статистику с подтверждением."""
        if messagebox.askyesno(_("reset_confirm_title"), _("reset_confirm_msg")):
            self.stats.reset()
            messagebox.showinfo(_("stats_title"), _("stats_reset"))
    
    def show_rules(self):
        messagebox.showinfo(_("rules_title"), _("rules_text"))
    
    def show_about(self):
        messagebox.showinfo(_("about_title"), _("about_text"))
    
    def on_closing(self):
        """Сохраняет геометрию окна и завершает работу."""
        # Получаем текущие размеры и положение
        geom = self.geometry().split("+")
        width_height = geom[0].split("x")
        if len(width_height) == 2:
            width, height = width_height
            x, y = geom[1], geom[2]
            self.settings.set("window_width", int(width))
            self.settings.set("window_height", int(height))
            self.settings.set("window_x", int(x))
            self.settings.set("window_y", int(y))
        self.destroy()

    def flash_entry(self):
        """Мигает красным фоном поля ввода."""
        self.entry.configure(background="#ffcccc")
        self.after(500, lambda: self.entry.configure(background=""))

    def show_win_dialog(self, moves, secret):
        win = tk.Toplevel(self)
        win.title(_("win_title"))
        win.geometry("300x150")
        win.resizable(False, False)
        win.transient(self)
        win.grab_set()
        
        ttk.Label(win, text="🎉 " + _("win_title") + " 🎉", font=("Segoe UI", 14, "bold")).pack(pady=10)
        ttk.Label(win, text=_("win_message", secret=secret, moves=moves)).pack()
        ttk.Button(win, text=_("ok"), command=win.destroy).pack(pady=10)

    def update_treeview_colors(self, theme):
        """Обновляет цвета чередования строк в зависимости от темы."""
        if theme == "dark":
            self.tree.tag_configure('oddrow', background='#2d2d2d')
            self.tree.tag_configure('evenrow', background='#3c3c3c')
        else:
            self.tree.tag_configure('oddrow', background='#f2f2f2')
            self.tree.tag_configure('evenrow', background='#ffffff')

    def update_texts(self):
        """Обновляет все тексты при смене языка."""
        self.title(_("app_title"))
        self.label_your_number.config(text=_("your_number"))
        self.check_btn.config(text=_("check"))
        self.hint_btn.config(text=_("hint"))
        self.auto_btn.config(text=_("auto"))
        self.tree.heading("move", text=_("move"))
        self.tree.heading("guess", text=_("guess"))
        self.tree.heading("bulls", text=_("bulls"))
        self.tree.heading("cows", text=_("cows"))
        # Пересоздаём меню, чтобы обновить его пункты
        self.create_menu()
        # Обновляем статус, если игра не начата
        if not self.game.game_over and len(self.game.history) == 0:
            self.status_var.set(_("status_new_game"))
        elif self.game.game_over and len(self.game.history) > 0:
            # Если победа, текст уже должен быть, но можно обновить
            pass