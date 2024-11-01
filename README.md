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
translation-util {import,export} ...
```

#### Import Command
```sh
translation-util import <excel_file> <ts_file> <sheet_name>
```

- `<excel_file>`: Path to the Excel file containing the translations.
- `<ts_file>`: Path to the TypeScript file to be updated.
- `<sheet_name>`: Name of the sheet in the Excel file that contains the translations.

#### Export Command
```sh
translation-util export <ts_file> <excel_file> <sheet_name>
```

- `<ts_file>`: Path to the TypeScript file containing translations.
- `<excel_file>`: Path to the Excel file to save exported translations.
- `<sheet_name>`: Sheet name to save translations under in the Excel file.

### Example
```sh
translation-util import path/to/translations.xlsx path/to/translations-french.ts French
```
This command will update the `translations-french.ts` file with the French translations from the `translations.xlsx`
file, under the `French` Excel sheet name.

```sh
translation-util export path/to/translations-french.ts path/to/translations.xlsx French
```
This command will export the translations from the `translations-french.ts` file to the `translations.xlsx` file, under the `French` Excel sheet name.
The Excel will follow the format from the [Excel File Format](#Excel-File-Format) section.
</details>


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

| Key                                          | English Text                           | French text                           |
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

