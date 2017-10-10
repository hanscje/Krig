import random

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


bunke1 = []
bunke2 = []

kortstokk = []
for i in ['Ruter', 'Kløver', 'Hjerter', 'spar']:
    for j in range(1,14):
        kortstokk.append (Kort(i, j))

while kortstokk:
    bunke1.append(kortstokk.pop(random.randrange(0, len(kortstokk))))
    bunke2.append(kortstokk.pop(random.randrange(0, len(kortstokk))))

trine = Spiller(bunke1)
hans = Spiller(bunke2)
rundeteller = 0


def krig(trinekrigsbunke, hanskrigsbunke):
    bunke = []

    while True:
        trineTreKort = trine.trekkTreKort()
        if trineTreKort:
            trinekrigsbunke.extend(trineTreKort)

        hansTreKort = hans.trekkTreKort()
        if hansTreKort:
            hanskrigsbunke.extend(hansTreKort)

        kampkort1 = trinekrigsbunke.pop(len(trinekrigsbunke) -1)
        kampkort2 = hanskrigsbunke.pop(len(hanskrigsbunke) -1)

        if kampkort1.verdi > kampkort2.verdi:
            bunke.extend(trinekrigsbunke)
            bunke.extend(hanskrigsbunke)
            bunke.extend([kampkort1, kampkort2])
            trine.vantKort(bunke)
            print("Trine vant en krig mot Hans")
            break
        elif kampkort1.verdi < kampkort2.verdi:
            bunke.extend(trinekrigsbunke)
            bunke.extend(hanskrigsbunke)
            bunke.extend([kampkort1, kampkort2])
            hans.vantKort(bunke)
            print("Hans vant en krig mot Trine")
            break
        trinekrigsbunke.append(kampkort1)
        hanskrigsbunke.append(kampkort2)


while True:
    kort1 = trine.visKort()
    if not kort1:
        print("Hans vant på runde: ", rundeteller)
        break
    kort2 = hans.visKort()
    if not kort2:
        print("Trine vant på runde: ", rundeteller)
        break

    #print("Antall kort hos Trine: ", trine.kortIgjen()+1, " Antall kort hos Hans: ",
    #        hans.kortIgjen()+1)

    print('Runde #',rundeteller, 'Trine: ', kort1.farge, ' ', kort1.verdi,
            '\t\t Hans: ', kort2.farge, ' ', kort2.verdi)

    if kort1.verdi > kort2.verdi:
        trine.vantKort([kort1, kort2])
    elif kort1.verdi < kort2.verdi:
        hans.vantKort([kort1, kort2])
    else:
        krig([kort1], [kort2])
    rundeteller += 1
