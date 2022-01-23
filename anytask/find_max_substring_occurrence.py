def find_max_substring_occurrence(input_string):
    ls = len(input_string)
    z = [0 for i in range(ls)]
    left = 0
    right = 0
    for i in range(1, ls):
        if left <= right:
            z[i] = min(z[i - left], right - i + 1)
        while i + z[i] < ls and input_string[z[i]] == input_string[i + z[i]]:
            z[i] += 1
        if i + z[i] - 1 > right:
            left = i
            right = i + z[i] - 1
    for i in range(ls):
        if i + z[i] == ls and ls % i == 0:
            return ls // i
    return 1
