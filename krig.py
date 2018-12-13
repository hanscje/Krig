import random
import sys
from network import ClientSocket, ServerSocket

class Kort(object):

    def __init__(self, farge, verdi):
        self.farge = farge
        self.verdi = verdi

    def __cmp__(self, other):
        return cmp(self.verdi, other.verdi)


class Spiller(object):

    def __init__(self, hånd):
        self.hånd = hånd
        self.bunke = []

    def visKort(self):
        if not self.hånd:
            if not self.bunke:
                return None
            else:
                self.hånd = self.bunke.copy()
                self.bunke.clear()
        tall = random.randrange(0, len(self.hånd))
        return self.hånd.pop(tall)

    def vantKort(self, kort):
        self.bunke.extend(kort)

    def trekkTreKort(self):
        trekort = []
        for i in range(4):
            trukket = self.visKort()
            if not trukket:
                return trekort
            trekort.append(trukket)
        return trekort

    def kortIgjen(self):
        return len(self.hånd) + len(self.bunke)

def lagKortstokk():
    kortstokk = []
    for i in ['Ruter', 'Kløver', 'Hjerter', 'spar']:
        for j in range(1,14):
            kortstokk.append (Kort(i, j))
    return kortstokk

class Spill(object):

    def __init__(self):
        kortstokk = lagKortstokk()
        bunke1  = []
        bunke2  = []
        while kortstokk:
            bunke1.append(kortstokk.pop(random.randrange(0, len(kortstokk))))
            bunke2.append(kortstokk.pop(random.randrange(0, len(kortstokk))))

        self.trine = Spiller(bunke1)
        self.hans = Spiller(bunke2)
        self.rundeteller = 0


    def spillRunde(self):
        kort1 = self.trine.visKort()
        if not kort1:
            print("Hans vant på runde: ", self.rundeteller)
            pass
        kort2 = self.hans.visKort()
        if not kort2:
            print("Trine vant på runde: ", self.rundeteller)
            pass

        #print("Antall kort hos Trine: ", self.trine.kortIgjen()+1, " Antall kort hos Hans: ",
        #        self.hans.kortIgjen()+1)

        print('Runde #',self.rundeteller, 'Trine: ', kort1.farge, ' ', kort1.verdi,
                '\t\t Hans: ', kort2.farge, ' ', kort2.verdi)

        if kort1.verdi > kort2.verdi:
            self.trine.vantKort([kort1, kort2])
        elif kort1.verdi < kort2.verdi:
            self.hans.vantKort([kort1, kort2])
        else:
            self.krig([kort1], [kort2])
        self.rundeteller += 1


    def krig(self, trinekrigsbunke, hanskrigsbunke):
        bunke = []
    #krigteller = 1
        while True:
            #if krigteller > 2:
            #    print("Dobbelkrig! ", krigteller)
            trineTreKort = self.trine.trekkTreKort()
            if trineTreKort:
                trinekrigsbunke.extend(trineTreKort)

            hansTreKort = self.hans.trekkTreKort()
            if hansTreKort:
                hanskrigsbunke.extend(hansTreKort)

            kampkort1 = trinekrigsbunke.pop(len(trinekrigsbunke) -1)
            kampkort2 = hanskrigsbunke.pop(len(hanskrigsbunke) -1)

            if kampkort1.verdi > kampkort2.verdi:
                bunke.extend(trinekrigsbunke)
                bunke.extend(hanskrigsbunke)
                bunke.extend([kampkort1, kampkort2])
                self.trine.vantKort(bunke)
                print("Trine vant en krig mot Hans")
                break
            elif kampkort1.verdi < kampkort2.verdi:
                bunke.extend(trinekrigsbunke)
                bunke.extend(hanskrigsbunke)
                bunke.extend([kampkort1, kampkort2])
                self.hans.vantKort(bunke)
                print("Hans vant en krig mot Trine")
                break
            trinekrigsbunke.append(kampkort1)
            hanskrigsbunke.append(kampkort2)


if __name__ == "__main__":
    port = 5050
    runder = 100
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    if len(sys.argv) > 2:
        runder = max(int(sys.argv[2]), 1)

    #spillTjener = ServerSocket(port, False)
    spill = Spill()
    
    for i in range(runder):
        spill.spillRunde()
