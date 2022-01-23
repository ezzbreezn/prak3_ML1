def linearize(sequence):
    for elem in sequence:
        if type(elem) is str and len(elem) == 1:
            yield elem
        elif not hasattr(elem, '__iter__'):
            yield elem
        else:
            try:
                for x in linearize(elem):
                    yield x
            except TypeError:
                yield elem
