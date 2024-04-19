# Kurdish Poems Word-Cloud Project

This project generates word-cloud images for Kurdish poems. It includes 117 poets from the allekok repository and compares the word frequency results for all poems with those of the famous Kurdish poet Mamosta Hemin.

## Installation

To use this project, follow these steps:

Install the required packages:

```bash

  sudo apt update

  sudo apt -y install unzip git cmake python3-pip python3.11-venv libfreetype6-dev libharfbuzz-dev libfribidi-dev meson gtk-doc-tools libcairo2-dev libfontconfig-dev libice-dev libpixman-1-dev libsm-dev libx11-dev libxcb-render0-dev libxcb-shm0-dev libxext-dev libxrender-dev xtrans-dev libjpeg-dev zlib1g-dev libpng-dev libtiff5-dev liblcms2-dev libwebp-dev libxcb1-dev


  mkdir ~/tmp
  cd tmp


  git clone https://github.com/HOST-Oman/libraqm.git
  git clone https://github.com/ninja-build/ninja.git


  cd ninja
  ./configure.py --bootstrap
  cmake -Bbuild-cmake
  cmake --build build-cmake


  cd ~/tmp/libraqm
  meson build
  ninja -C build
  sudo ninja -C build install


  python3 -m venv ~/venv/ckb
  source ~/venv/ckb/bin/activate

  pip install wheel setuptools pip --upgrade
  pip install -U pillow ptpython matplotlib mplcairo seaborn wordcloud pyfribidi PyICU regex unicodedataplus rich

  cd ~
  rm -rf ~/tmp

  # Guide Source: https://gist.github.com/andjc/ba84da258e7dbb5c2e4ee5b7adf2e1b2

```

Source of the used font _vazirmatn_ in this project:

```bash
  https://fonts.google.com/specimen/Vazirmatn
  # OR
  https://github.com/rastikerdar/vazirmatn
```

## Usage

To generate word-cloud images, run the following commands:

```python
python read_poems.py && python get_and_generate_wordclouds.py
```

This will clone the allekok-poems from its repository, create word-frequency files in json format, and generate word-cloud images for each poet with their names as directories for the photos and one for each poem separately.

## Result

```python
117 poets
341 directories
10,658 poem files
261,788 lines (after cleaning)
1,849,262 words
10,151,576 characters
```

The top five words used throughout all poems are:

```json
[
  {
    "entry": "و",
    "frequency": 94940
  },
  {
    "entry": "لە",
    "frequency": 47199
  },
  {
    "entry": "بە",
    "frequency": 37435
  },
  {
    "entry": "بۆ",
    "frequency": 20258
  },
  {
    "entry": "کە",
    "frequency": 18956
  }
]
```

To provide an example of the project's functionality, I conducted a comparison between all the poems and only those written by **Mamosta Hemin**. The first 8 lines of the results are displayed in the following screenshot:

![comparing all poems and mamosta hemin's poems](./images/Screenshot%20from%202023-03-14%2021-56-21.png)

### All Poems Word-Cloud

- taking into consideration one-character words

![all_poems_01](./images/all_poems_01.png)

- without considering one to three character words

![all_poems_02](./images/all_poems_02.png)

### Mamosta Hemin's Poems Word-Cloud

- taking into consideration one-character words

![hemin_01](./images/hemin_01.png)

- without considering one to three character words

![hemin_02](./images/hemin_02.png)

Additionally, the project includes a JSON file with the word frequency results for all poems.

## Credit

This project uses the allekok repository, which includes 117 Kurdish poets. The word-cloud generation is based on the Python package wordcloud with helping other packges which support Kurdish characters perfectly such as:

- freetype-2.13.0
- graphite2-1.3.14
- harfbuzz
- libraqm
