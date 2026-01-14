# VK Shortener

Educational project.  
A console application for shortening links using the VK API and getting click statistics for shortened links.

The program can:
- shorten regular URLs;
- detect whether a link is already shortened (`vk.cc`);
- display the total number of clicks for a shortened link.

---

## Installation

Clone the repository or download it as an archive:

```bash
git clone https://github.com/Alex149505/vk_shortener.git
cd vk_shortener
```
Python3 should already be installed. Use pip (or pip3, if there is a conflict with Python2) to install dependencies:
```bash
pip install -r requirements.txt
```
---

## invironment variables

Create a `.env` file in the project root and add:

```env
VK_ACCESS_TOKEN=your_access_token
```
How to get a token:
+ https://vk.com/dev/access_token

---

## Usage

Run the program:
```bash
python main.py
```
Enter a link when prompted.

### Example: shortening a link:

```text
python main.py https://google.com
Сокращённая ссылка: https://vk.cc/xxxxxx
```

### Example: getting click statistics:

```text
python main.py https://vk.cc/xxxxxx
Всего переходов: 42
```

---

## Project Goals

This code was written for educational purposes as part of an online course for web developers at [dvmn.org](https://dvmn.org/)