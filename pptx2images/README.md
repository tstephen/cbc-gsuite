Convert presentation to images
==============================

This simple script converts presentations (.pptx or .odp) to images.
This can be useful if you don't know what proesentation software is available as everything can cope with simple image files.

Usage
-----

* The hard work is done by external programs, so make sure these are installed first:
  * `libreoffice` - the open source office suite
  * `pdftoppm` - part of the [poppler project](https://en.wikipedia.org/wiki/Poppler_%28software%29).
  * Python

* Run the script
  ```
  ./pptx2png.py /path/to/your/presentation.pptx
  ```

More information
----------------

* Conversion is to JPEGs. When presentations contain photography compression can be as much as 5 times better than PNG.

