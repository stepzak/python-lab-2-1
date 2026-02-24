from src.consumer import consumer
from src.sources import GeneratorSource, FileSource
from src.constants import TASKS_FILE

def main() -> None:
    """
    Обязательнная составляющая программ, которые сдаются. Является точкой входа в приложение
    :return: Данная функция ничего не возвращает
    """
    gen = GeneratorSource()
    consumer(gen)
    file_source = FileSource(TASKS_FILE)
    consumer(file_source)


if __name__ == "__main__":
    main()
