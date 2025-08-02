import warnings
import sys
warnings.filterwarnings("ignore", category=UserWarning)
if not sys.warnoptions:
    warnings.simplefilter("ignore", SyntaxWarning)
from getpass import getpass
import speech_recognition as sr
import pyttsx3
from docxtpl import DocxTemplate
from datetime import datetime
import os
import pyfiglet
import subprocess
from docx import Document
from docxcompose.composer import Composer
from colorama import init, Fore

init(autoreset=True)
engine = pyttsx3.init()

def speak(text):
    print(Fore.LIGHTYELLOW_EX + f"[PaulAI] {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print(Fore.YELLOW + "[PaulAI] Listening... (Speak now)")
        audio = recognizer.listen(source, phrase_time_limit=10)
    try:
        command = recognizer.recognize_google(audio)
        print(Fore.BLUE + f"[You] {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("I didn't catch that. Please speak clearly.")
        return listen()
    except sr.RequestError:
        speak("Speech service error. Please check your connection.")
        return None



file = open("names.txt", "r", encoding="utf-8")
names = [line.strip() for line in file if line.strip()]
date = datetime.now().strftime("%B %d, %Y")

file2 = open("config.txt", "r", encoding="utf-8").read().split('@')
temp = file2[0].split("=")[1].strip()
cont = file2[1].split("=")[1].strip()



def docxonly():
    speak(f"{len(names)} name list found!. Please wait for a while")
    speak("Generating docx.")
    for index, name in enumerate(names):
        doc = DocxTemplate(f"templates/{temp}")
        context = eval("{" + cont + "}")
        filename = f"{name}_output.docx" if index == 0 else f"{name}_output{index}.docx"
        doc.render(context)
        doc.save(f"output/docx/{filename}")
        print(Fore.CYAN + f"⭕ Generated {filename}")
    speak("DOCX files created.")

def generatepdf():
    speak("Converting DOCX files to PDF.")
    docx_folder = os.path.abspath("output/docx")
    pdf_folder = os.path.abspath("output/pdfs")
    docx_files = [f for f in os.listdir(docx_folder) if f.endswith(".docx")]

    if not docx_files:
        speak("No DOCX files found.")
        return

    subprocess.run([
        "libreoffice", "--headless", "--convert-to", "pdf", "--outdir", pdf_folder
    ] + [os.path.join(docx_folder, f) for f in docx_files],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    speak("PDF conversion completed.")

def docx_and_pdf():
    speak("Generating Docx and PDF.")
    docxonly()
    generatepdf()

def merge_docx():
    speak("Merging Docx.")
    docx_folder = "output/docx"
    docx_files = sorted([
        os.path.join(docx_folder, f)
        for f in os.listdir(docx_folder)
        if f.endswith(".docx") and f != "merged.docx"
    ])

    if not docx_files:
        speak("No DOCX files found to merge.")
        return

    master = Document(docx_files[0])
    composer = Composer(master)
    for file in docx_files[1:]:
        composer.append(Document(file))

    merged_path = os.path.join("output/merged", "merged.docx")
    composer.save(merged_path)
    print(Fore.CYAN + f"⭕ Generated merged.docx")
    speak("DOCX files merged successfully.")
    speak("Converting merged files..")

def merge_docx_pdf():
    speak("Merging docx and pdf.")
    merge_docx()
    merged_docx_path = os.path.abspath("output/merged/merged.docx")
    merged_pdf_output = os.path.abspath("output/merged")
    subprocess.run([
        "libreoffice", "--headless", "--convert-to", "pdf", "--outdir", merged_pdf_output,
        merged_docx_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(Fore.CYAN + f"⭕ Generated merged.pdf")
    speak("Merged DOCX converted to PDF.")

def something():
    speak("Say Something?")
    command = listen()
    if command == "kupal":
        speak("kupal!. Wait for a while..")
        docx_and_pdf()
        merge_docx_pdf()
        speak("All tasks completed successfully.")
        speak("Thanks for run this code. Please Subscribe my Github Account and Visit my Website")
        print("Github : https://github.com/paulmendoza24")
        print("Website : https://paulmendoza24.github.io/index/")
        speak("Remember!: With great power! comes great responsibility.")
    else:
        speak("kupal!. Wait for a while..")
        docx_and_pdf()
        merge_docx_pdf()
        speak("All tasks completed successfully.")
        speak("Thanks for run this code. Please Subscribe my Github Account and Visit my Website")
        print("Github : https://github.com/paulmendoza24")
        print("Website : https://paulmendoza24.github.io/index/")
        speak("Remember!: With great power! comes great responsibility.")
        

def ai_menu():
    banner = pyfiglet.figlet_format("AI DOC MAKER")
    print(Fore.CYAN + banner + Fore.LIGHTYELLOW_EX +"\t\t\t BY PAUL MENDOZA")
    speak("Hello! I am your document assistant. What would you like me to do sir Paul?. ")
    while True:
        speak("You can say: generate docx, convert to PDF, generate both, merge files, merge docx, full automation, or exit.")
        command = listen()
        if command is None:
            continue
        elif "generate docx" in command:
            docxonly()
        elif "convert to pdf" in command:
            generatepdf()
        elif "generate both" in command:
            docx_and_pdf()
        elif "merge files" in command or "merge" in command:
            merge_docx_pdf()
        elif "merge docx" in command:
            merge_docx()
        elif "full automation" in command or "complete" in command:
            something()
            break
        elif "exit" in command or "quit" in command:
            speak("Goodbye!")
            break
        else:
            speak("Sorry, I didn't catch that. Please try again.")

if __name__ == "__main__":
    input_pass1 = "falcon"
    input_pass2 = "wizard"
    input_pass3 = "paul24"

    max_attempts = 3
    attempts = 0

    while attempts < max_attempts:
        print(Fore.YELLOW + f"\nAttempt {attempts + 1} of {max_attempts}")
        pass1 = getpass("Enter 1st Password: ")
        pass2 = getpass("Enter 2nd Password: ")
        pass3 = getpass("Enter 3rd Password: ")

        if pass1 == input_pass1 and pass2 == input_pass2 and pass3 == input_pass3:
            print(Fore.GREEN + "[ACCESS GRANTED]")
            os.makedirs("output/docx", exist_ok=True)
            os.makedirs("output/pdfs", exist_ok=True)
            os.makedirs("output/merged", exist_ok=True)
            ai_menu()
            break
        else:
            print(Fore.RED + "[ACCESS DENIED] Incorrect password(s). Try again.")
            attempts += 1

    if attempts == max_attempts:
        print(Fore.RED + "\n[LOCKED OUT] Too many incorrect attempts. Exiting.")
