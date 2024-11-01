import argparse
from colorama import Fore, init
from import_translations.import_translations import main as import_main
from export_translations.export_translations import main as export_main
import importlib.metadata

# Initialize colorama
init(autoreset=True)

def main():
    # Retrieve the package version dynamically
    version = importlib.metadata.version("translations-util")

    # Set up the argument parser
    parser = argparse.ArgumentParser(
        prog="translation-util",
        description=Fore.YELLOW + "Utility tool for importing and exporting translations to and from Excel files." + Fore.RESET
    )

    # Define the version flag
    parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {version}")

    # Define subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Define the `import` subcommand
    import_parser = subparsers.add_parser("import", help="Import translations from an Excel file to a TypeScript file")
    import_parser.add_argument("excel_file", type=str, help="Path to the Excel file containing translations")
    import_parser.add_argument("ts_file", type=str, help="Path to the TypeScript file to update translations")
    import_parser.add_argument("sheet_name", type=str, help="Sheet name within the Excel file")

    # Define the `export` subcommand
    export_parser = subparsers.add_parser("export", help="Export translations from a TypeScript file to an Excel file")
    export_parser.add_argument("ts_file", type=str, help="Path to the TypeScript file containing translations")
    export_parser.add_argument("excel_file", type=str, help="Path to the Excel file to save exported translations")
    export_parser.add_argument("sheet_name", type=str, help="Sheet name to save translations under in the Excel file")

    # Parse arguments and route to the correct main function
    args = parser.parse_args()

    if args.command == "import":
        import_main([args.excel_file, args.ts_file, args.sheet_name])
    elif args.command == "export":
        export_main([args.ts_file, args.excel_file, args.sheet_name])
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
