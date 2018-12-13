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

    def __init__(self, hånd, navn):
        self.hånd = hånd
        self.bunke = []
        self.navn = navn

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
    for i in ['Ruter', 'Kløver', 'Hjerter', 'Spar']:
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

        self.trine = Spiller(bunke1, "Trine")
        self.hans = Spiller(bunke2, "Hans")
        self.rundeteller = 1


    def spillRunde(self):
        seirendeSpiller = None
        kort1 = self.trine.visKort()
        if not kort1:
            seirendeSpiller = self.hans
        kort2 = self.hans.visKort()
        if not kort2:
            seirendeSpiller = self.trine

        if seirendeSpiller:
            print('\n\t\t\t', seirendeSpiller.navn, '(', seirendeSpiller.kortIgjen(), 
                'kort ) vant på runde: ', self.rundeteller, '\n')
            return True

        krigsstreng = '       '
        if kort1.verdi == kort2.verdi:
            krigsstreng = '(KRIG!)'
        print('Runde #%d\n\tTrine (%2d kort): %7s %2d   %7s   %2d %7s :(%2d kort) Hans' %
            (self.rundeteller, self.trine.kortIgjen()+1, kort1.farge, kort1.verdi, 
            krigsstreng, kort2.verdi, kort2.farge, self.hans.kortIgjen()+1))

        if kort1.verdi > kort2.verdi:
            self.trine.vantKort([kort1, kort2])
        elif kort1.verdi < kort2.verdi:
            self.hans.vantKort([kort1, kort2])
        else:   # kort1.verdi == kort2.verdi
            self.krig([kort1], [kort2])
        self.rundeteller += 1
        return False


    def krig(self, trinekrigsbunke, hanskrigsbunke):
        bunke = []

        print()
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
                print("\tTrine vant!      %7s %2d   <------   %2d %7s            Hans\n" %(
                    kampkort1.farge, kampkort1.verdi, kampkort2.verdi, kampkort2.farge))
                break
            elif kampkort1.verdi < kampkort2.verdi:
                bunke.extend(trinekrigsbunke)
                bunke.extend(hanskrigsbunke)
                bunke.extend([kampkort1, kampkort2])
                self.hans.vantKort(bunke)
                print("\tTrine            %7s %2d   ------>   %2d %7s            Hans vant!\n" %(
                    kampkort1.farge, kampkort1.verdi, kampkort2.verdi, kampkort2.farge))
                break
            trinekrigsbunke.append(kampkort1)
            hanskrigsbunke.append(kampkort2)


if __name__ == "__main__":
    port = 5050
    runder = 1
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    if len(sys.argv) > 2:
        runder = max(int(sys.argv[2]), 1)

    #spillTjener = ServerSocket(port, False)
    spill = Spill()
    
    for i in range(runder):
        seier = False
        while not seier:
            seier = spill.spillRunde()
