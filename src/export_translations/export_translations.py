import os
import re
import pandas as pd
from colorama import Fore, init

from src.util import find_translation_blocks

# Initialize colorama for colored output
init(autoreset=True)


def extract_translations_with_todo(ts_content):
    """
    Extracts translation key-value pairs marked with `// TODO: Translate`.
    """
    pattern = r"'(.*?)':\s*'(.*?)',?\s*// TODO: Translate"
    matches = re.findall(pattern, ts_content)
    return matches


def preprocess_translation_blocks(ts_file):
    with open(ts_file, "r", encoding="utf-8") as file:
        ts_content = file.read()

    # Preprocess translation blocks and extract marked translations
    ts_content = find_translation_blocks(ts_content)

    with open(ts_file, "w", encoding="utf-8") as file:
        file.write(ts_content)


def export_translations_to_excel(ts_file, excel_file, sheet_name):
    preprocess_translation_blocks(ts_file)

    # Read TypeScript file content
    with open(ts_file, "r", encoding="utf-8") as file:
        ts_content = file.read()
    translations = extract_translations_with_todo(ts_content)

    # Create DataFrame for exporting
    df = pd.DataFrame(translations, columns=["Translation key", "English text"])
    df[sheet_name + " text"] = ""

    # Write to Excel file
    with pd.ExcelWriter(excel_file, mode="a" if os.path.exists(excel_file) else "w") as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)

    print(Fore.GREEN + f"Translations exported to '{excel_file}' in sheet '{sheet_name}' successfully.")


def main():
    import sys

    if len(sys.argv) != 4:
        print(
            Fore.RED + "Usage: export_translations <ts_file> <excel_file> <sheet_name>"
        )
        sys.exit(1)

    ts_file = sys.argv[1]
    excel_file = sys.argv[2]
    sheet_name = sys.argv[3]

    export_translations_to_excel(ts_file, excel_file, sheet_name)

if __name__ == '__main__':
    main()

