# Kurdish Poems Word-Cloud Project

This project generates word-cloud images for Kurdish poems. It includes 117 poets from the allekok repository and compares the word frequency results for all poems with those of the famous Kurdish poet Mamosta Hemin. 

## Installation

To use this project, follow these steps:

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Below packsges needed to be built for supporting Kurdish language characters perfectly by _matplotlib_ and _wordcloud_ libraries:

```bash
freetype-2.13.0
graphite2-1.3.14
harfbuzz
libraqm
```

Library/Package Installation:

```yaml

- name: freetype
  instructions:
    - Clone the freetype repository:
      - git clone https://gitlab.freedesktop.org/freetype/freetype.git
    - Standard build with `configure`:
      - Depends on the following packages:
        - automake (1.10.1)
        - libtool (2.2.4)
        - autoconf (2.62)
      - To resolve, run:
        - sudo apt install libtool autotools-dev automake
      - Run:
        - sh autogen.sh

- name: graphite2-1.3.14
  instructions:
    - For detailed installation instructions, refer to:
      - https://www.metricfire.com/blog/how-to-install-and-configure-graphite-on-ubuntu/#Installing-Graphite-on-Ubuntu-1604
    - Use Docker to run Graphite:
      - docker run -d --name graphite --restart=always -p 81:80 -p 2003-2004:2003-2004 -p 2023-2024:2003-2004 -p 8125:8125/udp -p 8126:8126 graphiteapp/graphite-statsd

- name: harfbuzz
  instructions:
    - For detailed build instructions, refer to:
      - https://github.com/harfbuzz/harfbuzz/blob/main/BUILD.md
    - Install the required packages:
      - sudo apt install meson pkg-config ragel gtk-doc-tools gcc g++ libfreetype6-dev libglib2.0-dev libcairo2-dev
    - Clone the harfbuzz repository:
      - git clone https://github.com/harfbuzz/harfbuzz
    - Build and test:
      - meson build
      - meson test -C build

- name: libraqm
  instructions:
    - Install the required packages:
      - sudo apt install libfreetype6-dev libharfbuzz-dev libfribidi-dev meson gtk-doc-tools
    - For fribidi, clone the repository:
      - git clone https://github.com/fribidi/fribidi
      - sh autogen.sh
    - Clone the libraqm repository:
      - git clone https://github.com/HOST-Oman/libraqm
    - Build and install:
      - meson build
      - ninja -C build
      - ninja -C build install


```

Source of the used font _vazirmatn_ in this project:

```bash
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
* freetype-2.13.0
* graphite2-1.3.14
* harfbuzz
* libraqm
