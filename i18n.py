# i18n.py
class I18n:
    _instance = None
    _translations = {}
    _current_lang = "ru"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_translations()
        return cls._instance

    def _load_translations(self):
        self._translations = {
            "ru": {
                # Основное окно
                "app_title": "Быки и коровы",
                "new_game": "Новая игра",
                "settings": "Настройки",
                "exit": "Выход",
                "statistics": "Статистика",
                "show_stats": "Показать статистику",
                "reset_stats": "Сбросить статистику",
                "help": "Справка",
                "rules": "Правила",
                "about": "О программе",
                "your_number": "Ваше число:",
                "check": "✓ Проверить",
                "hint": "? Подсказка",
                "auto": "⚡ Авто",
                "move": "№",
                "guess": "Число",
                "bulls": "Быки",
                "cows": "Коровы",
                "status_new_game": "Новая игра. Введите число.",
                "status_move": "Ход {move}: Быки: {bulls}, Коровы: {cows}",
                "status_win": "Победа! Число {secret}",
                "status_auto_solve": "Авторешение. Число: {secret}",
                "game_over": "Игра окончена",
                "game_over_msg": "Игра уже завершена. Начните новую игру.",
                "win_title": "Победа!",
                "win_message": "Поздравляем! Вы угадали число {secret} за {moves} ходов.",
                "input_error_digits": "Введите только цифры!",
                "input_error_length": "Число должно быть {length}-значным!",
                "input_error_repeats": "Цифры не должны повторяться!",
                "hint_dialog": "Подсказка",
                "hint_text": "Подсказка: цифра {digit} на позиции {pos}.",
                "hint_all_guessed": "Все позиции уже угаданы!",
                "auto_solve_title": "Авторешение",
                "auto_solve_text": "Загаданное число: {secret}",
                # Диалог настроек
                "settings_title": "Настройки",
                "number_length": "Длина числа:",
                "allow_repeats": "Разрешить повтор цифр",
                "theme": "Тема:",
                "language": "Язык:",
                "ok": "OK",
                "cancel": "Отмена",
                # Статистика
                "stats_title": "Статистика",
                "stats_text": "Сыграно игр: {played}\nПобед: {won}\nСреднее число ходов: {avg}\nЛучший результат: {best}\nПодсказок использовано: {hints}\nАвторешений: {auto}",
                "reset_confirm_title": "Сброс статистики",
                "reset_confirm_msg": "Вы уверены, что хотите обнулить статистику?",
                "stats_reset": "Статистика сброшена.",
                # Правила
                "rules_title": "Правила",
                "rules_text": "Правила игры «Быки и коровы»:\n\nКомпьютер загадывает число из заданного количества цифр (по умолчанию 4).\nЦифры могут повторяться или нет — зависит от настроек.\n\nВы вводите своё число. В ответ программа сообщает:\n• Быки — цифры, стоящие на своих местах.\n• Коровы — цифры, присутствующие в числе, но не на своих местах.\n\nЦель — отгадать число за минимальное количество ходов.",
                # О программе
                "about_title": "О программе",
                "about_text": "Игра «Быки и коровы»\nВерсия 1.0\n\nРазработано в рамках Выпускной Квалификационной Работы Васильевым Глебом, студент ИСПт-22-(9)-2.\nИспользуется Python + Tkinter."
            },
            "en": {
                "app_title": "Bulls and Cows",
                "new_game": "New Game",
                "settings": "Settings",
                "exit": "Exit",
                "statistics": "Statistics",
                "show_stats": "Show Statistics",
                "reset_stats": "Reset Statistics",
                "help": "Help",
                "rules": "Rules",
                "about": "About",
                "your_number": "Your number:",
                "check": "✓ Check",
                "hint": "? Hint",
                "auto": "⚡ Auto",
                "move": "#",
                "guess": "Number",
                "bulls": "Bulls",
                "cows": "Cows",
                "status_new_game": "New game. Enter a number.",
                "status_move": "Move {move}: Bulls: {bulls}, Cows: {cows}",
                "status_win": "Victory! Number {secret}",
                "status_auto_solve": "Auto-solve. Number: {secret}",
                "game_over": "Game Over",
                "game_over_msg": "Game is already over. Start a new game.",
                "win_title": "Victory!",
                "win_message": "Congratulations! You guessed the number {secret} in {moves} moves.",
                "input_error_digits": "Enter digits only!",
                "input_error_length": "Number must be {length} digits!",
                "input_error_repeats": "Digits must not repeat!",
                "hint_dialog": "Hint",
                "hint_text": "Hint: digit {digit} at position {pos}.",
                "hint_all_guessed": "All positions already guessed!",
                "auto_solve_title": "Auto-solve",
                "auto_solve_text": "Secret number: {secret}",
                "settings_title": "Settings",
                "number_length": "Number length:",
                "allow_repeats": "Allow repeated digits",
                "theme": "Theme:",
                "language": "Language:",
                "ok": "OK",
                "cancel": "Cancel",
                "stats_title": "Statistics",
                "stats_text": "Games played: {played}\nWon: {won}\nAverage moves: {avg}\nBest score: {best}\nHints used: {hints}\nAuto-solves: {auto}",
                "reset_confirm_title": "Reset Statistics",
                "reset_confirm_msg": "Are you sure you want to reset statistics?",
                "stats_reset": "Statistics reset.",
                "rules_title": "Rules",
                "rules_text": "Rules of Bulls and Cows:\n\nThe computer generates a number with a given length (default 4).\nDigits may repeat or not, depending on settings.\n\nYou enter your guess. The program replies:\n• Bulls — digits in the correct position.\n• Cows — digits present but in the wrong position.\n\nThe goal is to guess the number in as few moves as possible.",
                "about_title": "About",
                "about_text": "Bulls and Cows game\nVersion 1.0\n\nDeveloped as part of the final qualification work by Gleb Vasilyev, student of group ISPt-22-(9)-2.\nUses Python + Tkinter."
            }
        }

    def set_language(self, lang):
        if lang in self._translations:
            self._current_lang = lang

    def get(self, key, **kwargs):
        text = self._translations[self._current_lang].get(key, key)
        if kwargs:
            return text.format(**kwargs)
        return text

# Глобальная функция для удобного доступа
_ = I18n().get