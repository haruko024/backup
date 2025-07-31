import warnings
import sys
warnings.filterwarnings("ignore", category=UserWarning)
if not sys.warnoptions:
    warnings.simplefilter("ignore", SyntaxWarning)

from docxtpl import DocxTemplate
from datetime import datetime
import os
import pyfiglet
import subprocess
from docx import Document
from docxcompose.composer import Composer
from colorama import init, Fore, Style

init(autoreset=True)

os.makedirs("output/docx", exist_ok=True)
os.makedirs("output/pdfs", exist_ok=True)
os.makedirs("output/merged", exist_ok=True)

file = open("names.txt", "r", encoding="utf-8")
names = [line.strip() for line in file if line.strip()]
date = datetime.now().strftime("%B %d, %Y")

def docxonly():
    for index, name in enumerate(names):
        doc = DocxTemplate("NAYOtemp.docx")
        context = {"name": name, "date": date}
        filename = f"{name}_output.docx" if index == 0 else f"{name}_output{index}.docx"
        doc.render(context)
        doc.save(f"output/docx/{filename}")
        print(Fore.CYAN + f"⭕ Generating {filename}")
    print(Fore.GREEN + f"✅ DOCX files saved at: {os.path.abspath('output/docx')}")

def generatepdf():
    print(Fore.LIGHTYELLOW_EX + "🔄 Converting all DOCX files to PDF...")
    docx_folder = os.path.abspath("output/docx")
    pdf_folder = os.path.abspath("output/pdfs")
    docx_files = [f for f in os.listdir(docx_folder) if f.endswith(".docx")]

    if not docx_files:
        print(Fore.RED + "⚠️ No DOCX files found to convert.")
        return

    subprocess.run([
        "libreoffice",
        "--headless",
        "--convert-to", "pdf",
        "--outdir", pdf_folder
    ] + [os.path.join(docx_folder, f) for f in docx_files],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    for f in docx_files:
        print(Fore.CYAN + f"📄 Converted {f} to PDF")
    print(Fore.GREEN + f"✅ PDF files saved at: {pdf_folder}")

def docx_and_pdf():
    docxonly()
    generatepdf()

def convertdocx2pdf():
    generatepdf()

def merge_docx():
    docx_folder = "output/docx"
    docx_files = sorted([
        os.path.join(docx_folder, f)
        for f in os.listdir(docx_folder)
        if f.endswith(".docx") and f != "merged.docx"
    ])

    if not docx_files:
        print(Fore.RED + "⚠️ No DOCX files found to merge.")
        return

    master = Document(docx_files[0])
    composer = Composer(master)

    for file in docx_files[1:]:
        sub_doc = Document(file)
        composer.append(sub_doc)

    merged_path = os.path.join("output/merged", "merged.docx")
    composer.save(merged_path)
    print(Fore.GREEN + f"📎 Merged DOCX saved at: {os.path.abspath(merged_path)}")

def merge_docx_pdf():
    merge_docx()
    print(Fore.LIGHTYELLOW_EX + "🔄 Converting merged DOCX to PDF...")
    merged_docx_path = os.path.abspath("output/merged/merged.docx")
    merged_pdf_output = os.path.abspath("output/merged")

    subprocess.run([
        "libreoffice",
        "--headless",
        "--convert-to", "pdf",
        "--outdir", merged_pdf_output,
        merged_docx_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(Fore.GREEN + f"✅ Merged PDF saved at: {merged_pdf_output}")

def main():
    banner = pyfiglet.figlet_format("DOCUMENT AUTOMATION")
    print(Fore.MAGENTA + banner + Fore.RED + "\t\t❤️  By Paul Mendoza ❤️")
    while True:
        print(Fore.WHITE + """
OPTIONS:
    [1] Generate Docx Only
    [2] Convert All Docx to PDF
    [3] Generate Docx + PDF
    [4] Merge All Docx and Convert to PDF
    [5] Merge All Docx Only
    [0] Complete Automate
    [q] Exit""")
        choice = input(Fore.YELLOW + "Enter your choice: ").strip().lower()
        if choice == "1":
            docxonly()
        elif choice == "2":
            convertdocx2pdf()
        elif choice == "3":
            docx_and_pdf()
        elif choice == "4":
            merge_docx_pdf()
        elif choice == "5":
            merge_docx()
        elif choice == "0":
            docx_and_pdf()
            merge_docx_pdf()
            print(Fore.GREEN + f"📂 Open your DOCX folder: {os.path.abspath('output/docx')}")
            print(Fore.GREEN + f"📂 Open your PDF folder: {os.path.abspath('output/pdfs')}")
            print(Fore.GREEN + f"📂 Open your Merged folder: {os.path.abspath('output/merged')}")
            print(Fore.GREEN + "✅ Captured Complete!!")
            break
        elif choice == "q":
            print(Fore.CYAN + "👋 Exiting. Goodbye!")
            break
        else:
            print(Fore.RED + "❌ Invalid input. Try again.")

if __name__ == "__main__":
    main()
