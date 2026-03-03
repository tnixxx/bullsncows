import json
import os
from tkinter import messagebox

class Stats:
    """Класс для управления статистикой игр."""
    
    DEFAULT_STATS = {
        "games_played": 0,
        "games_won": 0,
        "total_moves": 0,
        "hints_used": 0,
        "auto_solves": 0,
        "best_score": None  # минимальное число ходов для победы
    }
    
    def __init__(self, filename="stats.json"):
        self.filename = filename
        self.data = self.DEFAULT_STATS.copy()
        self.load()
    
    def load(self):
        """Загружает статистику из JSON."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    for key in self.DEFAULT_STATS:
                        if key in loaded:
                            self.data[key] = loaded[key]
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить статистику: {e}")
    
    def save(self):
        """Сохраняет статистику."""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить статистику: {e}")
    
    def add_game_played(self):
        """Увеличивает счётчик сыгранных игр."""
        self.data["games_played"] += 1
        self.save()
    
    def add_game_won(self, moves):
        """Фиксирует победу: обновляет количество побед, общее число ходов и лучший результат."""
        self.data["games_won"] += 1
        self.data["total_moves"] += moves
        if self.data["best_score"] is None or moves < self.data["best_score"]:
            self.data["best_score"] = moves
        self.save()
    
    def add_hint(self):
        """Увеличивает счётчик использованных подсказок."""
        self.data["hints_used"] += 1
        self.save()
    
    def add_auto_solve(self):
        """Увеличивает счётчик авторешений."""
        self.data["auto_solves"] += 1
        self.save()
    
    def reset(self):
        """Сбрасывает статистику на значения по умолчанию."""
        self.data = self.DEFAULT_STATS.copy()
        self.save()
    
    def get_text(self):
        """Возвращает строку с отформатированной статистикой для отображения."""
        text = f"Сыграно игр: {self.data['games_played']}\n"
        text += f"Побед: {self.data['games_won']}\n"
        if self.data['games_won'] > 0:
            avg = self.data['total_moves'] / self.data['games_won']
            text += f"Среднее число ходов: {avg:.2f}\n"
        else:
            text += "Среднее число ходов: —\n"
        text += f"Лучший результат: {self.data['best_score'] if self.data['best_score'] else '—'}\n"
        text += f"Подсказок использовано: {self.data['hints_used']}\n"
        text += f"Авторешений: {self.data['auto_solves']}"
        return text
    
    def get_data(self):
        return {
            "games_played": self.data["games_played"],
            "games_won": self.data["games_won"],
            "total_moves": self.data["total_moves"],
            "average_moves": self.data["total_moves"] / self.data["games_won"] if self.data["games_won"] > 0 else 0,
            "best_score": self.data["best_score"],
            "hints_used": self.data["hints_used"],
            "auto_solves": self.data["auto_solves"]
        }