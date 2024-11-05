import re
import math
from datetime import datetime
from dateutil import parser, relativedelta


def convert_size(size_bytes, unit='GB'):
    if size_bytes == 0:
        return 0
    size_names = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    if size_bytes < 0:
        size_bytes = abs(size_bytes)

    i = int(math.floor(math.log(size_bytes, 1024)))
    for index, size_name in enumerate(size_names):
        if size_name == unit:
            i = index
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    # logger.warning("{} {}".format(s, size_names[i]))
    return s

def ocr_remove_specials(text: str) -> str:
    text = re.sub('—', '-', text)
    text = re.sub('\s+', '', text.strip())
    return text


def str_remove_specials(text: str) -> str:
    remove_tag = r'。|◎|■|▼|◆|▽|・|･|\.|●|①|②|③|;|,|、|★|☆|＊|\+|◇|:|※|／／｜～|：' \
                 r'|－|-|\*|…|│|＋|←|→|\? |└|（※）|「|」|⇔|「|」|『|』|\u3000|' \
                 r'!|♪|！|~|％|%|～|\?|\／|\/|&|=|⇒|└|xx|>|<|\（|\）|\)|\(|【|】|＜|＞|≪|≫|\[|\]'
    text = re.sub(remove_tag, ' ', text)
    text = re.sub('\s\s+', ' ', text.strip())
    return text


def get_staff(request):
    return request.user.is_staff


def string2datetime(str_datetime):
    if type(str_datetime) is str:
        if str_datetime == '':
            dt = datetime.now()
        else:
            dt = parser.parse(str_datetime)
    else:
        dt = datetime.now()
    return dt


def write_roman(num):
    roman = {}
    roman[1000] = "M"
    roman[900] = "CM"
    roman[500] = "D"
    roman[400] = "CD"
    roman[100] = "C"
    roman[90] = "XC"
    roman[50] = "L"
    roman[40] = "XL"
    roman[10] = "X"
    roman[9] = "IX"
    roman[5] = "V"
    roman[4] = "IV"
    roman[1] = "I"

    def roman_num(num):
        for r in roman.keys():
            x, y = divmod(num, r)
            yield roman[r] * x
            num -= (r * x)
            if num > 0:
                roman_num(num)
            else:
                break

    return "".join([a for a in roman_num(num)])
