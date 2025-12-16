import os
import sys
import subprocess
import argparse
import shutil
import tempfile
import threading
import time
import itertools


# Clears previous line
def clear_line():
    sys.stdout.write("\r\033[K")
    sys.stdout.flush()

# This handles the spinner and message UI
def spinner(message: str, stop_event: threading.Event):
    for char in itertools.cycle("-/|\\"):
        if stop_event.is_set():
            break
        sys.stdout.write(f"\r{char} {message}")
        sys.stdout.flush()
        time.sleep(0.1)

# This will get the current directory of the users terminal, 
# and check that it is not root, and can be written to
def getCurrentDir():
    cwd = os.path.abspath(os.getcwd())
    if os.name == "nt":  # Windows
        if cwd.rstrip("\\") in ["C:", "D:", "E:"]:
            sys.exit("Error: Cannot run py-pdf-compress in the root directory of a drive.")
    else:  # macOS / Linux
        if cwd == "/":
            sys.exit("Error: Cannot run py-pdf-compress in the root directory (/).")

    # Write perm check
    try:
        with tempfile.TemporaryFile(dir=cwd):
            pass
    except Exception:
        sys.exit(
            f"Error: Cannot write to directory:\n {cwd}\n"
            "Check permissions or choose a different folder."
        )

    return cwd
           
        
# This will check that ghostscript is installed,
# and return the correct command per version
def getGhostscriptCmd():
    gs_cmd = shutil.which("gs") or shutil.which("gswin64c")
    if not gs_cmd:
        sys.exit(
            "Error: Ghostscript not found.\n"
            "Install it:\n"
            "  macOS:   brew install ghostscript\n"
            "  Linux:   sudo apt install ghostscript\n"
            "  Windows: choco install ghostscript"
        )
    return gs_cmd


# THis will return any file in the cwd with .pdf
def getPDFsInDir(path):
    return [f for f in os.listdir(path) if f.lower().endswith(".pdf")]


# This will create the output directory
def createOutDir(path):
    out_dir = os.path.join(path, "out")
    os.makedirs(out_dir, exist_ok=True)
    return out_dir

# This will wipe the output directory if it exists 
def clearOutDir(out_dir):
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)


# This turns the quality int into a 
# recognisable command for ghostscript
def getQuality(in_quality):
    match in_quality:
        case 1:
            return "/screen"
        case 2:
            return "/ebook"
        case 3:
            return "/printer"
        case 4:
            return "/prepress"
        case _:
            raise ValueError("Invalid quality level")


# This is the actual compress function
def compress_pdfs(arg_in_qual, quiet=False):
    # Get working dir and perform ghostsciprt check
    working_dir = getCurrentDir()
    gs_cmd = getGhostscriptCmd()
    
    # Get the files from the cwd
    pdf_names = sorted(getPDFsInDir(working_dir))
    
    # If no files presents - exit
    if not pdf_names:
        sys.exit(f"Error: No PDF files found in {working_dir}")

    # Get toral files and output
    total = len(pdf_names)
    if not quiet:
        print(f"Found {total} PDF file(s).")

    # Create output dir
    out_dir = createOutDir(working_dir)
    clearOutDir(out_dir)

    # Convert quality
    quality = getQuality(arg_in_qual)

    # Compress each file
    for idx, pdf in enumerate(pdf_names, start=1):
        in_path = os.path.join(working_dir, pdf) # Set input path

        if not os.path.isfile(in_path):          # Check path has a file
            continue

        out_path = os.path.join(out_dir, pdf)    # Set output path

        # Setup the compressing message
        if not quiet and sys.stdout.isatty():
            msg = f"Compressing {idx}/{total}: {pdf}"
            stop_event = threading.Event()
            spin_thread = threading.Thread(
                target=spinner, args=(msg, stop_event)
            )
            spin_thread.start()
        else:
            stop_event = None

        # Run the ghostscript subprocess
        try:
            subprocess.run(
                [
                    gs_cmd,
                    "-q",
                    "-sDEVICE=pdfwrite",
                    f"-dPDFSETTINGS={quality}",
                    "-dNOPAUSE",
                    "-dBATCH",
                    f"-sOutputFile={out_path}",
                    in_path,
                ],
                check=True,
            )
            
        except subprocess.CalledProcessError:
            if stop_event:
                stop_event.set()
                spin_thread.join()
            sys.exit(f"\nError: Failed to compress {pdf}")

        if stop_event:
            stop_event.set()
            spin_thread.join()

        if not quiet:
            clear_line()
            print(f"Compressed {idx}/{total}: {pdf}")

    print(f"\nDone! Files saved to {out_dir}")