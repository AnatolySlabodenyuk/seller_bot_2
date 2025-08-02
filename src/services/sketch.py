import os
from PIL import Image, ImageDraw, ImageFont
import io


def draw_dashed_line(draw, xy, dash_length=8, gap_length=6, width=1, fill="black"):
    x0, y0, x1, y1 = xy
    if x0 == x1:  # вертикальная
        if y0 > y1: y0, y1 = y1, y0
        total_length = y1 - y0
        num_dashes = total_length // (dash_length + gap_length)
        for i in range(int(num_dashes) + 1):
            start = y0 + i * (dash_length + gap_length)
            end = min(start + dash_length, y1)
            draw.line([(x0, start), (x1, end)], fill=fill, width=width)
    elif y0 == y1:  # горизонтальная
        if x0 > x1: x0, x1 = x1, x0
        total_length = x1 - x0
        num_dashes = total_length // (dash_length + gap_length)
        for i in range(int(num_dashes) + 1):
            start = x0 + i * (dash_length + gap_length)
            end = min(start + dash_length, x1)
            draw.line([(start, y0), (end, y1)], fill=fill, width=width)


def calc_grommet_count(width_m, grommet_diameter_mm, grommet_step_cm):
    grommet_diameter_m = grommet_diameter_mm / 1000
    grommet_step_m = grommet_step_cm / 100
    available_width = width_m - grommet_diameter_m
    if available_width <= 0:
        return 2
    num_intervals = available_width / grommet_step_m
    grommet_count = int(round(num_intervals)) + 1
    return max(2, grommet_count)


def generate_curtain_sketch(
        width_m,
        height_m,
        grommet_step_cm=30,
        grommet_diameter_mm=12,
        grommet_count=7,
        grommet_diameter_px=35
):
    font_path = os.path.join(os.path.dirname(__file__), "..", "fonts", "arial.ttf")

    # Размер холста
    img_w, img_h = 800, 1000
    margin_top = 140
    margin_sides = 120
    margin_bottom = 120

    # Пропорции шторы
    aspect = width_m / height_m if height_m else 1
    max_curtain_w = img_w - 2 * margin_sides
    max_curtain_h = img_h - margin_top - margin_bottom

    if aspect > 1:
        curtain_w = max_curtain_w
        curtain_h = int(curtain_w / aspect)
        if curtain_h > max_curtain_h:
            curtain_h = max_curtain_h
            curtain_w = int(curtain_h * aspect)
    else:
        curtain_h = max_curtain_h
        curtain_w = int(curtain_h * aspect)
        if curtain_w > max_curtain_w:
            curtain_w = max_curtain_w
            curtain_h = int(curtain_w / aspect)

    # Координаты шторы
    x0 = (img_w - curtain_w) // 2
    y0 = margin_top
    x1 = x0 + curtain_w
    y1 = y0 + curtain_h

    # Создаём изображение
    img = Image.new('RGB', (img_w, img_h), 'white')
    draw = ImageDraw.Draw(img)

    # Основная рамка шторы
    draw.rectangle([x0, y0, x1, y1], outline='black', width=3)

    # Внутренний прямоугольник (пунктир)
    offset_in = 8
    ix0 = x0 + offset_in
    iy0 = y0 + offset_in
    ix1 = x1 - offset_in
    iy1 = y1 - offset_in

    draw_dashed_line(draw, (ix0, iy0, ix1, iy0), width=2)  # верх
    draw_dashed_line(draw, (ix1, iy0, ix1, iy1), width=2)  # право
    draw_dashed_line(draw, (ix1, iy1, ix0, iy1), width=2)  # низ
    draw_dashed_line(draw, (ix0, iy1, ix0, iy0), width=2)  # лево

    # --- Люверсы ---
    # Отступ для центров люверсов от края (визуально подберите, например, = grommet_diameter_px / 2 + 8)
    offset = grommet_diameter_px / 2 + 8
    step = (curtain_w - 2 * offset) / (grommet_count - 1)
    vertical_offset = offset  # grommet_diameter_px  # увеличенный отступ от верха

    for i in range(grommet_count):
        gx = x0 + offset + i * step
        gy = y0 + vertical_offset  # центры ниже верхнего края
        r = grommet_diameter_px / 2
        # Внешний круг люверса
        draw.ellipse([gx - r, gy - r, gx + r, gy + r], outline='black', width=4)
        # Внутренний круг
        draw.ellipse([gx - r / 1.9, gy - r / 1.9, gx + r / 1.9, gy + r / 1.9], outline='black', width=3)

    # Шрифты
    try:
        font = ImageFont.truetype(font_path, 40)
        font_small = ImageFont.truetype(font_path, 32)
    except:
        font = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Надпись высоты
    height_text = f"{height_m:.2f}"
    bbox_h = draw.textbbox((0, 0), height_text, font=font)
    text_w_h = bbox_h[2] - bbox_h[0]
    text_h_h = bbox_h[3] - bbox_h[1]
    draw.text((x0 - text_w_h - 20, (y0 + y1) // 2 - text_h_h // 2), height_text, fill='black', font=font)

    # Надпись ширины
    width_text = f"{width_m:.2f}"
    bbox_w = draw.textbbox((0, 0), width_text, font=font)
    text_w_w = bbox_w[2] - bbox_w[0]
    draw.text(((x0 + x1) // 2 - text_w_w // 2, y1 + 10), width_text, fill='black', font=font)

    # Верхняя подпись
    grommet_bar_h = 50
    top_text = f"Шаг люверсов +/- {grommet_step_cm} см, диаметр {grommet_diameter_mm} мм"
    bbox_top = draw.textbbox((0, 0), top_text, font=font_small)
    top_w = bbox_top[2] - bbox_top[0]
    draw.text(
        ((img_w - top_w) // 2, y0 - grommet_bar_h - 40),
        top_text, fill='black', font=font_small
    )

    # Нижняяя подпись
    grommet_count_auto = calc_grommet_count(width_m, grommet_diameter_mm, grommet_step_cm)
    grommet_info = f"Люверсов +/- {grommet_count_auto}"
    bbox_g = draw.textbbox((0, 0), grommet_info, font=font_small)
    g_w = bbox_g[2] - bbox_g[0]
    draw.text(
        ((img_w - g_w) // 2, y0 + grommet_bar_h + 30),
        grommet_info, fill='black', font=font_small
    )

    # Сохраняем
    output = io.BytesIO()
    img.save(output, format='PNG')
    output.seek(0)
    return output
