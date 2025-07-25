# Таблица: кортежи (максимальная ширина, количество полос)
from typing import Any

WIDTH_THRESHOLDS = [
    (0.8, 1),
    (1.2, 1.5),
    (1.7, 2),
    (2.1, 2.5),
    (2.6, 3),
    (3.0, 3.5),
    (3.5, 4),
    (3.9, 4.5),
    (4.4, 5),
    (4.8, 5.5),
    (5.2, 6),
    (5.7, 6.5),
    (6.1, 7),
    (6.6, 7.5),
    (7.0, 8),
    (7.4, 8.5),
    (7.9, 9)
]



def get_full_width_and_stripes(width: float) -> tuple[Any, Any]:
    """
    Возвращает минимальное количество полос, достаточное для заданной ширины изделия.
    """
    for threshold_width, stripes in WIDTH_THRESHOLDS:
        if width <= threshold_width:
            return threshold_width, stripes
    raise ValueError("Ширина превышает максимально допустимую")
