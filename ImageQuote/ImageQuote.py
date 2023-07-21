import os, random, math, io
from typing import Tuple
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

# default social media image size
WIDTH = 720
HEIGHT = 1084

WHITE = "rgb(255, 255, 255)"
GREY = "rgb(200, 200, 200)"

FONT_SIZES_LG = [120, 110, 95, 80, 65, 60, 55, 50, 45, 40, 35, 30, 25, 20, 15]
FONT_SIZES = [65, 60, 55, 50, 45, 40, 35, 30, 25, 20, 15]
FONT_SIZES_SM = [50, 45, 40, 35, 30, 25, 20, 15]

MIN_FILE_SIZE = 35000

MARGIN = 50
MARGIN_TOP = 50
MARGIN_BOTTOM = 50
LOGO_MARGIN = 25

FONT_QUOTE = "font-text"
FONT_QUOTED_BY = "font-quoted-by"
FONT_SIZE = "font-size"
FONT_QUOTED_BY_SIZE = "font-quoted-by-size"

OUTPUT_QUOTE = "quote"
OUTPUT_QUOTED_BY = "quoted-by"
OUTPUT_LINES = "lines"

LINE_HEIGHT_ADDITION = 24


def get_wh(p):
    return (p[2] - p[0], p[3] - p[1])


def text_wrap_and_font_size(output, font_style, max_width, max_height):
    """
    Wraps content into multiple lines based on provided max width and height
    Figures out appropriate font size based on provided max width and height

    :param output: dict to which the lines will be written to
    :param font_style: dict to which font size will be written to
    :param max_width: maximum width of the output image
    :param max_height: maximum height of the output image
    """
    for font_size in FONT_SIZES:
        output[OUTPUT_LINES] = []
        font = ImageFont.truetype(
            font_style[FONT_QUOTE], size=font_size, encoding="unic"
        )
        output[OUTPUT_QUOTE] = " ".join(output[OUTPUT_QUOTE].split())

        if get_wh(font.getbbox(output[OUTPUT_QUOTE]))[0] <= max_width:
            output[OUTPUT_LINES].append(output[OUTPUT_QUOTE])
        else:
            words = output[OUTPUT_QUOTE].split()
            line = ""
            for word in words:
                if get_wh(font.getbbox(line + " " + word))[0] <= max_width:
                    line += " " + word
                else:
                    output[OUTPUT_LINES].append(line)
                    line = word
            output[OUTPUT_LINES].append(line)

        line_height = get_wh(font.getbbox("lp"))[1] + LINE_HEIGHT_ADDITION
        quoted_by_font_size = font_size
        quoted_by_font = ImageFont.truetype(
            font_style[FONT_QUOTED_BY], size=quoted_by_font_size, encoding="unic"
        )

        while get_wh(quoted_by_font.getbbox(output[OUTPUT_QUOTED_BY]))[0] > (
            max_width // 2
        ):
            quoted_by_font_size -= 1
            quoted_by_font = ImageFont.truetype(
                font_style[FONT_QUOTED_BY], size=quoted_by_font_size, encoding="unic"
            )

        height_cal = line_height * len(output[OUTPUT_LINES])
        height_cal += get_wh(quoted_by_font.getbbox("lp"))[1]
        height_cal += LINE_HEIGHT_ADDITION * 2
        if height_cal < max_height:
            font_style[FONT_SIZE] = font_size
            font_style[FONT_QUOTED_BY_SIZE] = quoted_by_font_size
            return True

    return False


class ImageQuote:
    def __init__(self):
        self.quote = "Please update the quote"
        self.quote_color = WHITE
        self.quote_stroke_fill = "black"
        self.quote_by = "Add quote by"
        self.quote_by_color = GREY
        self.top_text = None
        self.font_family = None
        self.font_variant = "md"
        self.output_size = (WIDTH, HEIGHT)
        self.watermark_text = None
        self.background_color = None
        self.background_image = None
        self.ouput_quality = 100
        self.output_file_size = None

    def set_quote(self, quote: str):
        self.quote = quote
        return self

    def set_quote_color(self, quote_color: str):
        self.quote_color = quote_color
        return self

    def set_font_family(self, font_family: str):
        """
        :font_family: absolute path to the font file or folder
        """
        self.font_family = font_family
        return self

    def set_output_size(self, size: Tuple[int, int]):
        self.output_size = size
        return self

    def set_watermark_text(self, watermark_text: str):
        self.watermark_text = watermark_text
        return self

    def set_quote_by(self, quote_by: str):
        self.quote_by = quote_by
        return self

    def set_quote_color(self, quote_by_color: str):
        self.quote_by_color = quote_by_color
        return self

    def set_top_text(self, top_text: str):
        self.top_text = top_text
        return self

    def set_variant(self, variant: str):
        self.font_variant = variant
        return self

    def set_background_image_dir(self, background_image_dir: str):
        self.background_image_dir = background_image_dir
        return self

    def set_background_image(self, background_image: str):
        self.background_image = background_image
        return self

    def set_background_color(self, background_color: str):
        self.background_color = background_color
        return self

    def set_output_file_size(self, output_file_size: int):
        """
        Allows you to enforce a maximum file size for the output image
        :param output_file_size: Set the output file size in bytes
        """
        self.output_file_size = (
            output_file_size if output_file_size >= MIN_FILE_SIZE else None
        )
        return self

    def set_ouput_quality(self, ouput_quality: int):
        self.ouput_quality = ouput_quality
        return self

    def __draw_text(self, image, output, font_style):
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(
            font_style[FONT_QUOTE], size=font_style[FONT_SIZE], encoding="unic"
        )
        line_height = get_wh(font.getbbox("lp"))[1] + LINE_HEIGHT_ADDITION
        lines = output[OUTPUT_LINES]

        # calculate top space; from where we start to print the lines
        quote_height = font_style[FONT_SIZE] * len(lines)
        y = (HEIGHT - quote_height) // 2
        y -= font_style[FONT_QUOTED_BY_SIZE]
        y -= LINE_HEIGHT_ADDITION

        if self.top_text:
            font_label = ImageFont.truetype(
                font_style[FONT_QUOTE],
                size=math.ceil(font_style[FONT_SIZE] // 1.5),
                encoding="unic",
            )
            label_size = get_wh(font_label.getbbox(self.top_text))
            x = (WIDTH - label_size[0]) // 2
            draw.text(
                (x, y - math.ceil(label_size[1] * 1.6)),
                self.top_text,
                fill=GREY,
                font=font_label,
                stroke_width=1,
                stroke_fill="black",
            )

        for line in lines:
            x = (WIDTH - get_wh(font.getbbox(line))[0]) // 2
            draw.text(
                (x, y), line, fill=WHITE, font=font, stroke_width=5, stroke_fill="black"
            )
            y = y + line_height

        quoted_by = output[OUTPUT_QUOTED_BY]
        quoted_by_font = ImageFont.truetype(
            font_style[FONT_QUOTED_BY],
            size=font_style[FONT_QUOTED_BY_SIZE],
            encoding="unic",
        )

        # position the quoted_by in the far right, but within margin
        x = WIDTH - get_wh(quoted_by_font.getbbox(quoted_by))[0] - MARGIN
        draw.text((x, y + 15), quoted_by, fill=GREY, font=quoted_by_font)

        return image

    def generate_image(self, output_image: str = None):
        output_file_name = (
            f"{self.quote[:10].replace(' ', '_')}_{random.randint(1000, 9999)}.jpg"
        )

        if output_image and os.path.isdir(output_image):
            output_image = os.path.join(output_image, output_file_name)
        elif not output_image:
            output_image = os.path.join(os.path.curdir, output_file_name)

        if self.background_image and os.path.isfile(self.background_image):
            image = Image.open(self.background_image)
            image = image.resize(self.output_size)
        elif self.background_color:
            image = Image.new("RGB", self.output_size, self.background_color)
        else:
            image = Image.new("RGB", self.output_size, "white")

        if not self.font_family or not os.path.isfile(self.font_family):
            raise Exception("Error: Invalid font family/folder")

        # START GENERATING IMAGE
        output = {OUTPUT_QUOTE: self.quote, OUTPUT_QUOTED_BY: self.quote_by}

        font_style = {FONT_QUOTE: self.font_family, FONT_QUOTED_BY: self.font_family}

        [width, height] = self.output_size

        text_wrap_and_font_size(
            output,
            font_style,
            width - (2 * MARGIN),
            height - MARGIN_TOP - MARGIN_BOTTOM,
        )

        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(0.5)

        image = self.__draw_text(image, output, font_style)

        quality = self.ouput_quality

        if self.output_file_size:
            min_quality = 65  # image looks below this quality

            # bring image size below a 100kb
            while True:
                output_buffer = io.BytesIO()
                image.save(output_buffer, "JPEG", quality=quality)

                file_size = output_buffer.tell()

                if file_size <= self.output_file_size or quality <= min_quality:
                    output_buffer.close()
                    break
                else:
                    quality -= 5

        image.save(output_image, "JPEG", quality=quality)

        return True
