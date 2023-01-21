import argparse
import os
from concurrent.futures import ThreadPoolExecutor
from mimetypes import guess_type

import pypdf as pdf


def sanitize(name: str) -> str:
    RULES:dict[str, str] = {
        ' ': '.',
        '.':'_',
        '\u2014': '_',
        '(': '_',
        ')': '_',
        '/':'.',
        ':':'_'
    }
    chars = list(name)
    for i, c in enumerate(chars):
        if c in RULES.keys():
            chars[i] = RULES[c]
        elif not c.isalnum():
            chars[i] = ''
    return "".join(chars)

def content_title(pdf_filename: str) -> str:
    reader = pdf.PdfReader(pdf_filename)
    title = reader.metadata.title
    if title is None:
        return filename.split('/')[-1].removesuffix('.pdf')
    return title.capitalize()
        
def is_pdf(filename: str) -> bool:
    mime:str = guess_type(filename)[0]
    return mime is not None and mime.endswith('pdf')
    
def new_name(filename: str) -> str:
    title = content_title(filename)
    return sanitize(title) + '.pdf'

rename_function = os.rename
def rename_pdf(filename: str) -> None:
    new = new_name(filename)
    path = os.path.dirname(filename)
    new_path = os.path.join(path, new)
    rename_function(filename, new_path)


if __name__ == '__main__':    
    parser = argparse.ArgumentParser(prog="python3 main.py", description="Batch renames PDF files to their Titles (Content-Title)")
    parser.add_argument('directory', metavar='<DIR>', default='.', type=str, help="Directory with PDF files")
    parser.add_argument('--version', action='version', version='%(prog)s 0.1')
    parser.add_argument('--dry-run', action='store_true', help="Do not rename actual files")
    
    args = parser.parse_args()
    if not os.path.exists(args.directory):
        print(f"No such path: {args.directory}")
        exit(1)

    if args.dry_run:
        rename_function = lambda src, dst: print(src + '->' + dst)
    
    with ThreadPoolExecutor() as executor:
        for root, dirs, files in os.walk(args.directory):
            for file in files:
                print(file)
                if is_pdf(file):
                    filename = os.path.join(root, file)       
                    executor.submit(rename_pdf, filename)
        executor.shutdown(wait=True) 

  