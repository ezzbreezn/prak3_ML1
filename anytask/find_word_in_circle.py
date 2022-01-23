def find_word_in_circle(circle, word):
    if len(circle) == 0:
        return -1
    str1 = circle
    str2 = circle[::-1]
    not_fit = False
    while True:
        pos1 = str1.find(word)
        pos2 = str2.find(word)
        if pos1 != -1:
            return pos1, 1
        elif pos2 != -1:
            return len(circle) - pos2 - 1, -1
        elif len(str1) > len(word) and not_fit:
            return -1
        else:
            str1 += circle
            str2 += circle[::-1]
            not_fit = True
