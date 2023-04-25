from PIL import Image, ImageDraw, ImageFont
import textwrap

def draw_text(text, font_name, font_padding=5, width=800, height=800,
               bg_colour=(255,255,255), font_size=180, font_colour=(0,0,0), wrap_after_chars=4):
    paragraph = textwrap.wrap(text, width=wrap_after_chars)
    out = Image.new("RGB", (width, height), bg_colour)

    font = ImageFont.truetype(font_name, font_size)
    ascent, descent = font.getmetrics()
    (_, _), (_, offset_y) = font.font.getsize(text)
    font_height = ascent - offset_y

    draw = ImageDraw.Draw(out)

    font_padding = 5
    curr_height = (height / 2) - (len(paragraph) * font_height) + font_padding
    for line in paragraph:
        w, h = draw.textsize(line, font=font)
        draw.text(((width - w) / 2, curr_height), line, font=font, fill=font_colour)
        curr_height += h + font_padding

    return out
