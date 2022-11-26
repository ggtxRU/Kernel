from db.enum.base import StrEnum


class CalculationStatusEnum(StrEnum):
    """
    Enum of possible calculation statuses.

    complete: Завершен
    in_progress: В процессе выполнения
    in_the_queue: В очереди на выполнение
    """

    complete = 'complete'
    in_progress = 'in_progress'
    in_the_queue = 'in_the_queue'
