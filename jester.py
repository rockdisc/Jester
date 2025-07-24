import argparse
import json
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
import pytesseract
from pdf2image import convert_from_path
from PIL import Image, ImageFilter
import concurrent.futures

# Set Tesseract path (update if needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load environment variables from .env
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
OBSIDIAN_VAULT_PATH = os.getenv("OBSIDIAN_VAULT_PATH")

# Error handling in case the key isn't set
if not API_KEY:
    raise ValueError("API key not found. Make sure OPENROUTER_API_KEY is set in your .env file.")

# Constants
HISTORY_FILE = "history.json"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "qwen/qwen3-235b-a22b-07-25:free"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "User-Agent": "Jester/1.0"
}

def preprocess_image(image):
    img = image.convert('L')
    img = img.point(lambda x: 0 if x < 140 else 255, '1')
    img = img.filter(ImageFilter.SHARPEN)
    return img

# Helper function for parallel OCR processing
def process_page_for_ocr(page_data):
    """Processes a single image for OCR. To be used with a process pool."""
    i, image = page_data
    # Note: print statements in subprocesses might not appear in order.
    print(f"  - Starting OCR for page {i+1}...")
    processed_img = preprocess_image(image)
    text = pytesseract.image_to_string(processed_img, lang='eng', config='--oem 3 --psm 6')
    print(f"  - Finished OCR for page {i+1}.")
    return f"\n\n---\n\n## Page {i+1}\n{text}"

# Function to query the model
def ask_ai(prompt):
    messages = [{"role": "user", "content": prompt}]
    try:
        response = requests.post(API_URL, headers=HEADERS, json={
            "model": MODEL,
            "messages": messages
        })
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error contacting model: {e}"

# Load/save history
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(entry):
    history = load_history()
    history.append(entry)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

# Save response to Obsidian
def save_to_obsidian(filename, content):
    filepath = os.path.join(OBSIDIAN_VAULT_PATH, f"{filename}.md")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)


# ASCII intro
def show_intro():
    PURPLE = "\033[95m"
    RESET = "\033[0m"
    print(PURPLE + r"""          
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⠿⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣤⣤⣦⣤⡀⠠⣿⣿⣿⠟⢁⣴⣾⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀
⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣦⠈⠿⠃⣰⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄⠀⠀⠀⠀
⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⡗⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀
⠀⠀⠀⣿⡿⠛⠿⣿⣿⣿⣿⡟⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀
⠀⠀⢸⠏⠀⠀⠀⠈⢻⣿⣿⢁⣾⣿⣿⣿⣿⣿⣿⡿⠋⣉⡉⠻⣿⣿⡇⠀⠀⠀
⠀⠀⣈⠀⠀⠀⠀⠀⠈⣿⠃⣼⣿⣿⣿⣿⣿⣿⣿⠁⠘⢿⡇⠀⠈⢻⣿⠀⠀⠀
⠀⢾⣿⡇⠀⠀⠀⠀⠀⠏⢰⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⢀⣀⣀⠀⠀⢻⠀⠀⠀
⠀⠀⠉⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠸⠿⠿⠀⠀⠈⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⢿⣿⣿⣿⡿⣿⣿⣿⡄⠀⠀⠀⠀⠀⢠⣶⣆⠀
⠀⠀⠀⠀⠀⠀⠀⢀⠀⣿⡿⢁⠘⣿⣿⣿⠁⡈⢻⣿⠃⣰⡄⠀⠀⠀⠘⠛⠋⠀
⠀⠀⠀⠀⠀⠀⠀⣾⣆⠈⠁⣾⣦⠘⢿⠃⣰⣷⡄⠁⣰⣿⣿⣆⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣿⣿⣷⣤⣿⣿⣷⣤⣾⣿⣿⣷⣾⣿⠿⠿⠛⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠛⠛⠛⠋⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    """ + RESET)
    print("Jester here. How may I serve thee?\n")

# OCR Function
def convert_pdf_to_ai_markdown(pdf_path, output_folder):
    try:
        print("Converting PDF to images (this may take a moment)...")
        # Use multiple threads to speed up PDF to image conversion
        images = convert_from_path(pdf_path, dpi=300, thread_count=4)

        print("Extracting text from PDF pages (in parallel)...")

        # Use a process pool to run OCR in parallel
        with concurrent.futures.ProcessPoolExecutor() as executor:
            # The map function will apply process_page_for_ocr to each item in enumerate(images)
            # and return the results in order. We use list() to wait for all futures to complete.
            page_texts = list(executor.map(process_page_for_ocr, enumerate(images)))

        extracted_text = "".join(page_texts)

        # Create a prompt for the AI
        prompt = (
            "The following text was extracted from a PDF using OCR. "
            "It may contain errors or formatting issues. "
            "Please clean it up, correct any obvious OCR mistakes, and format it into clear, well-structured markdown. "
            "Preserve the original intent and structure (headings, lists, paragraphs) as best as you can.\n\n"
            "--- OCR TEXT START ---\n"
            f"{extracted_text.strip()}"
            "\n--- OCR TEXT END ---"
        )

        markdown_content = ask_ai(prompt)

        # Suggest a filename and ask the user
        default_base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        suggested_filename_base = f"{default_base_name}_AI_formatted"

        # Prompt the user for a filename, using the suggested name as a default
        user_filename_base = input(f"\nEnter the desired filename (without .md) [default: {suggested_filename_base}]: ").strip()
        if not user_filename_base:
            user_filename_base = suggested_filename_base

        # Construct the final path, ensuring it has the .md extension
        final_filename = f"{user_filename_base}.md"
        output_path = os.path.join(output_folder, final_filename)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_content.strip())

        print(f"\nSuccessfully converted and saved to: {output_path}")
    except Exception as e:
        print(f"Error processing PDF: {e}")

# Main
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--summarize", help="Summarize a topic or literature")
    parser.add_argument("-q", "--question", help="Quick answer to a question")
    parser.add_argument("-iq", "--quotes", help="Interesting quotes from a book")
    parser.add_argument("-hh", "--helpme", action="store_true", help="Show all commands")
    parser.add_argument("-nf", "--neofetch", action="store_true", help="Neofetch-style intro")
    parser.add_argument("-g", "--generate", help="Generate something as requested")
    parser.add_argument("-w", "--wordfor", help="Creative word lists for something")
    parser.add_argument("-dm", "--dnd", help="Answer a Dungeons and Dragons question")
    parser.add_argument("-cd", "--code", help="Help with code")
    parser.add_argument("-cv", "--convertnote", help="Convert a PDF to clean, AI-formatted markdown and save to Obsidian")
    parser.add_argument("-o", "--obsidian", nargs="?", const="last_output", help="Save the response to Obsidian")


    args = parser.parse_args()

    if args.neofetch:
        show_intro()
        return

    if args.helpme:
        print("""
Commands:
  -s  --summarize   Summarize literature or a concept
  -q  --question    Get a short answer + summary
  -iq --quotes      Get interesting quotes from a book
  -hh --helpme      Show this help menu
  -nf --neofetch    Show Jester ASCII intro
  -g  --generate    Create something (story, poem, etc.)
  -w  --wordfor     Suggest a word or phrase
  -cd --code        Help with code-related questions
  -dm --dnd         Answer a Dungeons and Dragons question
  -cv --convertnote Convert a PDF to clean, AI-formatted markdown and save to Obsidian
  -o  --obsidian    Save the response to Obsidian (optional filename)
        """)
        return

    if args.convertnote:
        if not OBSIDIAN_VAULT_PATH:
            print("Obsidian vault path not set. Add OBSIDIAN_VAULT_PATH to your .env file.")
            return
        convert_pdf_to_ai_markdown(args.convertnote.strip('"'), OBSIDIAN_VAULT_PATH)
        return

    # Prompt generation
    if args.summarize:
        prompt = f"In markdown format: Summarize {args.summarize} into a medium length understandable form, around one or two paragraphs."
    elif args.question:
        prompt = f"In markdown format: Quickly answer the question (1 line), then give a more detailed summary: {args.question}"
    elif args.quotes:
        prompt = f"In markdown format: Show 10 interesting quotes from '{args.quotes}', with who said it, when, and some context."
    elif args.generate:
        prompt = f"In markdown format: Generate something based on: {args.generate}"
    elif args.wordfor:
        prompt = f"In markdown format: Give 5 close matches, 5 far matches, 3 expressions, 2 metaphors, and 3 made-up fantasy-like words to explain: {args.wordfor}"
    elif args.dnd:
        prompt = f"In markdown format: Answer this D&D question simply, then give a detailed explanation: {args.dnd}"
    elif args.code:
        prompt = f"Make code for this problem in the language stated: {args.code}"
    else:
        print("No valid command. Try `-hh` for help.")
        return

    print("\n Thinking...\n")
    response = ask_ai(prompt)
    print(" Response:\n" + response.strip())

    save_history({
        "timestamp": datetime.now().isoformat(),
        "prompt": prompt,
        "response": response
    })

    if args.obsidian:
        filename = args.obsidian if args.obsidian != "last_output" else f"jester_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        save_to_obsidian(filename, response)
        print(f"\nSaved to Obsidian as {filename}.md")


if __name__ == "__main__":
    main()
