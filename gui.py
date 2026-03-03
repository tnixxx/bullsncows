import sv_ttk
import tkinter as tk
from tkinter import ttk, messagebox

from game_logic import GameLogic
from settings import Settings
from stats import Stats

class SettingsDialog(tk.Toplevel):
    """Диалог настроек игры."""
    
    def __init__(self, parent, settings):
        super().__init__(parent)
        self.parent = parent
        self.settings = settings
        self.title("Настройки")
        self.geometry("300x250")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        self.create_widgets()
    
    def create_widgets(self):
        frame = ttk.Frame(self, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Длина числа
        ttk.Label(frame, text="Длина числа:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.length_var = tk.IntVar(value=self.settings.get("number_length"))
        length_spin = ttk.Spinbox(frame, from_=3, to=6, textvariable=self.length_var, width=5)
        length_spin.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        # Разрешить повторы
        self.repeats_var = tk.BooleanVar(value=self.settings.get("allow_repeats"))
        ttk.Checkbutton(frame, text="Разрешить повтор цифр", variable=self.repeats_var).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Тема
        ttk.Label(frame, text="Тема:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.theme_var = tk.StringVar(value=self.settings.get("theme"))
        theme_combo = ttk.Combobox(frame, textvariable=self.theme_var, values=["light", "dark"], state="readonly", width=10)
        theme_combo.grid(row=2, column=1, sticky=tk.W, padx=5)
        
        # Кнопки
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="OK", command=self.ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Отмена", command=self.destroy).pack(side=tk.LEFT)
    
    def ok(self):
        # Сохраняем настройки
        self.settings.set("number_length", self.length_var.get())
        self.settings.set("allow_repeats", self.repeats_var.get())
        self.settings.set("theme", self.theme_var.get())
        # Применяем тему (можно перезапустить игру или обновить стиль)
        self.settings.apply_theme(self.parent)
        self.destroy()


class GameWindow(tk.Tk):
    """Главное окно игры."""
    
    def __init__(self):
        super().__init__()
        self.title("Быки и коровы")
        sv_ttk.set_theme("dark")
        self.settings = Settings()
        self.stats = Stats()
        
        # Устанавливаем размер и положение окна из настроек
        self.geometry(f"{self.settings.get('window_width')}x{self.settings.get('window_height')}+{self.settings.get('window_x')}+{self.settings.get('window_y')}")
        self.minsize(600, 400)
        
        sv_ttk.set_theme(self.settings.get("theme"))
        
        # Инициализация игровой логики
        self.game = GameLogic(
            length=self.settings.get('number_length'),
            allow_repeats=self.settings.get('allow_repeats')
        )
        
        self.create_menu()
        self.create_widgets()
        # self.update_status()
        
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
        
        ttk.Label(input_frame, text="Ваше число:").pack(side=tk.LEFT, padx=5)
        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(input_frame, textvariable=self.entry_var, width=10, font=("Courier", 14))
        self.entry.pack(side=tk.LEFT, padx=5)
        self.entry.focus()
        
        self.check_btn = ttk.Button(input_frame, text="Проверить", command=self.check_guess)
        self.check_btn.pack(side=tk.LEFT, padx=5)
        
        self.hint_btn = ttk.Button(input_frame, text="Подсказка", command=self.hint)
        self.hint_btn.pack(side=tk.LEFT, padx=5)
        
        self.auto_btn = ttk.Button(input_frame, text="Авторешение", command=self.auto_solve)
        self.auto_btn.pack(side=tk.LEFT, padx=5)
        
        # Таблица истории ходов
        columns = ("move", "guess", "bulls", "cows")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=15)
        self.tree.heading("move", text="№")
        self.tree.heading("guess", text="Число")
        self.tree.heading("bulls", text="Быки")
        self.tree.heading("cows", text="Коровы")
        
        # Устанавливаем ширину колонок
        self.tree.column("move", width=50, anchor=tk.CENTER)
        self.tree.column("guess", width=100, anchor=tk.CENTER)
        self.tree.column("bulls", width=70, anchor=tk.CENTER)
        self.tree.column("cows", width=70, anchor=tk.CENTER)
        
        # Добавляем скроллбар
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Строка состояния
        self.status_var = tk.StringVar()
        self.status_var.set("Новая игра. Введите число.")
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
        self.status_var.set("Новая игра. Введите число.")
        self.entry.focus()
        self.stats.add_game_played()  # Увеличиваем счётчик игр
    
    def check_guess(self):
        """Обрабатывает нажатие кнопки Проверить."""
        if self.game.game_over:
            messagebox.showinfo("Игра окончена", "Игра уже завершена. Начните новую игру.")
            return
        
        guess = self.entry_var.get().strip()
        try:
            bulls, cows = self.game.check_guess(guess)
        except ValueError as e:
            messagebox.showerror("Ошибка ввода", str(e))
            return
        
        # Добавляем запись в таблицу
        move_num = len(self.game.history)
        self.tree.insert("", tk.END, values=(move_num, guess, bulls, cows))
        # Прокручиваем к последней записи
        self.tree.see(self.tree.get_children()[-1])
        
        self.entry_var.set("")
        self.status_var.set(f"Ход {move_num}: Быки: {bulls}, Коровы: {cows}")
        
        if self.game.game_over:
            self.stats.add_game_won(move_num)
            messagebox.showinfo("Победа!", f"Поздравляем! Вы угадали число {self.game.secret} за {move_num} ходов.")
            self.status_var.set(f"Победа! Число {self.game.secret}")
    
    def hint(self):
        """Выдаёт подсказку."""
        if self.game.game_over:
            messagebox.showinfo("Игра окончена", "Игра завершена. Начните новую игру.")
            return
        hint_text = self.game.hint()
        if hint_text:
            self.stats.add_hint()
            messagebox.showinfo("Подсказка", hint_text)
        else:
            messagebox.showinfo("Подсказка", "Игра завершена, подсказка не нужна.")
    
    def auto_solve(self):
        """Автоматическое решение."""
        if self.game.game_over:
            messagebox.showinfo("Игра окончена", "Игра уже завершена.")
            return
        answer = self.game.auto_solve()
        self.stats.add_auto_solve()
        # Показываем ответ
        messagebox.showinfo("Авторешение", f"Загаданное число: {answer}")
        # Завершаем игру, как победу (но не считаем в статистику побед, а только авторешение)
        self.game.game_over = True
        self.status_var.set(f"Авторешение. Число: {answer}")
    
    def open_settings(self):
        """Открывает диалог настроек."""
        SettingsDialog(self, self.settings)
    
    def show_stats(self):
        """Показывает статистику."""
        messagebox.showinfo("Статистика", self.stats.get_text())
    
    def reset_stats(self):
        """Сбрасывает статистику с подтверждением."""
        if messagebox.askyesno("Сброс статистики", "Вы уверены, что хотите обнулить статистику?"):
            self.stats.reset()
            messagebox.showinfo("Статистика", "Статистика сброшена.")
    
    def show_rules(self):
        rules = (
            "Правила игры «Быки и коровы»:\n\n"
            "Компьютер загадывает число из заданного количества цифр (по умолчанию 4).\n"
            "Цифры могут повторяться или нет — зависит от настроек.\n\n"
            "Вы вводите своё число. В ответ программа сообщает:\n"
            "• Быки — цифры, стоящие на своих местах.\n"
            "• Коровы — цифры, присутствующие в числе, но не на своих местах.\n\n"
            "Цель — отгадать число за минимальное количество ходов."
        )
        messagebox.showinfo("Правила", rules)
    
    def show_about(self):
        about = (
            "Игра «Быки и коровы»\n"
            "Версия 1.0\n\n"
            "Разработано в рамках Выпускной Квалификационной Работы Васильевым Глебом, студент ИСПт-22-(9)-2.\n"
            "Используется Python + Tkinter."
        )
        messagebox.showinfo("О программе", about)
    
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