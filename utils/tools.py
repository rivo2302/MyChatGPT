def correct_split(text):
    if len(text) > 2000:
        res = []
        max = 20
        words = text.split(" ")
        current = ""
        for word in words:
            current += word + " "
            if len(current) > max:
                res.append(current)
                current = ""
        return res
    else:
        return [text]
