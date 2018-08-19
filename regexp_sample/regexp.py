def calculate(data, findall):
    for match in findall(r"[abc][\+\-]?=[\+\-]?[abc]?[\+\-]?[\d]*"):
        exec(match, globals(), data)
    return data

