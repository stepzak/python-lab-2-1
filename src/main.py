import sys

from src.consumer import consumer
from src.sources import FileSource
from src.constants import TASKS_FILE
import logging

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

def main() -> None:
    """
    Обязательнная составляющая программ, которые сдаются. Является точкой входа в приложение
    :return: Данная функция ничего не возвращает
    """
    sources = [FileSource(TASKS_FILE)]
    for source in sources:
        consumer(source)


if __name__ == "__main__":
    main()
