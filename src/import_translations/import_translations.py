import os
import sys
import pandas as pd
import re
from colorama import Fore, Style, init

from src.util import find_translation_blocks

# Initialize colorama
init(autoreset=True)


def find_placeholders(text):
    """Finds all placeholders in the format {variable} in a given text."""
    return set(re.findall(r"\{(\w+)\}", text))


def update_translations(excel_file, ts_file, language_sheet):
    # Extract the last section of the ts_file path
    ts_filename = os.path.basename(ts_file)

    # Load the specified language sheet from the Excel file
    df = pd.read_excel(excel_file, sheet_name=language_sheet)

    # Ensure the required columns (A, B, and C) are present
    if df.shape[1] < 3:
        print(Fore.RED + "Error: The Excel file does not contain the required columns.")
        return

    # Extract keys, English text (for reference), and translations
    translation_data = df.iloc[:, [0, 1, 2]].dropna(
        subset=[df.columns[0]]
    )  # Drop rows with no key

    # Read the TypeScript file
    with open(ts_file, "r", encoding="utf-8") as file:
        ts_content = file.read()

    # Preprocess translation blocks to add `// TODO: Translate` where needed
    ts_content = find_translation_blocks(ts_content)

    # Process each translation
    for _, row in translation_data.iterrows():
        key, english_text, translation = row.iloc[0], row.iloc[1], row.iloc[2]

        # Skip if the translation is empty
        if pd.isna(translation) or translation.strip() == "":
            print(Fore.CYAN + f"Skipping '{key}': translation is empty.")
            continue

        # Check for placeholder mismatch between English and translated text
        english_placeholders = find_placeholders(english_text)
        translation_placeholders = find_placeholders(translation)

        if english_placeholders != translation_placeholders:
            print(
                Fore.LIGHTRED_EX +
                f"Error: Placeholder mismatch for key '{key}'. Skipping substitution. "
                f"Expected '{english_placeholders}', found '{translation_placeholders}'."
            )
            continue

        # Construct the regex pattern to match the key in the TypeScript file
        pattern = rf"('{key}':\s*')[^']*(')(,?\s*(// TODO: Translate)?)"
        replacement = rf"\1{translation}\2\3"

        # Replace all occurrences of the key in the TypeScript file content
        ts_content, count = re.subn(pattern, replacement, ts_content)

        # If the translation was successful, remove any "// TODO: Translate" comment
        if count > 0:
            ts_content = re.sub(
                rf"('{key}':\s*'{translation}'(?:,?))\s*// TODO: Translate",
                rf"\1",
                ts_content,
            )
        else:
            print(Fore.RED + f"Error: No match found for key '{key}' in {ts_filename}")

    # Write the updated content back to the TypeScript file
    with open(ts_file, "w", encoding="utf-8") as file:
        file.write(ts_content)

    print(Fore.GREEN + f"Translations for '{language_sheet}' updated successfully in {ts_filename}.")


# Main
def main(args=None):
    import sys
    args = args or sys.argv[1:]
    if len(args) != 3:
        print(Fore.LIGHTGREEN_EX + "Usage: translation-util import <excel_file> <ts_file> <sheet_name>")
        sys.exit(1)

    excel_file, ts_file, sheet_name = args
    update_translations(excel_file, ts_file, sheet_name)