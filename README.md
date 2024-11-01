# translations-util

Command line tools for extracting and importing translations from and to Excel files.

## Installation
<details open>

<summary>CLI tool</summary>

Installs the package globally so that you can use the command line tool from anywhere.

```shell
pip install translations-util
```
</details>

<details>
<Summary>Install as a Python package</Summary>

## Installation with Poetry

To install using [Poetry](https://python-poetry.org/):

```sh
poetry add -D translations-util
```

Which will install the utils as a development dependency in your local python environment.

</details>

## Usage

This tool allows you to update translations in a TypeScript file based on an Excel file. The Excel file should contain 
the translations in a specific format.

<details open>

<summary> CLI usage </summary>

### Command
```sh
import-translations <excel_file_path> <language_sheet_name> <ts_file_path>
```

- `<excel_file_path>`: Path to the Excel file containing the translations.
- `<language_sheet_name>`: Name of the sheet in the Excel file that contains the translations.
- `<ts_file_path>`: Path to the TypeScript file to be updated.

### Example
```sh
import-translations path/to/translations.xlsx French path/to/translations-french.ts
```
This command will update the `translations-french.ts` file with the French translations from the `translations.xlsx` 
file, under the `French` Excel sheet name.
</details>

### Command Line Usage with python
### Example
```sh
python import_translations.py translations.xlsx French translations.ts
```


## Excel File Format

The Excel file should have at least three columns:
1. **Key**: The key for the translation.
2. **English Text**: The original English text.
3. **Translation**: The translated text.

## Features

- **Placeholder Matching**: Ensures that placeholders in the format `{variable}` are consistent between the English text and the translation.
- **Translation Blocks**: Detects and processes translation blocks marked by `// TODO: vvv Translate below vvv` and `// TODO: ^^^ Translate above ^^^`.

### Example
Assuming the Excel workbook has a sheet named `French` with the following content:

| Key                                          | English Text                           | French                                |
|----------------------------------------------|----------------------------------------|---------------------------------------|
| common.greeting-{name}                       | Hello, {name}!                         | Bonjour, {name}!                      |
| common.goodbye                               | Goodbye!                               | Au revoir!                            |
| login.username                               | Username                               | Nom d'utilisateur                     |
| login.password                               | Password                               |                                       |
| error.invalid-translation-of-variable-{name} | Invalid translation of variable {name} | Traduction invalide de variable {nom} |

The `import-translations` command will update the TypeScript file with the following content:

```javascript
export const translations = {
    ..., // Other translations
    'common.existing-translation': 'Traduction existante',
    'common.greeting-{name}': 'Bonjour, {name}!',
    'common.goodbye': 'Au revoir!',
    'login.username': "Nom d'utilisateur",
    'login.password': '', // TODO Translate
    'error.invalid-translation-of-variable-{name}': '', // TODO Translate
    ... // Other translations
};
```


## Development

To contribute to this project, clone the repository and install the dependencies using Poetry:

```sh
git clone <repository-url>
cd translations-util
poetry install
```

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE.txt) file for details.
