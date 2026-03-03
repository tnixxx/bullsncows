import random

class GameLogic:
    """Содержит логику игры 'Быки и коровы'."""
    
    def __init__(self, length=4, allow_repeats=False):
        self.length = length
        self.allow_repeats = allow_repeats
        self.secret = ""
        self.history = []  # список кортежей (guess, bulls, cows)
        self.game_over = False
        self.generate_secret()
    
    def generate_secret(self):
        """Генерирует загаданное число в соответствии с настройками."""
        digits = list("0123456789")
        if not self.allow_repeats:
            # Выбираем уникальные цифры
            self.secret = ''.join(random.sample(digits, self.length))
        else:
            # Генерируем с повторениями (первая цифра не может быть 0, чтобы число было length-значным)
            first = random.choice("123456789")
            rest = ''.join(random.choice("0123456789") for _ in range(self.length - 1))
            self.secret = first + rest
        self.game_over = False
        self.history.clear()
    
    def check_guess(self, guess):
        """
        Проверяет введённое число (строку) и возвращает (bulls, cows).
        Если число некорректно, выбрасывает ValueError с описанием.
        """
        if not guess.isdigit():
            raise ValueError("Введите только цифры!")
        if len(guess) != self.length:
            raise ValueError(f"Число должно быть {self.length}-значным!")
        
        # Проверка на уникальность (если запрещены повторы)
        if not self.allow_repeats and len(set(guess)) != self.length:
            raise ValueError("Цифры не должны повторяться!")
        
        # Вычисляем быков и коров
        bulls = 0
        cows = 0
        for i, ch in enumerate(guess):
            if ch == self.secret[i]:
                bulls += 1
            elif ch in self.secret:
                cows += 1
        
        self.history.append((guess, bulls, cows))
        
        if bulls == self.length:
            self.game_over = True
        
        return bulls, cows
    
    def hint(self):
        """
        Возвращает подсказку: случайную позицию, которая ещё не была угадана.
        Подсказка считается использованной (увеличиваем счётчик в stats отдельно).
        Возвращает строку с сообщением или None, если игра завершена.
        """
        if self.game_over:
            return None
        
        # Соберём все позиции, которые уже точно угаданы (есть в истории быки)
        guessed_positions = set()
        for guess, bulls, _ in self.history:
            for i, (g, s) in enumerate(zip(guess, self.secret)):
                if g == s:
                    guessed_positions.add(i)
        
        # Выбираем случайную позицию из ещё не угаданных
        available = [i for i in range(self.length) if i not in guessed_positions]
        if not available:
            return "Все позиции уже угаданы!"  # но тогда игра должна быть завершена
        
        pos = random.choice(available)
        digit = self.secret[pos]
        return f"Подсказка: цифра {digit} на позиции {pos+1}."
    
    def auto_solve(self):
        """
        Возвращает загаданное число и завершает игру (победа).
        """
        self.game_over = True
        return self.secret
    
    def get_history(self):
        """Возвращает историю ходов в виде списка кортежей."""
        return self.history