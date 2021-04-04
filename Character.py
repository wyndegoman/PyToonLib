import json


class CharGen:
    strPts = 0
    dexPts = 0
    conPts = 0
    bodPts = 0

    pcvPts = 0
    pdPts = 0
    edPts = 0
    recPts = 0
    endPts = 0
    stunPts = 0

    def cost(self):
        return self.strPts + self.dexPts + self.conPts + self.bodPts \
                + self.pcvPts + self.pdPts + self.edPts + self.recPts + self.endPts + self.stunPts


def round_stat(pts, cost):
    return int(pts/cost + 0.5)


class Stats:
    str = 10
    dex = 10
    con = 10
    bod = 10

    pcv = 3
    pd = 2
    ed = 2
    rec = 4
    end = 20
    stun = 20

    def recalc(self, chargen):
        self.str = 10 + round_stat(chargen.strPts, 1)
        self.dex = 10 + round_stat(chargen.dexPts, 3)
        self.con = 10 + round_stat(chargen.conPts, 2)
        self.bod = 10 + round_stat(chargen.bodPts, 2)

        self.pcv = round_stat(self.dex + chargen.pcvPts, 3)
        self.pd = round_stat(self.str + chargen.pdPts, 5)
        self.ed = round_stat(self.con + chargen.edPts, 5)
        self.rec = round_stat(self.str + self.con + chargen.recPts, 5)
        self.end = round_stat(self.con + chargen.endPts, 0.5)
        self.stun = round_stat(self.bod, 1) + round_stat(self.str + self.con + chargen.stunPts, 2)

    def get_stat(self, name):
        return self.__dict__[name]

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)


class Character:
    name = ""
    gen = CharGen()
    stats = Stats()
    skills = []

    def __init__(self, name):
        self.name = name
        self.recalc()

    def recalc(self):
        self.stats.recalc(self.gen)

    def cost(self):
        return self.gen.cost()

    def __str__(self):
        skill_list = ",\n".join(map(str, self.skills))
        return f"{self.name}<{self.cost()}> Stats {self.stats.__str__()} Skills [\n{skill_list}\n]"
