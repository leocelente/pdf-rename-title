# Batch PDF Rename to Title
A python script to rename all pdfs in directory to a sanitized version of their Content-Title metadata

## Dependencies
Just PyPDF
```shell
pip install pypdf
```
or 
```shell
pip install -r requirements.txt
```

## Usage

```
usage: python3 main.py [-h] [--version] [--dry-run] <DIR>

Batch renames PDF files to their Titles (Content-Title)

positional arguments:
  <DIR>       Directory with PDF files

options:
  -h, --help  show this help message and exit
  --version   show program's version number and exit
  --dry-run   Do not rename actual files 
```

## Notes