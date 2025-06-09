def mypow(root, exponent):
    res = 1
    for i in range(exponent):
        res *= root
    return res

def excel_ctn(col):
    col = col.upper()
    tot = len(col)
    res = 0
    for i in range(tot):
        res += (ord(col[i]) - ord('A') + 1) * mypow(26, tot - i - 1)
    return res - 1