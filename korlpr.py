from lpr import lpr


kor_dict = ["가", "나", "다", "라", "마", "거", "너", "더", "러",
            "머", "버", "서", "어", "저", "고", "노", "도", "로",
            "모", "보", "소", "오", "조", "구", "누", "두", "루",
            "무", "부", "수", "우", "주", "허", "하", "호"]
num_dict = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]


def korlpr(lprnet,crnn):
    def check_appropriate(st):
        isokay = 1
        if len(st)<=6:
            isokay = 0
        if (st[-1] not in num_dict):
            isokay = 0
        if (st[-2] not in num_dict):
            isokay = 0
        if (st[-3] not in num_dict):
            isokay = 0
        if (st[-4] not in num_dict):
            isokay = 0
        if (st[-5] not in kor_dict):
            isokay = 0
        if (st[-6] not in num_dict):
            isokay = 0
        if (st[-7] not in num_dict):
            isokay = 0
        if len(st) >= 8 and st[-8] not in num_dict:
            isokay = 0
        return isokay
    #TODO: Implement correction algorithm
    if lprnet == crnn:
        return lprnet
    else:
        #1 first check length
        #length should be over 7 characters
        if len(lprnet) < 7:
            if check_appropriate(crnn):
                if len(lprnet) < 5:
                    return " "
                return crnn
            return " "
        else:
            #lprnet has right length
            if len(crnn) < 7:
                if (check_appropriate(lprnet)):
                    return lprnet
                else:
                    return " "
            else:
                #both right length
                if (check_appropriate(lprnet) and check_appropriate(crnn)):
                    if lprnet[-5] != crnn[-5] and len(lprnet) == len(crnn):
                        #if lprnet[-4:] == crnn[-4:] and lprnet[-7:-5] == crnn[-7:-5]:
                        return lprnet[:-5]+crnn[-5]+lprnet[-4:]
                        
                    else:
                        return lprnet
                elif check_appropriate(lprnet) == 1:
                    return lprnet
                elif check_appropriate(crnn) == 1:
                    return crnn
                else:
                    return " "







