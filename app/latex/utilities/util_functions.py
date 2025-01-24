"""
Module of functions for backtracking
"""

from pathlib import Path
import subprocess
import os
import glob


def remove_output_files(directory, extensions=["*.tex"]):
    """Remove specified output files in a directory."""
    for ext in extensions:
        files = glob.glob(os.path.join(directory, ext))
        for file in files:
            try:
                os.remove(file)
                print(f"Removed: {file}")
            except Exception as e:
                print(f"Error removing {file}: {e}")


def merge_files(file1, file2, outputname):
    """Merge two PDF files into one."""
    subprocess.run(["pdfunite", file1, file2, outputname], check=True)


def convert_to_pdf(tex_path, outputdir):
    """Convert a LaTeX file to a PDF and clean auxiliary files."""
    tex_path = Path(tex_path).resolve()
    outputdir = Path(outputdir).resolve()
    # for testing
    # print(f"tex_path: {tex_path}")
    # print(f"outputdir: {outputdir}")
    try:
        # Generate the PDF
        subprocess.run(["latexmk", "-pdf", "-outdir=" + str(outputdir), str(tex_path)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # Clean auxiliary files after successful PDF generation
        subprocess.run(["latexmk", "-c", "-outdir=" + str(outputdir), str(tex_path)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # for hosted remove stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL for debugging any errors
        # subprocess.run(["latexmk", "-pdf", "-outdir=" + str(outputdir), str(tex_path)], check=True)
        # subprocess.run(["latexmk", "-c", "-outdir=" + str(outputdir), str(tex_path)], check=True)
        # Remove the .tex file manually

        # keep .tex during testing
        # if tex_path.exists():
        #     os.remove(tex_path)

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
