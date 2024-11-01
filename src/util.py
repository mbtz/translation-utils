import re


def find_translation_blocks(ts_content):
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
        if re.match(r"\s*//.+Translate below.*", line):
            in_translation_block = True
            continue  # Skip this line

        # Detect the end of a translation block
        if re.match(r"\s*//.+Translate above.*", line):
            in_translation_block = False
            continue  # Skip this line

        # If within a translation block, add `// TODO: Translate` to each line
        if in_translation_block:
            if re.match(r"\s*'.*',?\s*$", line):  # Match key-value lines
                line += " // TODO: Translate"

        processed_lines.append(line)

    return "\n".join(processed_lines)