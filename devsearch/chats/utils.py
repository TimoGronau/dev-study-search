import re

def insert_line_breaks(text, max_line_length=50):
    words = re.findall(r'\S+\s*', text)
    for i in range(len(words)):
        if len(words[i]) > 40:
            words[i] = re.sub(r'(.{39})', r'\1-<br>', words[i])

    
    lines = []
    current_line = ''

    for word in words:
        if len(current_line) + len(word) <= max_line_length:
            current_line += word
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return '<br>'.join(lines)