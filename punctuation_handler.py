def punctuation_handler(data):
    PUNCTUATIONS = [".", '?', ",", ";", ":"]
    for i in PUNCTUATIONS:
        if i in data:
            data = data.replace(i, "")
    return data