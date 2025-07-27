from PIL import Image, ImageDraw, ImageFont
import io


def generate_curtain_sketch(width_m, height_m, grommet_step_cm=30, grommet_diameter_mm=12):
    """
    Генерирует изображение шторы с размерами, шагом и количеством люверсов.
    """
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
    img = Image.new('RGB', (img_w, img_h), 'black')
    draw = ImageDraw.Draw(img)

    # Основная рамка шторы
    draw.rectangle([x0, y0, x1, y1], outline='red', width=6)

    # Верхняя полоса для люверсов
    grommet_bar_h = 50
    draw.line([x0, y0 + grommet_bar_h, x1, y0 + grommet_bar_h], fill='red', width=6)

    # Люверсы (автоподбор количества)
    px_per_m = curtain_w / width_m if width_m else 1
    grommet_diameter_px = max(6, grommet_diameter_mm / 1000 * px_per_m)

    # Подбираем количество люверсов, чтобы шаг был близок к заданному
    target_step_px = grommet_step_cm / 100 * px_per_m
    grommet_count = max(2, int(round(curtain_w / target_step_px)) + 1)

    if grommet_count > 1:
        actual_step_px = (curtain_w - grommet_diameter_px) / (grommet_count - 1)
    else:
        actual_step_px = 0

    for i in range(grommet_count):
        gx = x0 + grommet_diameter_px / 2 + i * actual_step_px
        gy = y0 + grommet_bar_h / 2
        r = grommet_diameter_px / 2
        draw.ellipse([gx - r, gy - r, gx + r, gy + r], outline='red', width=3)

    # Шрифты
    try:
        font = ImageFont.truetype("arial.ttf", 48)
        font_small = ImageFont.truetype("arial.ttf", 32)
    except:
        font = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # === Подписи ===
    # Высота (слева, центрируется по вертикали)
    height_text = f"{height_m:.2f}"
    bbox_h = draw.textbbox((0, 0), height_text, font=font)
    text_w_h = bbox_h[2] - bbox_h[0]
    text_h_h = bbox_h[3] - bbox_h[1]
    draw.text(
        (x0 - text_w_h - 20, (y0 + y1) // 2 - text_h_h // 2),
        height_text, fill='red', font=font
    )

    # Ширина (снизу, центрируется по горизонтали)
    width_text = f"{width_m:.2f}"
    bbox_w = draw.textbbox((0, 0), width_text, font=font)
    text_w_w = bbox_w[2] - bbox_w[0]
    draw.text(
        ((x0 + x1) // 2 - text_w_w // 2, y1 + 10),
        width_text, fill='red', font=font
    )

    # Верхняя подпись
    top_text = f"Шаг люверсов +/-{grommet_step_cm}см, диаметр {grommet_diameter_mm}мм"
    bbox_top = draw.textbbox((0, 0), top_text, font=font_small)
    top_w = bbox_top[2] - bbox_top[0]
    draw.text(
        ((img_w - top_w) // 2, y0 - grommet_bar_h - 40),
        top_text, fill='white', font=font_small
    )

    # Информация о люверсах
    approx_step_cm = curtain_w / (grommet_count - 1) / px_per_m * 100
    grommet_info = f"Люверсов: {grommet_count}, шаг ≈ {approx_step_cm:.0f}см"
    bbox_g = draw.textbbox((0, 0), grommet_info, font=font_small)
    g_w = bbox_g[2] - bbox_g[0]
    draw.text(
        ((img_w - g_w) // 2, y0 + grommet_bar_h + 10),
        grommet_info, fill='white', font=font_small
    )

    # Сохраняем
    output = io.BytesIO()
    img.save(output, format='PNG')
    output.seek(0)
    return output
