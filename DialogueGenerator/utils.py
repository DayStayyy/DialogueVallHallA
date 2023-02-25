def splitterCommaNotInQuote(text):
    """Split a string by comma, but not if the comma is in quotes. Return a list of strings."""
    result = []
    quote = False
    lastAppend = 0
    for i in range(len(text)):
        if text[i] == '"':
            quote = not quote
        elif text[i] == ',' and not quote:
            result.append(text[lastAppend:i])
            lastAppend = i + 1
    result.append(text[lastAppend:])
    return result
    