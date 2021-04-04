import json


# Choices made in character creation
class CharGen:
    str_pts = 0
    dex_pts = 0
    con_pts = 0
    bodPts = 0

    mcv_pts = 0
    rcv_pts = 0
    dcv_pts = 0
    pd_pts = 0
    ed_pts = 0
    spd_pts = 0
    rec_pts = 0
    end_pts = 0
    stun_pts = 0

    def cost(self):
        return self.str_pts + self.dex_pts + self.con_pts + self.bodPts \
               + self.mcv_pts + self.rcv_pts + self.dcv_pts + self.pd_pts + self.ed_pts + +self.spd_pts \
               + self.rec_pts + self.end_pts + self.stun_pts


# Derived statistics for a character
class Stats:
    str = 10
    dex = 10
    con = 10
    bod = 10

    dxf = 2

    mcv = 3
    rcv = 3
    dcv = 3
    pd = 2
    ed = 2
    spd = 1.0
    rec = 4
    end = 20
    stun = 20

    def recalc(self, chargen):
        self.str = 10 + round_stat(chargen.str_pts, 1)
        self.dex = 10 + round_stat(chargen.dex_pts, 3)
        self.con = 10 + round_stat(chargen.con_pts, 2)
        self.bod = 10 + round_stat(chargen.bodPts, 2)

        self.dxf = round_stat(self.dex, 5)

        self.mcv = round_stat(self.dex + chargen.mcv_pts*0.6, 3)
        self.rcv = round_stat(self.dex + chargen.rcv_pts*0.6, 3)
        self.dcv = round_stat(self.dex + chargen.dcv_pts*0.6, 3)
        self.pd = round_stat(self.str + chargen.pd_pts, 5)
        self.ed = round_stat(self.con + chargen.ed_pts, 5)
        self.spd = round_stat(self.dex + chargen.spd_pts, 5)/2
        self.rec = round_stat(self.str + self.con + chargen.rec_pts, 5)
        self.end = round_stat(self.con + chargen.end_pts, 0.5)
        self.stun = round_stat(self.bod, 1) + round_stat(self.str + self.con + chargen.stun_pts, 2)

    def get_value(self, stat_name):
        return self.__dict__[stat_name]

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
        cost = self.gen.cost()
        for index, skill in enumerate(self.skills):
            cost += skill.cost()
        return cost

    def roll(self, skill_name):
        for index, skill in enumerate(self.skills):
            if skill.name == skill_name:
                return skill.roll(self.stats)
        return None

    def __str__(self):
        skill_list = ",\n".join(map(str, self.skills))
        return f"{self.name}<{self.cost()}> Stats {self.stats.__str__()} Skills [\n{skill_list}\n]"


# Function to perform stats calculations
def round_stat(pts, cost):
    return int(pts/cost + 0.5)
