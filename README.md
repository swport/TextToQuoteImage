<h1 align="center">TextToQuoteImage</h1>
<p align="center"><b>Python library to convert text to a quote image</b></p>
<p align="center"><kbd><img src="https://i.imgur.com/n4sAqY7_d.webp?maxwidth=760&fidelity=grand" height=300px></kbd></p>

## Basic Usage
```python
from ImageQuote import ImageQuote

image = ImageQuote()
image.set_quote("स्वार्थ संसार का एक ऐसा कुआं है जिसमें गिरकर निकल पाना बड़ा कठिन होता हैं।")
image.set_quote_by("भगवान श्री कृष्ण")
image.set_font_family("/path/to/font/file.ttf")
image.set_background_image("/path/to/background_image/file.jpeg")

# generate image in current directory
image.generate_image("./output")
```
