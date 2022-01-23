def get_new_dictionary(input_dict_name, output_dict_name):
    f1 = open(input_dict_name, 'r')
    f2 = open(output_dict_name, 'w')
    num = int(f1.readline())
    d = {}
    for i in range(num):
        s = f1.readline()
        if s[len(s) - 1] == '\n':
            s = s[:-1:]
        translate = s.split(" - ")[0]
        leftover = s.split(" - ")[1]
        sources = leftover.split(", ")
        for word in sources:
            if word not in d:
                d[word] = [translate]
            else:
                d[word].append(translate)
    f1.close()
    f2.write(str(len(d)) + '\n')
    sorted_keys = list(d.keys())
    sorted_keys.sort()
    for j in range(len(sorted_keys)):
        key = sorted_keys[j]
        d[key].sort()
        f2.write(key + " - ")
        for i in range(len(d[key])):
            f2.write(d[key][i])
            if i < len(d[key]) - 1:
                f2.write(", ")
        if j < len(sorted_keys) - 1:
            f2.write("\n")
    f2.close()
