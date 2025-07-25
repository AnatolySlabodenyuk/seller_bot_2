from services.price import MATERIAL_PRICES
from services.stripes import get_full_width_and_stripes
from keyboards.keyboards import MATERIALS


def calc(width, height, material):
    full_width_and_stripes_tuple = get_full_width_and_stripes(width)
    full_width = full_width_and_stripes_tuple[0]
    stripes = full_width_and_stripes_tuple[1]
    area = round(full_width * height, 2)
    price_per_m2 = {
        MATERIALS[0]: MATERIAL_PRICES[0],
        MATERIALS[1]: MATERIAL_PRICES[1],
        MATERIALS[2]: MATERIAL_PRICES[2],
        MATERIALS[3]: MATERIAL_PRICES[3],
    }[material]
    total = int(area * price_per_m2)
    formatted_total = f'{total:,}'.replace(',', ' ')

    return {
        "material": material,
        "height": height,
        "width": width,
        "stripes": stripes,
        "width_with_allowance": full_width,
        "area": area,
        "total": formatted_total,
    }
