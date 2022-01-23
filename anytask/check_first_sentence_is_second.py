def check_first_sentence_is_second(s1, s2):
    w1 = s1.split()
    w2 = s2.split()
    d1 = {}
    d2 = {}
    for w in w1:
        if w not in d1:
            d1[w] = 1
        else:
            d1[w] += 1
    for w in w2:
        if w not in d2:
            d2[w] = 1
        else:
            d2[w] += 1
    for key in d2:
        if key not in d1 or d1[key] < d2[key]:
            return False
    return True
