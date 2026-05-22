from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from typing import Any, Callable, Generic, TypeVar


T = TypeVar("T")
R = TypeVar("R")


# ---------------------------------------------------------------------------
# Допоміжні функції
# ---------------------------------------------------------------------------

def print_header(title: str) -> None:
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def divide(a: float, b: float) -> float:
    return a / b


# ---------------------------------------------------------------------------
# Завдання 1. Аналіз коду
# ---------------------------------------------------------------------------

def divide_with_try_except(a: float, b: float) -> float | str:
    try:
        return a / b
    except ZeroDivisionError:
        return "division by zero"


def task_1_code_analysis() -> None:
    print_header("Завдання 1. Аналіз коду")

    print("Оригінальна функція:")
    print("def divide(a, b):")
    print("    return a / b")

    print("\nЩо станеться при b = 0?")
    print("- Буде виняток ZeroDivisionError.")
    print("- Якщо його не обробити, програма аварійно завершить поточне виконання.")

    print("\nВаріант через try/except:")
    print(f"divide_with_try_except(10, 2) = {divide_with_try_except(10, 2)}")
    print(f"divide_with_try_except(10, 0) = {divide_with_try_except(10, 0)}")

    print(
        "\nНедоліки підходу try/except:\n"
        "- Прихована логіка: помилка не видно в типі повернення функції.\n"
        "- Побічні ефекти: обробник може логувати, друкувати, змінювати стан або маскувати проблему.\n"
        "- Складність композиції: важче будувати ланцюжки функцій, бо кожен етап може кинути виняток.\n"
        "- Результат функції стає неоднорідним: іноді число, іноді рядок з помилкою."
    )


# ---------------------------------------------------------------------------
# Завдання 2. Safe-функція
# ---------------------------------------------------------------------------

def safe_divide_tuple(a: float, b: float) -> tuple[str, float | str]:
    if b == 0:
        return "error", "division by zero"

    return "ok", a / b


def task_2_safe_function() -> None:
    print_header("Завдання 2. Safe-функція")

    print(f"safe_divide_tuple(10, 2) = {safe_divide_tuple(10, 2)}")
    print(f"safe_divide_tuple(10, 0) = {safe_divide_tuple(10, 0)}")

    print(
        "\nПояснення:\n"
        "- Виняток не виходить назовні.\n"
        "- Функція явно повертає один із двох станів: ok або error.\n"
        "- Код, який викликає функцію, може перевірити перший елемент tuple."
    )


# ---------------------------------------------------------------------------
# Завдання 3-6. Option
# ---------------------------------------------------------------------------

class Option(Generic[T]):
    """Базовий клас для Some / Nothing."""

    def map(self, func: Callable[[T], R]) -> "Option[R]":
        raise NotImplementedError


class Some(Option[T]):
    def __init__(self, value: T):
        self.value = value

    def map(self, func: Callable[[T], R]) -> "Option[R]":
        return Some(func(self.value))

    def __repr__(self) -> str:
        return f"Some({self.value!r})"


class Nothing(Option[Any]):
    def map(self, func: Callable[[Any], R]) -> "Nothing":
        return self

    def __repr__(self) -> str:
        return "Nothing()"


def safe_divide_option(a: float, b: float) -> Option[float]:
    if b == 0:
        return Nothing()

    return Some(a / b)


def task_3_option_model() -> None:
    print_header("Завдання 3. Реалізація Option")

    some_value = Some(10)
    nothing_value = Nothing()

    print(f"some_value = {some_value}")
    print(f"nothing_value = {nothing_value}")

    print(
        "\nПояснення:\n"
        "- Some(value) означає, що значення існує.\n"
        "- Nothing() означає відсутність значення.\n"
        "- Option дозволяє явно моделювати можливу відсутність результату."
    )


def task_4_option_safe_function() -> None:
    print_header("Завдання 4. Safe функція з Option")

    print(f"safe_divide_option(10, 2) = {safe_divide_option(10, 2)}")
    print(f"safe_divide_option(10, 0) = {safe_divide_option(10, 0)}")


def task_5_option_map() -> None:
    print_header("Завдання 5. Map для Option")

    result_1 = Some(10).map(lambda x: x * 2)
    result_2 = Nothing().map(lambda x: x * 2)

    print(f"Some(10).map(lambda x: x * 2) = {result_1}")
    print(f"Nothing().map(lambda x: x * 2) = {result_2}")

    print(
        "\nПояснення:\n"
        "- Some(x).map(f) застосовує f до x і повертає Some(f(x)).\n"
        "- Nothing().map(f) нічого не виконує і повертає Nothing()."
    )


def task_6_option_chain() -> None:
    print_header("Завдання 6. Ланцюжок обчислень")

    success = (
        safe_divide_option(10, 2)
        .map(lambda x: x * 2)
        .map(lambda x: x + 5)
    )

    failure = (
        safe_divide_option(10, 0)
        .map(lambda x: x * 2)
        .map(lambda x: x + 5)
    )

    print("Успішний pipeline:")
    print(f"safe_divide_option(10, 2).map(*2).map(+5) = {success}")

    print("\nPipeline з помилкою:")
    print(f"safe_divide_option(10, 0).map(*2).map(+5) = {failure}")

    print(
        "\nПояснення:\n"
        "- Якщо результат Some, обчислення продовжується.\n"
        "- Якщо результат Nothing, наступні map не виконують функції."
    )


# ---------------------------------------------------------------------------
# Завдання 7-11. Result
# ---------------------------------------------------------------------------

class Result(Generic[T]):
    """Базовий клас для Ok / Error."""

    def map(self, func: Callable[[T], R]) -> "Result[R]":
        raise NotImplementedError

    def flat_map(self, func: Callable[[T], "Result[R]"]) -> "Result[R]":
        raise NotImplementedError


class Ok(Result[T]):
    def __init__(self, value: T):
        self.value = value

    def map(self, func: Callable[[T], R]) -> "Result[R]":
        return Ok(func(self.value))

    def flat_map(self, func: Callable[[T], Result[R]]) -> "Result[R]":
        return func(self.value)

    def __repr__(self) -> str:
        return f"Ok({self.value!r})"


class Error(Result[Any]):
    def __init__(self, message: Any):
        self.message = message

    def map(self, func: Callable[[Any], R]) -> "Error":
        return self

    def flat_map(self, func: Callable[[Any], Result[R]]) -> "Error":
        return self

    def __repr__(self) -> str:
        return f"Error({self.message!r})"


def safe_divide_result(a: float, b: float) -> Result[float]:
    if b == 0:
        return Error("division by zero")

    return Ok(a / b)


def task_7_result_model() -> None:
    print_header("Завдання 7. Реалізація Result")

    ok_value = Ok(100)
    error_value = Error("some error")

    print(f"ok_value = {ok_value}")
    print(f"error_value = {error_value}")

    print(
        "\nПояснення:\n"
        "- Ok(value) містить успішний результат.\n"
        "- Error(message) містить інформацію про помилку.\n"
        "- На відміну від Option, Result не просто каже 'немає значення', а пояснює чому."
    )


def task_8_result_safe_function() -> None:
    print_header("Завдання 8. Safe функції з Result")

    print(f"safe_divide_result(10, 2) = {safe_divide_result(10, 2)}")
    print(f"safe_divide_result(10, 0) = {safe_divide_result(10, 0)}")


def task_9_result_map() -> None:
    print_header("Завдання 9. Map для Result")

    result_1 = Ok(10).map(lambda x: x * 2)
    result_2 = Error("bad value").map(lambda x: x * 2)

    print(f"Ok(10).map(lambda x: x * 2) = {result_1}")
    print(f"Error('bad value').map(lambda x: x * 2) = {result_2}")

    print(
        "\nПояснення:\n"
        "- Ok(x).map(f) повертає Ok(f(x)).\n"
        "- Error(e).map(f) не викликає f і повертає Error(e)."
    )


def task_10_flat_map() -> None:
    print_header("Завдання 10. FlatMap")

    success = (
        safe_divide_result(10, 2)
        .flat_map(lambda x: safe_divide_result(x, 5))
    )

    failure = (
        safe_divide_result(10, 2)
        .flat_map(lambda x: safe_divide_result(x, 0))
    )

    print(f"safe_divide_result(10, 2).flat_map(divide by 5) = {success}")
    print(f"safe_divide_result(10, 2).flat_map(divide by 0) = {failure}")

    print(
        "\nПояснення:\n"
        "- map потрібен для функцій, які повертають звичайне значення.\n"
        "- flat_map потрібен для функцій, які самі повертають Result.\n"
        "- Без flat_map вийшла б вкладеність типу Ok(Ok(value)) або Ok(Error(...))."
    )


def safe_pipeline(x: float) -> Result[float]:
    return (
        safe_divide_result(x, 2)
        .map(lambda value: value + 10)
        .flat_map(lambda value: safe_divide_result(value, 0))
    )


def task_11_pipeline_without_try_except() -> None:
    print_header("Завдання 11. Pipeline без try/except")

    result = safe_pipeline(10)

    print("Pipeline:")
    print("safe_divide_result(x, 2)")
    print("    .map(lambda value: value + 10)")
    print("    .flat_map(lambda value: safe_divide_result(value, 0))")
    print(f"\nРезультат safe_pipeline(10) = {result}")

    print(
        "\nПояснення:\n"
        "- safe_divide_result(10, 2) повертає Ok(5.0).\n"
        "- map додає 10 і отримує Ok(15.0).\n"
        "- flat_map намагається поділити 15.0 на 0.\n"
        "- Pipeline зупиняється на safe_divide_result(15.0, 0), результат: Error('division by zero')."
    )


# ---------------------------------------------------------------------------
# Завдання 12. Обробка користувача без try/except
# ---------------------------------------------------------------------------

def is_int_string(value: Any) -> bool:
    if not isinstance(value, str):
        return False

    return re.fullmatch(r"[+-]?\d+", value.strip()) is not None


def parse_int_safe(value: Any) -> Result[int]:
    if isinstance(value, int) and not isinstance(value, bool):
        return Ok(value)

    if is_int_string(value):
        return Ok(int(str(value).strip()))

    return Error(f"cannot parse int from {value!r}")


def get_age(user: dict[str, Any]) -> Result[Any]:
    if "age" not in user:
        return Error("age is required")

    return Ok(user["age"])


def validate_adult(age: int) -> Result[int]:
    if age > 18:
        return Ok(age)

    return Error("age must be greater than 18")


def process_user_age(user: dict[str, Any]) -> Result[int]:
    return (
        get_age(user)
        .flat_map(parse_int_safe)
        .flat_map(validate_adult)
    )


def task_12_user_processing() -> None:
    print_header("Завдання 12. Обробка користувача")

    users = [
        {"age": "25"},
        {"age": "17"},
        {"age": "abc"},
        {},
    ]

    for user in users:
        print(f"{user} -> {process_user_age(user)}")

    print(
        "\nПояснення:\n"
        "- try/except не використовується.\n"
        "- Перед int(...) виконується перевірка формату рядка.\n"
        "- Кожен крок повертає Result, тому pipeline можна будувати через flat_map."
    )


# ---------------------------------------------------------------------------
# Завдання 13. Обробка файлу
# ---------------------------------------------------------------------------

FAKE_FILES = {
    "hello.txt": "Hello from file",
    "data.txt": "100\n200\n300",
}


def read_file(name: str) -> Result[str]:
    if name not in FAKE_FILES:
        return Error("file not found")

    return Ok(FAKE_FILES[name])


def task_13_file_processing() -> None:
    print_header("Завдання 13. Обробка файлу")

    print(f"read_file('hello.txt') = {read_file('hello.txt')}")
    print(f"read_file('missing.txt') = {read_file('missing.txt')}")

    print(
        "\nПояснення:\n"
        "- read_file імітує файлову систему через словник FAKE_FILES.\n"
        "- Якщо файл існує, повертається Ok(content).\n"
        "- Якщо файлу немає, повертається Error('file not found')."
    )


# ---------------------------------------------------------------------------
# Завдання 14. Multiple validations
# ---------------------------------------------------------------------------

def validate_user_all(user: dict[str, Any]) -> Result[dict[str, Any]]:
    errors: list[str] = []

    name = user.get("name")
    age = user.get("age")

    if not isinstance(name, str) or not name.strip():
        errors.append("name must be non-empty")

    if not isinstance(age, int) or isinstance(age, bool):
        errors.append("age must be integer")
    elif age < 18:
        errors.append("age must be >= 18")

    if errors:
        return Error(errors)

    return Ok(user)


def task_14_multiple_validations() -> None:
    print_header("Завдання 14. Multiple validations")

    users = [
        {"name": "Alice", "age": 17},
        {"name": "", "age": 15},
        {"name": "Bob", "age": 22},
        {"name": "Kate", "age": "old"},
    ]

    for user in users:
        print(f"{user} -> {validate_user_all(user)}")

    print(
        "\nПояснення:\n"
        "- На відміну від fail-fast pipeline, тут збираються всі помилки.\n"
        "- Якщо помилки є, повертається Error(list_of_errors).\n"
        "- Якщо помилок немає, повертається Ok(user)."
    )


# ---------------------------------------------------------------------------
# Завдання 15. Data processing pipeline
# ---------------------------------------------------------------------------

def get_amount(transaction: dict[str, Any]) -> Result[Any]:
    if "amount" not in transaction:
        return Error("amount is required")

    return Ok(transaction["amount"])


def validate_positive_amount(amount: int) -> Result[int]:
    if amount > 0:
        return Ok(amount)

    return Error("amount must be > 0")


def process_transaction(transaction: dict[str, Any]) -> Result[int]:
    return (
        get_amount(transaction)
        .flat_map(parse_int_safe)
        .flat_map(validate_positive_amount)
    )


@dataclass
class TransactionProcessingReport:
    total: int
    errors: list[str]

    def __repr__(self) -> str:
        return f"TransactionProcessingReport(total={self.total}, errors={self.errors!r})"


def process_transactions(transactions: list[dict[str, Any]]) -> TransactionProcessingReport:
    total = 0
    errors: list[str] = []

    for index, transaction in enumerate(transactions):
        result = process_transaction(transaction)

        if isinstance(result, Ok):
            total += result.value
        elif isinstance(result, Error):
            errors.append(f"transaction #{index}: {result.message}")

    return TransactionProcessingReport(total=total, errors=errors)


def task_15_data_processing_pipeline() -> None:
    print_header("Завдання 15. Data processing pipeline")

    transactions = [
        {"amount": "100"},
        {"amount": "abc"},
        {"amount": "200"},
        {"amount": "-50"},
        {},
    ]

    print("transactions:")
    for transaction in transactions:
        print(f"  {transaction}")

    report = process_transactions(transactions)

    print(f"\nReport: {report}")
    print(f"Total valid amount: {report.total}")
    print("Errors:")
    for error in report.errors:
        print(f"- {error}")

    print(
        "\nПояснення:\n"
        "- Кожна транзакція проходить pipeline: get_amount -> parse_int_safe -> validate_positive_amount.\n"
        "- Кожен етап повертає Result.\n"
        "- Валідні amount додаються до total.\n"
        "- Помилки не падають винятками, а збираються в report.errors."
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_selected_task(task_number: str) -> None:
    tasks: dict[str, Callable[[], None]] = {
        "1": task_1_code_analysis,
        "2": task_2_safe_function,
        "3": task_3_option_model,
        "4": task_4_option_safe_function,
        "5": task_5_option_map,
        "6": task_6_option_chain,
        "7": task_7_result_model,
        "8": task_8_result_safe_function,
        "9": task_9_result_map,
        "10": task_10_flat_map,
        "11": task_11_pipeline_without_try_except,
        "12": task_12_user_processing,
        "13": task_13_file_processing,
        "14": task_14_multiple_validations,
        "15": task_15_data_processing_pipeline,
    }

    if task_number == "all":
        for number in map(str, range(1, 16)):
            tasks[number]()
        return

    if task_number not in tasks:
        available = ", ".join(["all"] + list(tasks.keys()))
        raise ValueError(f"Невідоме завдання: {task_number}. Доступні варіанти: {available}")

    tasks[task_number]()


def main() -> None:
    parser = argparse.ArgumentParser(description="Завдання з Option, Result і safe pipeline у Python")
    parser.add_argument(
        "--task",
        default="all",
        help="Номер завдання: 1..15 або all. За замовчуванням: all",
    )

    args = parser.parse_args()
    run_selected_task(args.task)


if __name__ == "__main__":
    main()
