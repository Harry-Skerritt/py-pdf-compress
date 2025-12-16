# PDF-CLI-Compressor
![Made with Python](https://img.shields.io/badge/Python-a?logo=python&label=Made%20With&color=blue&style=for-the-badge)
![GitHub License](https://img.shields.io/github/license/Harry-Skerritt/PDF-CLI-Compressor?style=for-the-badge)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/Harry-Skerritt/PDF-CLI-Compressor?style=for-the-badge)
![Runs on Mac](https://img.shields.io/badge/Mac-OS?logo=apple&color=%23555555&style=for-the-badge)
![Runs on Linux](https://img.shields.io/badge/Linux-OS?logo=linux&color=orange&style=for-the-badge)
![Runs on Windows](https://img.shields.io/badge/Windows-OS?logo=windows&color=blue&style=for-the-badge)

---

* This is a quick and dirty CLI PDF compressor written in python.

* Not the neatest or most efficient code, but was written in 30 minutes as I needed to compress some PDFs without uploading them to the internet.

* Uses Ghostscript to operate

## How to Install
_**Requires Python3 being installed**_

### To install the Ghostscript dependency:
* On MacOS run `brew install ghostscript`
* On Windows run `choco install ghostscript`
* On Linux run `sudo apt install ghostscript`

### To 'Install' the script:
* Put the compress.py file into the directory of pdfs and run `python3 compress.py` (This will run at default compression level of 2)


## Quality Flag
You can use the `--quality` flag to specify the quality of your compressed PDF.
> Example Useage `python3 compress.py --quality 2`

| Quality Tag    | Quality / Size | Ghostscript Preset |
| -------------- | ----------------- | --------------- |
| `--quality 1`  | lowest / smallest | /screen         |
| `--quality 2`  | good / small      | /ebook          |
| `--quality 3`  | high / big        | /printer        |
| `--quality 4`  | best / largest    | /prepress       |



## Possible Additions
* Neaten up of the code
* More efficient code
* Make it easier to use
