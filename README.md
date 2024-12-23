# Python CV template with PyLatex

## Motivation

I wanted to maintain a single source of `.json` database for updating my CV and website. The best option is to render my CV via Python

Features

- Use .json to record manuscripts, presentations, publications
- Google Scholar
- Gather GitHub 
- Easily extensable

## Installation

```bash
pip install -r requirements.txt
```

Another way is to download

```bash
pip install scholarly PyLaTeX
```

If the above does not work, install in a new conda environment:

```bash
conda create -n cv_env python=3.13
pip install -r requirements.txt
```

## How to get started

Clone and enter the direcotry:

```bash
# Clone the repository
git clone https://github.com/bobleesj/python-cv-template

# Go to the direcotry
cd python-cv-template
```

Run 

```bash
python cv.py
```

## How to customize

You can easily customize information under `cv.py`. Also all of the data are stored in the `data` folder.
