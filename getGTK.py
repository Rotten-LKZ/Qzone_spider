import sys
import re


def getGTK(cookie):
    def LongToInt(value):
        if isinstance(value, int):
            return int(value)
        else:
            return int(value & sys.maxint)

    def LeftShiftInt(number, step):
        return int(number << step)

    def getOldGTK(skey):
        a = 5381
        for i in range(0, len(skey)):
            a = a + LeftShiftInt(a, 5) + ord(skey[i])
            a = LongToInt(a)
        return a & 0x7fffffff

    def getNewGTK(p_skey, skey, rv2):
        b = p_skey or skey or rv2
        a = 5381
        for i in range(0, len(b)):
            a = a + LeftShiftInt(a, 5) + ord(b[i])
            a = LongToInt(a)
        return a & 0x7fffffff

    # @1h4BB3B54 804BF877775DC07D0B313E9BC345C0C10A8DC211948584EB47 1081244980

    if re.search(r'p_skey=(?P<p_skey>[^;]*)', cookie):
        p_skey = re.search(r'p_skey=(?P<p_skey>[^;]*)', cookie).group('p_skey')
    else:
        p_skey = None
    if re.search(r'skey=(?P<skey>[^;]*)', cookie):
        skey = re.search(r'skey=(?P<skey>[^;]*)', cookie).group('skey')
    else:
        skey = None
    if re.search(r'rv2=(?P<rv2>[^;]*)', cookie):
        rv2 = re.search(r'rv2=(?P<rv2>[^;]*)', cookie).group('rv2')
    else:
        rv2 = None

        # print(p_skey)
        # print(skey)
        # print(rv2)
        # print(getOldGTK(skey))
    return getNewGTK(p_skey, skey, rv2)


if __name__ == "__main__":
    pass