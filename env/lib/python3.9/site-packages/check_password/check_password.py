import re
import time
import random
import datetime

from itertools import dropwhile
from difflib import SequenceMatcher


def return_answer(recommendation, res_type: str = "bool"):
    result = [i for i in recommendation if i != ""]

    res_type = type(eval(res_type + "()"))

    if res_type == bool:
        return not result
    elif res_type == str:
        return "\n".join(result) if result else "OK"
    elif res_type == list:
        return result
    else:
        raise ArgumentException("Argument \"result_type\" id not valid."
                                " It must be one of \"bool\", \"str\", \"list\"")


class ArgumentException(Exception):
    pass


class PasswordLengthException(Exception):
    pass


class Check:
    def __init__(self, lang="ru"):
        self.language = lang
        self.fraze = {
            "ru": {
                # dock
                "--dock--": "Ссылка на документацию: https://github.com/pavelglazunov/Check-Password",
                # password
                "--lower": "В пароле должны быть символы нижнего регистра",
                "--upper": "В пароле должны быть символы верхнего регистра",
                "--number": "В пароле должны быть цифры",
                "--symbols": "В пароле должны быть специальные символы",
                "--lower-count": "Количество букв в нижнем регистре не совпадает",
                "--upper-count": "Количество букв в верхнем регистре не совпадает",
                "--number-count": "Количество цифр не совпадает",
                "--symbols-count": "Количество специальных символов не совпадает",
                "--space": "Не должно быть пробелов",
                "--ease": "Пароль слишком простой",
                "--req-symbols": "В пароле должен быть указанные символы",
                "--length-low": "Пароль слишком короткий",
                "--length-height": "Слишком длинный",
                # email
                "--not-domain": "Ошибка домена",
                "--not-symbol": "Недопустимый символ",
                "--first_symbol": "Недопустимый первый или последний символ",
                # date
                "--date-min": "Дата меньше минимальной",
                "--date-max": "Дата больше максимальной",
                "--date": "Неверная дата"
            },
            "en": {
                # dock
                "--dock--": "Documentation: https://github.com/pavelglazunov/Check-Password",
                # password
                "--lower": "Password must contain lowercase characters",
                "--upper": "Password must contain uppercase characters",
                "--number": "Password must contain numbers",
                "--symbols": "Password must contain special characters",
                "--lower-count": "The number of lowercase letters does not match",
                "--upper-count": "The number of uppercase letters does not match",
                "--number-count": "The number of digits does not match",
                "--symbols-count": "The number of special characters does not match",
                "--space": "Must not contain spaces",
                "--ease": "Password is too simple",
                "--req-symbols": "The password must contain the specified characters",
                "--length-low": "Password is too short",
                "--length-height": "Is too long",
                # email
                "--not-domain": "Domain error",
                "--not-symbol": "Invalid character",
                "--first_symbol": "Invalid first or last character",
                # date
                "--date-min": "Date less than minimum",
                "--date-max": "Date greater than maximum",
                "--date": "Wrong date"
            }
        }
        self.numbers = re.compile(r"[0-9]")
        self.uppers = re.compile(r"[A-Z]")
        self.lowers = re.compile(r"[a-z]")
        self.symbols = re.compile(r"\W")
        self.all_letters = re.compile(r"[A-Za-z]")

    def help(self):
        print(self.fraze[self.language]["--dock--"])

    def _get_recommendation(self, param, count, need) -> list:
        result = list()
        result.append(self.fraze[self.language][param] * (count == 0))
        if need != count and type(need) == int:
            result.append(self.fraze[self.language][f"{param}-count"])
        return result

    def password(self,
                 password: str,
                 result_type: str = "bool",
                 upper: bool | int = True,
                 lower: bool | int = True,
                 numbers: bool | int = True,
                 symbols: bool | int = True,
                 spaces: bool = False,
                 check_simple_password=None,
                 min_length: int = 6,
                 max_length: int = 128,
                 max_similarity: int = 0.7,
                 required_symbol: str = "") -> bool | str | list:
        """
                :param password: Пароль, который необходимо проверить
                :param result_type: Тип данных результата -> bool | str | list
                :param upper: Наличие или количество букв верхнего регистра
                :param lower: Наличие или количество букв нижнего регистра
                :param numbers: Наличие или количество цифр
                :param symbols: Наличие или количество специальных символов
                :param spaces: Наличие пробелов в пароле
                :param check_simple_password: Файл с простыми паролями
                :param min_length: минимальная длина пароля
                :param max_length: максимальная длина пароля
                :param max_similarity: максимальный коэффициент схожести пароля от 0 до 1, рекомендуется 0.75
                :param required_symbol: строка символов, который обязаны быть в пароле
                :return: if result_type="bool" :return True/False
                         if result_type="list" :return Список рекомендаций/ошибок в пароле
                         if result_type="str"  :return Строку рекомендаций/ошибок в пароле
                """

        recommendation = []

        #  Генерация списка с количеством символов разного типа в порядке: lower, upper, num, symbol
        count_of_symbols_type = list(map(len, [
            self.lowers.findall(password),
            self.uppers.findall(password),
            self.numbers.findall(password),
            self.symbols.findall(password)
        ]))

        #  Проверки на различные символы - заглавные, строчные, цифры, спец. символы
        recommendation += self._get_recommendation("--lower", count_of_symbols_type[0], lower) * bool(lower)
        recommendation += self._get_recommendation("--upper", count_of_symbols_type[1], upper) * bool(upper)
        recommendation += self._get_recommendation("--number", count_of_symbols_type[2], numbers) * bool(numbers)
        recommendation += self._get_recommendation("--symbols", count_of_symbols_type[3], symbols) * bool(symbols)

        #  Проверки на длину
        recommendation.append(self.fraze[self.language]["--length-low"] * (len(password) < min_length))
        recommendation.append(self.fraze[self.language]["--length-height"] * (len(password) > max_length))

        #  Проверка на пробелы
        recommendation.append(self.fraze[self.language]["--space"] * (" " in password) * (not (bool(spaces))))

        #  Проверка на схожесть с паролями из фала
        if check_simple_password:
            with check_simple_password as f:
                for line in dropwhile(lambda x: x.startswith('#'), f):
                    common = line.strip().split(':')[-1]
                    diff = SequenceMatcher(a=password.lower(), b=common)
                    if diff.ratio() >= max_similarity:
                        recommendation.append(self.fraze[self.language]["--ease"])
                        break

        #  Проверка на обязательные символы (указанные пользователем)
        for s in required_symbol:
            if s not in password:
                recommendation.append(self.fraze[self.language]["--req-symbols"] * bool(required_symbol))

        return return_answer(recommendation, res_type=result_type)

    def email(self,
              email: str,
              result_type: str = "bool"):
        recommendations = []

        recommendations.append(self.fraze[self.language]["--not-domain"] * (email.count("@") == 1))
        recommendations.append(self.fraze[self.language]["--length-height"] * len(email) > 320)
        recommendations.append(self.fraze[self.language]["--space"] * (" " in email))

        return return_answer(recommendations, res_type=result_type)

    def date(self,
             date: str,
             date_split: str = "-",
             date_format: str = "d/m/y",
             min_year: str = "01-01-1900",
             max_year: str = "01-01-3000",
             result_type: str = "bool"):
        result = []
        formats = {
            "d/m/y": "%d-%m-%Y",
            "d/y/m": "%d-%Y-%m",
            "m/d/y": "%m-%d-%Y",
            "m/y/d": "%m-%Y-%d",
            "y/m/d": "%Y-%m-%d",
            "y/d/m": "%Y-%d-%m",
        }
        date = "-".join(date.split(date_split))

        try:
            val_date = time.strptime(date, formats[date_format])
            d, m, y = val_date.tm_mday, val_date.tm_mon, val_date.tm_year

            min_date = datetime.datetime.strptime(min_year, "%d-%m-%Y")
            now_date = datetime.datetime.strptime(f"{d}-{m}-{y}", "%d-%m-%Y")
            max_date = datetime.datetime.strptime(max_year, "%d-%m-%Y")

            if now_date < min_date:
                result.append(self.fraze[self.language]["--date-min"])
            if now_date > max_date:
                result.append(self.fraze[self.language]["--date-max"])
        except ValueError:
            result.append(self.fraze[self.language]["--date"])

        return return_answer(result, res_type=result_type)


class Generate:
    def __init__(self):
        self.lowers = "qwertyuiopasdfghjklzxcvbnm"
        self.uppers = "QWERTYUIOPASDFGHJKLZXCVBNM"
        self.nums = "0123456789"
        self.symbols = "~!@#$%^&*()[]{}-_=+"

    def passwords(self,
                  length: int = 11,
                  count: int = 1,
                  upper: bool = True,
                  number: bool = True,
                  symbol: bool = True
                  ):

        if length < 6:
            raise PasswordLengthException("Length mast be >= 6")

        result = []
        for c in range(count):
            start_password = random.choice(self.lowers) + \
                             random.choice(self.uppers) * upper + \
                             random.choice(self.nums) * number + \
                             random.choice(self.symbols) * symbol
            for i in range(4, length):
                start_password += random.choice(
                    [i for i in f"{self.lowers}{self.uppers * upper}{self.nums * number}{self.symbols * symbol}"])
            result_password = ''.join(random.sample(start_password, len(start_password)))

            result.append("".join(result_password))

        return result
