import json
import os
from tkinter import messagebox, ttk

class Settings:
    """Класс для управления настройками приложения."""
    
    DEFAULT_SETTINGS = {
        "number_length": 4,
        "allow_repeats": False,
        "window_width": 800,
        "window_height": 600,
        "window_x": 100,
        "window_y": 100,
        "theme": "light"  # "light" or "dark"
    }
    
    def __init__(self, filename="settings.json"):
        self.filename = filename
        self.data = self.DEFAULT_SETTINGS.copy()
        self.load()
    
    def load(self):
        """Загружает настройки из JSON-файла, если он существует."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    # Обновляем только те ключи, которые есть в DEFAULT_SETTINGS
                    for key in self.DEFAULT_SETTINGS:
                        if key in loaded:
                            self.data[key] = loaded[key]
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить настройки: {e}")
    
    def save(self):
        """Сохраняет текущие настройки в JSON-файл."""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить настройки: {e}")
    
    def get(self, key):
        """Возвращает значение настройки по ключу."""
        return self.data.get(key, self.DEFAULT_SETTINGS[key])
    
    def set(self, key, value):
        """Устанавливает значение настройки и сразу сохраняет."""
        if key in self.data:
            self.data[key] = value
            self.save()
        else:
            raise KeyError(f"Неизвестный ключ настройки: {key}")
    
    def apply_theme(self, root_widget):
        """
        Применяет текущую тему к корневому окну и всем виджетам.
        Для полноценной смены темы используем ttk.Style.
        """
        style = ttk.Style()
        if self.data["theme"] == "dark":
            style.theme_use("clam")
            # Настраиваем цвета для тёмной темы
            style.configure(".", background="#2b2b2b", foreground="white", 
                            fieldbackground="#3c3c3c", troughcolor="#2b2b2b")
            style.configure("TLabel", background="#2b2b2b", foreground="white")
            style.configure("TButton", background="#404040", foreground="white", borderwidth=1)
            style.map("TButton", background=[("active", "#5a5a5a")])
            style.configure("TEntry", fieldbackground="#3c3c3c", foreground="white")
            style.configure("Treeview", background="#3c3c3c", foreground="white", 
                            fieldbackground="#3c3c3c")
            style.configure("Treeview.Heading", background="#404040", foreground="white")
            # Корневое окно тоже затемняем
            root_widget.configure(bg="#2b2b2b")
        else:
            style.theme_use("default")  # Возврат к стандартной теме (vista/alt/clam в зависимости от ОС)
            # Сброс фона корневого окна
            root_widget.configure(bg="SystemButtonFace")