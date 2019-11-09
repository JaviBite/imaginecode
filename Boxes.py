from enum import Enum


boxes= ["pink","green","yellow","blue","red","white","black","organe","purple","brown","grey","gold",
        "silver","gold","beige","lilac","violeta","turgoise","magenta","fluor","cobalt","lapis"]
word2num = {"uno":1,
            "un":1,
            "dos":2,
            "tres":3,
            "cuatro":4,
            "cinco":5,
            "seis":6,
            "siete":7,
            "ocho":8,
            "nueve":9,
            "diez":10,
            "once":11,
            "doce":12,
            "trece":13,
            "catorce":14,
            "quince":15,
            "dieciseis":16,
            "diecisiete":17,
            "dieciocho":18,
            "diecinueve":19,
            "veinte":20}

def toNum(text):
    for num in word2num:
        if num in text:
            return word2num[num]
    return None
