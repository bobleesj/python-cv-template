# Welcome to Python CV Template

## Motivation

You are probably here because... you are tired of managing your CV either using Overleaf or Word. Now, you want to

- you probably want to maintain single `.json` and render your CV automatically.
- you want to spend less time formatting CV.
- you want to dynamically retrieve information such as citations and GitHub stars

## What this code does

This is not a library. This is a Python script that renders a single PDF.

- Use `.json` to record manuscripts, presentations, and publications
- Retrieve citation information from Google Scholar
- Retrieve GitHub repositories info (# of stars)
- Easily customizable

## Installation

Install `scholarly` and `PyLaTeX`:

```bash
pip install scholarly PyLaTeX
```

If the above does not work, install create a new conda environment and install `scholarly` and `PyLaTeX`.

```bash
conda create -n cv_env python=3.13
conda activate cv_env
pip install scholarly PyLaTeX
```

## Getting started

Clone and enter the directory:

```bash
# Clone the repository
git clone https://github.com/bobleesj/python-cv-template

# Go to the directory
cd python-cv-template

# Render a pdf file
python cv.py
```

`Sangjoon_Lee_CV.pdf` is rendered generated.

## How to customize

`cv.py` is the source of truth. I have maintained all functions and syntax within here. For manuscripts, publicatoins, it parses .json data under the `data` folder.

## Are you interested in contributing?

Please clone and fork the repository. Once changes are committed from a branch, please run `pre-commit`:

```bash
# Install pre-commit for automatic linting
pip install pre-commit

# Run pre-commit to standard the code
pre-commit --run-all-files
```
