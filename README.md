# translations-util

Command line tools for extracting and importing translations from and to Excel files.

## Installation

To install the dependencies for this project, use [Poetry](https://python-poetry.org/):

```sh
poetry install
```

## Usage

This tool allows you to update translations in a TypeScript file based on an Excel file. The Excel file should contain the translations in a specific format.

### Command Line Usage

```sh
python update_translations.py <excel_file_path> <language_sheet_name> <ts_file_path>
```

- `<excel_file_path>`: Path to the Excel file containing the translations.
- `<language_sheet_name>`: Name of the sheet in the Excel file that contains the translations.
- `<ts_file_path>`: Path to the TypeScript file to be updated.

### Example

```sh
python update_translations.py translations.xlsx French translations.ts
```

This command will update the `translations.ts` file with the French translations from the `translations.xlsx` file.

## Excel File Format

The Excel file should have at least three columns:
1. **Key**: The key for the translation.
2. **English Text**: The original English text.
3. **Translation**: The translated text.

## Features

- **Placeholder Matching**: Ensures that placeholders in the format `{variable}` are consistent between the English text and the translation.
- **Translation Blocks**: Detects and processes translation blocks marked by `// TODO: vvv Translate below vvv` and `// TODO: ^^^ Translate above ^^^`.

## Development

To contribute to this project, clone the repository and install the dependencies using Poetry:

```sh
git clone <repository-url>
cd translations-util
poetry install
```

## License

This project is licensed under the MIT License.
