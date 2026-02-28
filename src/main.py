from src.consumer import consumer
from src.sources import GeneratorSource, FileSource
from src.constants import TASKS_FILE, API_URL
from src.sources.api_source import ApiSource


def main() -> None:
    """
    Обязательнная составляющая программ, которые сдаются. Является точкой входа в приложение
    :return: Данная функция ничего не возвращает
    """
    sources = [GeneratorSource(), FileSource(TASKS_FILE), ApiSource(API_URL)]
    for source in sources:
        consumer(source)


if __name__ == "__main__":
    main()
