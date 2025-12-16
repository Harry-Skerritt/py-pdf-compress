import argparse
from importlib.metadata import version, PackageNotFoundError
from .compress import compress_pdfs


def get_version():
    try:
        return version("py-pdf-compress")
    except PackageNotFoundError:
        return "unknown"

def main():
    parser = argparse.ArgumentParser(
        description="Compress PDFs in current directory"
    )

    parser.add_argument(
        "--quality",
        type=int,
        choices=[1, 2, 3, 4],
        default=2,
        help="Compression quality: 1=screen, 2=ebook (default), 3=printer, 4=prepress",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {get_version()}",
    )

    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Only print final result",
    )
    
    args = parser.parse_args()
    compress_pdfs(args.quality, quiet=args.quiet)
