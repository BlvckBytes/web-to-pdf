# web-to-pdf

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Screenshot page wrappers on a website and combine them into a PDF-file for quick and easy document generation.

## Table of Contents
* [Installation](#installation)
* [Usage](#usage)
  * [Page Wrapping](#page-wrapping)
  * [Header and Footer](#header-and-footer)

## Installation

Just clone this repo, install the dependencies and run!

```bash
git clone https://github.com/BlvckBytes/web-to-pdf.git
cd web-to-pdf
pip3.9 install pillow
pip3.9 install selenium
pip3.9 install webdriver_manager
python3.9 web2pdf.py
```

## Usage

To get familiar with the required arguments, just run with `--help`:

```
usage: web2pdf.py [-h] -u URL [-o OUTPUT] [-n FILENAME] -p PAGECLASS [-w WAITCLASS]

optional arguments:
  -h, --help    show this help message and exit
  -u URL        Full URL of target website
  -o OUTPUT     Output directory path, defaults to Desktop
  -n FILENAME   Name of PDF file (excluding .pdf), defaults to "result"
  -p PAGECLASS  Class of page wrapping container (no leading .)
  -w WAITCLASS  Class of item to wait for until rendered (no leading .)
```

`-u`, `-o`, and `-n` should be pretty self explandatory. `-p` has to equal the class-name of your page-wrapping element, which will be the screenshot basis. `-w` can be the class-name of an element, which the tool waits for, until it appears within the document. This can be useful for async API-fetched elements that should be included in the document.

### Page Wrapping

The page wrapper just needs to be a div which has the correct proportions of an *ISO A4* paper, which happen to be `2480 pixels x 3508 pixels`. For my own use, I usually scale both the width and height down by a factor of 2. The tool automatically scales the images up to fit the full paper.

```html
<div class='page-wrapper'>
  <h1>This is on page one!</h1>
</div>
<div class='page-wrapper'>
  <h1>This is on page two!</h1>
</div>
```

```css
.page-wrapper {
  /* ISO A4 proportions */
  width: calc(2480px / 2);
  height: calc(3508px / 2);

  /* To keep edge-clearance for printing */
  padding: 4rem;

  /* Space out pages horizontally */
  /* Makes prototyping easier and avoids clipping */
  margin-bottom: 5rem;
  &:last-of-type {
    margin-bottom: 0;
  }
}
```

### Header and Footer

Oftentimes, you'd want to append a header and footer to each page, without too much extra work. I achieve it like this:

```html
<div class='page-wrapper page-wrapper--header page-wrapper--footer'>
  <h1>Has both header and footer</h1>
</div>
<div class='page-wrapper page-wrapper--footer'>
  <h1>Has only a footer</h1>
</div>
<div class='page-wrapper page-wrapper--header'>
  <h1>Has only a header</h1>
</div>
```

```css
.page-wrapper {
  /* ISO A4 proportions */
  width: calc(2480px / 2);
  height: calc(3508px / 2);

  /* To keep edge-clearance for printing */
  padding: 4rem;

  /* Space out pages horizontally */
  /* Makes prototyping easier and avoids clipping */
  margin-bottom: 5rem;
  &:last-of-type {
    margin-bottom: 0;
  }

  /* HEADER FOOTER BEGIN */
  &::before, &::after {
    content: '';
    position: absolute;
    left: 0;
    width: 100%;
    background-repeat: no-repeat;
    background-position: center center;
    background-size: cover;
  }

  &--header {
    padding-top: 18rem;
    &::before {
      top: 0;
      height: 18rem;
      background-image: url('../assets/header.png');
    }
  }

  &--footer {
    padding-bottom: 10rem;
    &::after {
      bottom: 0;
      height: 10rem;
      background-image: url('../assets/footer.png');
    }
  }
  /* HEADER FOOTER END */
}
```

This works a treat for image-based headers and footers, where the height rule basically defines the resulting width, you just have to play around and make those numbers fit your assets. If something more complex is desired, then just use javascript to iterate over the page elements and inject custom elements containing your data. That's the beauty of this tool, you have the full webstack at your disposal.