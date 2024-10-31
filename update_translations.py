import os
import sys
import pandas as pd
import re


def find_placeholders(text):
    """Finds all placeholders in the format {variable} in a given text."""
    return set(re.findall(r"\{(\w+)\}", text))


def preprocess_translation_blocks(ts_content):
    """
    Detects translation blocks marked by `// TODO: vvv Translate below vvv`
    and `// TODO: ^^^ Translate above ^^^` and appends `// TODO: Translate`
    to each line within the block.
    """
    lines = ts_content.splitlines()
    in_translation_block = False
    processed_lines = []

    for line in lines:
        # Detect the start of a translation block
        if re.match(r"//+Translate below", line):
            in_translation_block = True
            continue  # Skip this line

        # Detect the end of a translation block
        if re.match(r"//+Translate above", line):
            in_translation_block = False
            continue  # Skip this line

        # If within a translation block, add `// TODO: Translate` to each line
        if in_translation_block:
            # Append `// TODO: Translate` if not already present
            if re.match(r"\s*'.*',?\s*$", line):  # Match key-value lines
                line += " // TODO: Translate"

        processed_lines.append(line)

    return "\n".join(processed_lines)


def update_translations(excel_file, language_sheet, ts_file):
    # Extract the last section of the ts_file path
    ts_filename = os.path.basename(ts_file)

    # Load the specified language sheet from the Excel file
    df = pd.read_excel(excel_file, sheet_name=language_sheet)

    # Ensure the required columns (A, B, and C) are present
    if df.shape[1] < 3:
        print("Error: The Excel file does not contain the required columns.")
        return

    # Extract keys, English text (for reference), and translations
    translation_data = df.iloc[:, [0, 1, 2]].dropna(
        subset=[df.columns[0]]
    )  # Drop rows with no key

    # Read the TypeScript file
    with open(ts_file, "r", encoding="utf-8") as file:
        ts_content = file.read()

    # Preprocess translation blocks to add `// TODO: Translate` where needed
    ts_content = preprocess_translation_blocks(ts_content)

    # Process each translation
    for _, row in translation_data.iterrows():
        key, english_text, translation = row.iloc[0], row.iloc[1], row.iloc[2]

        # Skip if the translation is empty
        if pd.isna(translation) or translation.strip() == "":
            print(f"Skipping: '{key}': translation is empty.")
            continue

        # Check for placeholder mismatch between English and translated text
        english_placeholders = find_placeholders(english_text)
        translation_placeholders = find_placeholders(translation)

        if english_placeholders != translation_placeholders:
            print(
                f"Warning: Placeholder mismatch for key '{key}'. Skipping substitution. Expected '{english_placeholders}', found '{translation_placeholders}'."
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
            print(f"Error: No match found for key '{key}' in {ts_filename}")

    # Write the updated content back to the TypeScript file
    with open(ts_file, "w", encoding="utf-8") as file:
        file.write(ts_content)

    print(f"Translations for '{language_sheet}' updated successfully in {ts_filename}.")


# Main script entry point
if __name__ == "__main__":
    # Check for command-line arguments
    if len(sys.argv) != 4:
        print(
            "Usage: python update_translations.py <excel_file> <language_sheet> <ts_file>"
        )
        sys.exit(1)

    # Get arguments
    excel_file = sys.argv[1]
    language_sheet = sys.argv[2]
    ts_file = sys.argv[3]

    # Run the update function
    update_translations(excel_file, language_sheet, ts_file)
