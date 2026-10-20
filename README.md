# Steagnox

Hide files inside images. A Django web app for password-protected image steganography.

![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.1-092E20?logo=django&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-cv2-5C3EE8?logo=opencv&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

## About

Steagnox lets you embed a confidential file inside an image so it can be sent without drawing attention, then extract it again with a password. Data is written into the least significant bits of each pixel, so the image looks unchanged to the eye. The project was built for VOIS by Team 330 from the Army Institute of Technology.

## Features

- **Embed:** upload a cover image, a file to hide and a password; download the result as `encrypted_img.png`
- **Extract:** upload an embedded image and the password to recover the original file under its original name
- **LSB encoding:** each byte is split 3-3-2 across the red, green and blue channels of one pixel, so one pixel carries one byte
- **Password-protected header:** a 30-byte header (file size + file name) is XOR-encrypted with the password; a wrong password shows an error page
- **Capacity check:** embedding is skipped if the file plus header is larger than the image's pixel count
- Uploaded files are deleted from the server after each embed or extract

> Note: only the header is XOR-encrypted with the password. The hidden file's bytes are stored as-is in the pixels, so treat this as obfuscation rather than strong encryption.

## Tech Stack

- **Backend:** Python, Django 4.1
- **Image processing:** OpenCV (`opencv-python`), Pillow (for Django `ImageField`)
- **Frontend:** Django templates, HTML, CSS, JavaScript
- **Database:** SQLite (Django default)

## Project Structure

```
Steagnox/
├── manage.py
├── steagnox/          # Project settings and root URL config
├── Home_Page/         # Landing page (/)
├── Image_embed/       # Embedding logic, form and views (/embed_image)
├── Image_extract/     # Extraction logic, form and views (/extract_image)
├── templete/          # HTML templates (folder name as used in settings.py)
├── static/            # CSS, JS and icons
└── media/             # Upload/output folders: images/, Files/, output/
```

## Getting Started

### Prerequisites

- Python 3.10 (the committed bytecode was built with 3.10)
- pip

There is no `requirements.txt`, so the dependencies are installed by hand below.

### Setup

```sh
git clone https://github.com/AryanDeswal/Steagnox.git
cd Steagnox

python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install "django>=4.1,<4.2" pillow opencv-python

python manage.py migrate
python manage.py runserver
```

Then open http://127.0.0.1:8000/.

> The download views build file paths with Windows `\` separators, so downloading the embedded image or extracted file currently works on Windows only.

## Usage

| Route            | Purpose                                         |
| ---------------- | ----------------------------------------------- |
| `/`              | Home page                                       |
| `/embed_image`   | Upload a cover image, a file and a password     |
| `/download_enc`  | Download the generated `encrypted_img.png`      |
| `/extract_image` | Upload an embedded image and its password       |
| `/download`      | Download the extracted file                     |
| `/admin/`        | Django admin                                    |

Always keep the embedded image as PNG. Lossy formats such as JPEG destroy the hidden bits.

## Contributors

Built by [Aryan Deswal](https://github.com/AryanDeswal) and [Dheeraj Kumar](https://github.com/dheerajrao20).

<a href="https://github.com/AryanDeswal/Steagnox/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=AryanDeswal/Steagnox" alt="Contributors" />
</a>

## License

This project is licensed under the [MIT License](LICENSE).
