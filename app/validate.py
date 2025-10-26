import re

email_pattern = r"^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}$"


def validate_full_name(full_name):
    for word in full_name.split():
        if not word.isalpha():
            raise ValueError("Некорректное ФИО")
    if len(full_name.split()) <= 2:
        raise ValueError("Некорректное ФИО")
    if len(full_name.replace(" ", "")) <= 3:
        raise ValueError("Слишком короткое ФИО")
    return " ".join(
        [format_full_name.capitalize() for format_full_name in full_name.split()]
    )


def validate_age(age: str):
    if not age.isdigit():
        raise ValueError("Некорректный возраст")
    if age.startswith("0"):
        raise ValueError("Некорректный возраст")
    if int(age) <= 17 or int(age) >= 80:
        raise ValueError("Некорректный возраст")
    return int(age)


def validate_email(email):
    if not re.match(email_pattern, email):
        raise ValueError("Некорректная почта")
    return email


def validate_status(status):
    status_lst = ["new", "interviewed", "rejected", "hired"]
    if not status in status_lst:
        raise ValueError("Некорректный статус")
    return status


def validate_id(id):
    if id.startswith("0"):
        raise ValueError("Некорректный ID")
    return int(id)
