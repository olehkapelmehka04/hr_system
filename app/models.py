import json
from pickletools import int4


from app.validate import (
    validate_full_name,
    validate_age,
    validate_email,
    validate_status,
    validate_id,
)
from .loger import logger


class Candidate:
    def __init__(self, full_name: str, age: int, email: str):
        self.id = 0
        self.full_name = full_name
        self.age = age
        self.email = email
        self.status = "new"

    def edit_candidate(self, new_value: str | int, choice: int) -> str:
        if choice == 1:
            self.full_name = new_value
            return "ФИО изменено"
        elif choice == 2:
            self.age = new_value
            return "Возраст изменен"
        elif choice == 3:
            self.email = new_value
            return "Почта изменена"
        elif choice == 4:
            self.status = new_value
            return "Статус изменен"
        else:
            raise ValueError("Некорректный выбор действия")

    def to_dict(self) -> dict:
        return {
            self.id: {
                "full_name": self.full_name,
                "age": self.age,
                "email": self.email,
                "status": self.status,
            }
        }

    def __str__(self):
        return f"ID: {self.id} | ФИО: {self.full_name} | Возраст: {self.age} | Почта: {self.email} | Статус: {self.status}"


class HrBase:
    def __init__(self) -> None:
        self.local_base = list()

    def add_condidate(self, candidate: Candidate) -> Candidate:
        candidate.id = len(self.local_base) + 1
        self.local_base.append(candidate)
        return candidate

    def get_all_candidates(self) -> str:
        return "\n".join(str(candidate) for candidate in self.local_base)

    def find_candidate_by_str(self, search: str) -> str | None:
        list_candidates = list()
        search = search.lower()
        for candidate in self.local_base:
            if search in candidate.full_name.lower():
                list_candidates.append(candidate)
        if not list_candidates:
            return None
        return "\n".join(str(candidate) for candidate in list_candidates)

    def find_candidate_by_id(self, id: int) -> Candidate | None:
        for candidate in self.local_base:
            if candidate.id == id:
                return candidate
        return None

    def filter_candidate(self, filter: str) -> str | None:
        list_candidates = list()
        for candidate in self.local_base:
            if candidate.status == filter:
                list_candidates.append(candidate)
        if not list_candidates:
            return None
        return "\n".join(str(candidate) for candidate in list_candidates)

    def save_in_base(self) -> str:
        try:
            data = [candidate.to_dict() for candidate in self.local_base]
            with open("app/database.json", "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            return f"Данные успешно сохранены"
        except (json.JSONDecodeError, FileNotFoundError):
            return "Список пуст или файл не найден"

    def load_base(self):
        try:
            self.local_base = []
            with open("app/database.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                for candidate_data in data:
                    for candidate_info in candidate_data.values():
                        candidate = Candidate(
                            candidate_info["full_name"],
                            candidate_info["age"],
                            candidate_info["email"],
                        )
                        self.add_condidate(candidate)
            return "База успешно обновлена"
        except (json.JSONDecodeError, FileNotFoundError):
            return "Список пуст или файл не найден"

    def del_candidate(self, candidate: Candidate):
        self.local_base.remove(candidate)
        return f"Кандидат {candidate.full_name} успешно удален"


class Menu:
    def __init__(self) -> None:
        self.base = HrBase()

    def display_menu(self):
        print(
            """
──────────────────────────────────────────────────────
          🎯 HR-СИСТЕМА: Управление кандидатами
──────────────────────────────────────────────────────
    
    [1] Добавить кандидата
    [2] Просмотреть всех кандидатов
    [3] Найти кандидата (по ID или ФИО)
    [4] Фильтровать по статусу
    [5] Редактировать кандидата
    [6] Удалить кандидата
    [7] Сохранить данные
    [8] Загрузить данные
    [9] Выход

    """
        )

    def add_candidate(self):
        full_name = input("Введите ФИО кандидата: ")
        full_name = validate_full_name(full_name)
        age = input("Введите возраст кандидата: ")
        age = validate_age(age)
        email = input("Введите эл.почту кандидата: ")
        email = validate_email(email)
        condidate = Candidate(full_name, age, email)
        print(self.base.add_condidate(condidate))

    def get_all_candidates(self):
        candidates = self.base.get_all_candidates()
        if candidates:
            print(candidates)
        else:
            print("Список пуст")

    def find_candidate(self):
        input_str = input("Введите ФИО или ID: ")
        if input_str.isalpha():
            candidate = self.base.find_candidate_by_str(input_str)
        elif input_str.isdigit():
            id = validate_id(input_str)
            candidate = self.base.find_candidate_by_id(id)
        else:
            raise ValueError("Введите корректно ФИО или ID")
        if candidate is None:
            return "Кандидат(ы) не найден(ы)"
        return candidate

    def filter_by_status(self):
        print(f"Доступные статусы: \n- new\n- interviewed\n- rejected \n- hired")
        status = input("Введите статус: ")
        status = validate_status(status.lower())
        print(self.base.filter_candidate(status))

    def edit_candidate(self):
        id = input("Введите ID кандидата: ")
        if id.isalpha():
            raise ValueError("Некоррентый ID")
        valid_id = validate_id(id)
        candidate = self.base.find_candidate_by_id(valid_id)
        if candidate is None:
            return "Кандидат с таким ID не найден"
        print(candidate)
        print(
            """
[1] Изменить ФИО кандидата
[2] Изменить возраст кандидата
[3] Изменить почту кандидата
[4] Изменить статус кандидата
                """
        )
        choice = input("Выберите действие (1-4): ")
        if not choice.isdigit():
            raise ValueError("Некорректное действие")
        if choice == "1":
            new_value = input("Введите новое значение: ")
            new_value = validate_full_name(new_value)
            return candidate.edit_candidate(new_value, int(choice))
        elif choice == "2":
            new_value = input("Введите новое значение: ")
            new_value = validate_age(new_value)
            return candidate.edit_candidate(new_value, int(choice))
        elif choice == "3":
            new_value = input("Введите новое значение: ")
            new_value = validate_email(new_value)
            return candidate.edit_candidate(new_value, int(choice))
        elif choice == "4":
            new_value = input("Введите новое значение: ")
            new_value = validate_status(new_value.lower())
            return candidate.edit_candidate(new_value, int(choice))
        else:
            raise ValueError("Некорректное действие")

    def delete_candidate(self):
        id = input("Введите ID кандидата: ")
        if not id.isdigit():
            raise ValueError("Некорректный ID")
        valid_id = validate_id(id)
        candidate = self.base.find_candidate_by_id(valid_id)
        if candidate is None:
            return "Кандидат с таким ID не найден"
        print(candidate)
        confirm = input("Точно хотите удалить этого кандидата? (Да или Нет): ")
        if confirm.capitalize() == "Да":
            return self.base.del_candidate(candidate)

        else:
            return "Отмена ..."

    def save_to_base(self):
        print(self.base.save_in_base())

    def upload_to_base(self):
        return self.base.load_base()

    def run(self):
        self.upload_to_base()
        while True:
            self.display_menu()
            try:
                choice = input("Выберите действие (1-9): ")
                if choice == "1":
                    self.add_candidate()
                elif choice == "2":
                    self.get_all_candidates()
                elif choice == "3":
                    print(self.find_candidate())
                elif choice == "4":
                    self.filter_by_status()
                elif choice == "5":
                    print(self.edit_candidate())
                elif choice == "6":
                    print(self.delete_candidate())
                elif choice == "7":
                    self.save_to_base()
                elif choice == "8":
                    print(self.upload_to_base())
                elif choice == "9":
                    print("Программа остановлена")
                    break
                else:
                    print("Некорректный ввод")
            except ValueError as e:
                print(e)
                logger.error(str(e), exc_info=True)
