from services.stripes import get_full_width_and_stripes
from keyboards.keyboards import MATERIALS, OPTIONS


def calc(width, height, material, options):
    full_width_and_stripes_tuple = get_full_width_and_stripes(width)

    full_width = full_width_and_stripes_tuple[0]
    stripes = full_width_and_stripes_tuple[1]
    area = full_width * height
    price_per_m2 = {
        MATERIALS[0]: 300,
        MATERIALS[1]: 500,
        MATERIALS[2]: 600,
        MATERIALS[3]: 700,
    }[material]
    base_cost = int(area * price_per_m2)
    opts = []
    opts_sum = 0
    if OPTIONS[0] in options:
        opts.append(f"{OPTIONS[0]} — 300₽")
        opts_sum += 300
    if OPTIONS[1] in options:
        opts.append(f"{OPTIONS[1]} — 100₽")
        opts_sum += 100
    total = base_cost + opts_sum
    return {
        "material": material,
        "height": height,
        "width": width,
        "stripes": stripes,
        "width_with_allowance": full_width,
        "area": area,
        "base_cost": base_cost,
        "opts": opts,
        "opts_sum": opts_sum,
        "total": total,
    }
