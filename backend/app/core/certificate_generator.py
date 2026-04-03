# Sertifikat PDF generatori — reportlab bilan
# A4 landscape, chiroyli dizayn, faqat lotin harflar (Helvetica unicode cheklovlari tufayli)

import os
import random
import string
from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas as rl_canvas

# ─── Ranglar ─────────────────────────────────────────────────────────────────

DARK_BG       = colors.HexColor("#0F0E2A")      # qoʻyiq fon
CARD_BG       = colors.HexColor("#1C1A3E")      # karta foni
PRIMARY       = colors.HexColor("#14B8A6")      # teal primary
GOLD          = colors.HexColor("#F59E0B")      # oltin
LIGHT_GOLD    = colors.HexColor("#FDE68A")      # och oltin
CARD_BORDER   = colors.HexColor("#2E2B5A")      # karta chegarasi
TEXT_WHITE    = colors.white
TEXT_MUTED    = colors.HexColor("#A0AEC0")      # kulrang matn
ACCENT_LINE   = colors.HexColor("#14B8A6")      # ajratuvchi chiziq

# ─── Yordamchi funksiyalar ────────────────────────────────────────────────────

def _truncate(text: str, max_len: int) -> str:
    """Matnni belgilangan uzunlikda qisqartirish."""
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def _transliterate(text: str) -> str:
    """
    O'zbek kirill harflarini lotinga o'girish.
    Helvetica faqat lotin belgilarini to'g'ri ko'rsatadi.
    """
    table = {
        "А": "A", "а": "a", "Б": "B", "б": "b",
        "В": "V", "в": "v", "Г": "G", "г": "g",
        "Д": "D", "д": "d", "Е": "E", "е": "e",
        "Ё": "Yo", "ё": "yo", "Ж": "J", "ж": "j",
        "З": "Z", "з": "z", "И": "I", "и": "i",
        "Й": "Y", "й": "y", "К": "K", "к": "k",
        "Л": "L", "л": "l", "М": "M", "м": "m",
        "Н": "N", "н": "n", "О": "O", "о": "o",
        "П": "P", "п": "p", "Р": "R", "р": "r",
        "С": "S", "с": "s", "Т": "T", "т": "t",
        "У": "U", "у": "u", "Ф": "F", "ф": "f",
        "Х": "X", "х": "x", "Ц": "Ts", "ц": "ts",
        "Ч": "Ch", "ч": "ch", "Ш": "Sh", "ш": "sh",
        "Щ": "Sch", "щ": "sch", "Ъ": "", "ъ": "",
        "Ы": "I", "ы": "i", "Ь": "", "ь": "",
        "Э": "E", "э": "e", "Ю": "Yu", "ю": "yu",
        "Я": "Ya", "я": "ya",
        # O'zbek maxsus harflari
        "Ў": "O'", "ў": "o'", "Қ": "Q", "қ": "q",
        "Ғ": "G'", "ғ": "g'", "Ҳ": "H", "ҳ": "h",
        "Ҷ": "J", "ҷ": "j",
    }
    result = []
    for ch in text:
        result.append(table.get(ch, ch))
    return "".join(result)


def generate_certificate_number() -> str:
    """INKTALIM-YYYY-XXXXX formatida noyob raqam yaratish."""
    year = datetime.now().year
    suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return f"INKTALIM-{year}-{suffix}"


def _draw_background(c: rl_canvas.Canvas, w: float, h: float) -> None:
    """Gradient imitatsiya qiladigan qoʻyiq fon."""
    # Asosiy fon
    c.setFillColor(DARK_BG)
    c.rect(0, 0, w, h, stroke=0, fill=1)

    # Yuqori chap burchakda dekorativ doira
    c.setFillColorRGB(0.078, 0.075, 0.165, alpha=0.5)
    c.circle(0, h, 120 * mm, stroke=0, fill=1)

    # Pastki o'ng burchakda doira
    c.setFillColorRGB(0.082, 0.722, 0.651, alpha=0.07)
    c.circle(w, 0, 100 * mm, stroke=0, fill=1)


def _draw_corner_decorations(c: rl_canvas.Canvas, x: float, y: float, cw: float, ch: float) -> None:
    """Karta burchaklarida geometrik dekoratsiya."""
    size = 10 * mm
    lw = 1.5

    # Yuqori chap
    c.setStrokeColor(GOLD)
    c.setLineWidth(lw)
    c.line(x + 4 * mm, y + ch - 4 * mm, x + 4 * mm + size, y + ch - 4 * mm)
    c.line(x + 4 * mm, y + ch - 4 * mm, x + 4 * mm, y + ch - 4 * mm - size)

    # Yuqori o'ng
    c.line(x + cw - 4 * mm, y + ch - 4 * mm, x + cw - 4 * mm - size, y + ch - 4 * mm)
    c.line(x + cw - 4 * mm, y + ch - 4 * mm, x + cw - 4 * mm, y + ch - 4 * mm - size)

    # Pastki chap
    c.line(x + 4 * mm, y + 4 * mm, x + 4 * mm + size, y + 4 * mm)
    c.line(x + 4 * mm, y + 4 * mm, x + 4 * mm, y + 4 * mm + size)

    # Pastki o'ng
    c.line(x + cw - 4 * mm, y + 4 * mm, x + cw - 4 * mm - size, y + 4 * mm)
    c.line(x + cw - 4 * mm, y + 4 * mm, x + cw - 4 * mm, y + 4 * mm + size)


def generate_certificate(
    full_name: str,
    course_title: str,
    certificate_number: str,
    issued_at: datetime,
    output_path: str,
) -> None:
    """
    A4 landscape PDF sertifikat yaratish.

    Args:
        full_name: Foydalanuvchi toʻliq ismi
        course_title: Kurs nomi
        certificate_number: INKTALIM-YYYY-XXXXX
        issued_at: Berilgan sana
        output_path: PDF saqlash yoʻli
    """
    # Papkani yaratish (mavjud boʻlmasa)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    page_w, page_h = landscape(A4)
    c = rl_canvas.Canvas(output_path, pagesize=landscape(A4))

    # Matnlarni transliteratsiya qilish
    name_text   = _transliterate(full_name)
    course_text = _transliterate(course_title)
    course_text = _truncate(course_text, 60)

    # ─── Fon ────────────────────────────────────────────────────────────────
    _draw_background(c, page_w, page_h)

    # ─── Markaziy karta ─────────────────────────────────────────────────────
    card_w = page_w * 0.82
    card_h = page_h * 0.80
    card_x = (page_w - card_w) / 2
    card_y = (page_h - card_h) / 2

    # Karta soyasi (offset bilan)
    c.setFillColor(colors.HexColor("#000000"))
    c.setFillColorRGB(0, 0, 0, alpha=0.4)
    c.roundRect(card_x + 3, card_y - 3, card_w, card_h, radius=8 * mm, stroke=0, fill=1)

    # Karta foni
    c.setFillColor(CARD_BG)
    c.roundRect(card_x, card_y, card_w, card_h, radius=8 * mm, stroke=0, fill=1)

    # Karta chegarasi (teal)
    c.setStrokeColor(PRIMARY)
    c.setLineWidth(1.5)
    c.roundRect(card_x, card_y, card_w, card_h, radius=8 * mm, stroke=1, fill=0)

    # Ichki oltin border (dekorativ)
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.5)
    c.roundRect(
        card_x + 5 * mm, card_y + 5 * mm,
        card_w - 10 * mm, card_h - 10 * mm,
        radius=6 * mm, stroke=1, fill=0,
    )

    # Burchak dekoratsiyalari
    _draw_corner_decorations(c, card_x + 5 * mm, card_y + 5 * mm, card_w - 10 * mm, card_h - 10 * mm)

    # ─── Logo doirasi ────────────────────────────────────────────────────────
    logo_cx = page_w / 2
    logo_cy = card_y + card_h - 28 * mm
    logo_r  = 13 * mm

    c.setFillColor(PRIMARY)
    c.circle(logo_cx, logo_cy, logo_r, stroke=0, fill=1)

    c.setFillColor(CARD_BG)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(logo_cx, logo_cy - 5, "EDU")

    # ─── Platform nomi ────────────────────────────────────────────────────────
    c.setFont("Helvetica-Bold", 22)
    c.setFillColor(TEXT_WHITE)
    c.drawCentredString(page_w / 2, logo_cy - 22 * mm, "InkTalim.Uz")

    c.setFont("Helvetica", 9)
    c.setFillColor(TEXT_MUTED)
    c.drawCentredString(page_w / 2, logo_cy - 27 * mm, "Online Ta'lim Platformasi")

    # ─── SERTIFIKAT sarlavha ─────────────────────────────────────────────────
    title_y = logo_cy - 40 * mm
    c.setFont("Helvetica-Bold", 36)
    c.setFillColor(GOLD)
    c.drawCentredString(page_w / 2, title_y, "SERTIFIKAT")

    # Sarlavha ostidagi chiziq
    line_w = 80 * mm
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.line(page_w / 2 - line_w / 2, title_y - 4 * mm, page_w / 2 + line_w / 2, title_y - 4 * mm)

    # ─── "Ushbu sertifikat" ───────────────────────────────────────────────────
    text_y = title_y - 14 * mm
    c.setFont("Helvetica", 11)
    c.setFillColor(TEXT_MUTED)
    c.drawCentredString(page_w / 2, text_y, "Ushbu sertifikat")

    # ─── Foydalanuvchi ismi ───────────────────────────────────────────────────
    name_y = text_y - 11 * mm
    c.setFont("Helvetica-Bold", 26)
    c.setFillColor(PRIMARY)
    c.drawCentredString(page_w / 2, name_y, name_text)

    # ─── "ga" ─────────────────────────────────────────────────────────────────
    ga_y = name_y - 10 * mm
    c.setFont("Helvetica", 11)
    c.setFillColor(TEXT_MUTED)
    c.drawCentredString(page_w / 2, ga_y, "ga")

    # ─── Kurs nomi ────────────────────────────────────────────────────────────
    course_y = ga_y - 10 * mm
    c.setFont("Helvetica-BoldOblique", 16)
    c.setFillColor(LIGHT_GOLD)
    c.drawCentredString(page_w / 2, course_y, f'"{course_text}"')

    # ─── Tavsif matni ─────────────────────────────────────────────────────────
    desc_y = course_y - 10 * mm
    c.setFont("Helvetica", 10)
    c.setFillColor(TEXT_MUTED)
    c.drawCentredString(
        page_w / 2, desc_y,
        "kursini muvaffaqiyatli tugatganligi uchun berildi",
    )

    # ─── Ajratuvchi chiziq ────────────────────────────────────────────────────
    div_y = card_y + 20 * mm
    c.setStrokeColor(CARD_BORDER)
    c.setLineWidth(0.8)
    c.line(card_x + 20 * mm, div_y + 4 * mm, card_x + card_w - 20 * mm, div_y + 4 * mm)

    # ─── Pastki qism: 3 ustun ─────────────────────────────────────────────────
    bottom_y = div_y - 2 * mm

    # Chap: sertifikat raqami
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(TEXT_MUTED)
    c.drawString(card_x + 20 * mm, bottom_y, "SERTIFIKAT RAQAMI")
    c.setFont("Courier-Bold", 10)
    c.setFillColor(GOLD)
    c.drawString(card_x + 20 * mm, bottom_y - 5 * mm, certificate_number)

    # Markaziy: sana
    date_str = issued_at.strftime("%d.%m.%Y")
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(TEXT_MUTED)
    c.drawCentredString(page_w / 2, bottom_y, "BERILGAN SANA")
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(TEXT_WHITE)
    c.drawCentredString(page_w / 2, bottom_y - 5 * mm, date_str)

    # O'ng: imzo
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(TEXT_MUTED)
    right_x = card_x + card_w - 20 * mm
    c.drawRightString(right_x, bottom_y, "IMZO")
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColor(PRIMARY)
    c.drawRightString(right_x, bottom_y - 5 * mm, "InkTalim.Uz Ta'lim Platformasi")

    # ─── Saqlash ─────────────────────────────────────────────────────────────
    c.save()
