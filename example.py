import os, random
from ImageQuote import ImageQuote

bg_files = []

for root, subdirs, files in os.walk("./backgrounds"):
    for file in files:
        bg_files.append(os.path.join(root, file))

font_files = []

for root, subdirs, files in os.walk("./fonts/hindi"):
    for file in files:
        font_files.append(os.path.join(root, file))

random_background = os.path.abspath(random.choice(bg_files))
random_font = os.path.abspath(random.choice(font_files))

image = ImageQuote()
# image.set_top_text("आज का सुविचार")
image.set_quote("स्वार्थ संसार का एक ऐसा कुआं है जिसमें गिरकर निकल पाना बड़ा कठिन होता हैं।")
image.set_quote_by("भगवान श्री कृष्ण")
image.set_font_family(random_font)
image.set_background_image(random_background)
image.set_output_file_size(35000)

# generate image in current directory
image.generate_image("./output")