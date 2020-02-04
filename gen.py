import re
to_angka=[["0","O"],["!","1"],["I","1"],["|","1"],["S","5"],["E","8"]]
to_huruf=[["0","O"],["!","I"],["1","I"],["|","I"],["5","S"],["8","E"]]
kode_plat = ["BL","BB","BK","BA","BM","BP","BG","BN","BE","BD","BH","A",\
            "B","D","E","F","T","Z","G","H","K","R","AA","AB","AD","L","M","N","P",\
            "S","W","AE","AG","DK","DR","EA","DH","EB","ED","KB","DA","KH","KT",\
            "DB","DL","DM","DN","DT","DD","DC","DE","DG","DS"]
kode_plat =set (kode_plat)

def replaceToAngka(val):
    for i in to_angka:
        if val==i[0]:
            return i[1]
    return ""

def replaceToHuruf(val):
    for i in to_huruf:
        if val==i[0]:
            return i[1]
    return ""


def getPlat(plat):
    pl0 = ""
    pl1 = ""
    pl2 = ""
    #get plat kota
    for i in range(0,2):
        try:
            if(type(int(plat[i])))==int:
                pass
        except ValueError:
            val = pl0+plat[i]
            if val in kode_plat:
                pl0+=plat[i]

    #get plat angka
    for i in range(len(pl0),len(pl0)+4):
        try:
            if(type(int(plat[i])))==int:
                pl1+=plat[i]
        except ValueError:
            pl1+=replaceToAngka(plat[i])
    #get plat huruf belakang
    for i in range(len(pl0)+len(pl1),len(plat)):
        try:
            if(type(int(plat[i])))==int:
                pl2+=replaceToHuruf(plat[i])
        except ValueError:
            pl2+=plat[i]

    plat=pl0+"-"+pl1+"-"+pl2
    return plat

def removeSymbol(val):
    val  = re.sub("[^0-9a-zA-Z]","",val)
    return val

plat=input("masukan Plat : ")
pl = removeSymbol(plat)
pl = getPlat(pl)
print(pl)