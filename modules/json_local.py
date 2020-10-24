import json

def _remove_comment(json_string: str) -> str:

    quote_character: str = '"'
    comment_character: str = '#'

    lines: list = json_string.split('\n')
    is_inside_quoting: bool = False
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            character: str = lines[i][j]
            if (character == quote_character):
                is_inside_quoting ^= True
            elif (character == comment_character):
                if (not is_inside_quoting):
                    lines[i] = lines[i][:j]
                    break
    return '\n'.join(lines)

def json_loads(json_string: str, should_interpret_comment: bool = False) -> dict:
    if (should_interpret_comment):
        json_string = _remove_comment(json_string)
    return json.loads(json_string)

def json_loadf(filepath: str, should_interpret_comment: bool = False) -> dict:
    with open(filepath, 'r') as f:
        json_string: str = f.read()
    return json_loads(json_string, should_interpret_comment)

