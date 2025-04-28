def parse_number_with_suffix(s):
    suffixes = {"K": 10**3, "M": 10**6, "B": 10**9, "T": 10**12}

    s = s.upper()
    if s[-1] in suffixes:
        return int(float(s[:-1]) * suffixes[s[-1]])
    return int(float(s))
