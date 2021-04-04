import json
import copy
from Character import round_stat


class SkillType:
    name = "Major"
    entry_pts = 3
    level_pts = 2

    def __init__(self, name, entry_pts, level_pts):
        self.name = name
        self.entry_pts = entry_pts
        self.level_pts = level_pts

    def rank(self, pts):
        if pts < self.entry_pts:
            return 0
        return 1 + (pts - self.entry_pts)/self.level_pts


MajorSkill = SkillType("Major", 3, 2)
MinorSkill = SkillType("Minor", 2, 1)


class Skill:
    name = ""
    base_stat = ""
    pts = 0
    skill_type = MajorSkill

    def __init__(self, name, base_stat, pts, skill_type):
        self.name = name
        self.base_stat = base_stat
        self.pts = pts
        self.skill_type = skill_type

    def cost(self):
        return self.pts

    def rank(self):
        return self.skill_type.rank(self.pts)

    def stat(self, stats):
        stat_value = stats.get_stat(self.bases_stat)
        if stat_value is None:
            return 2
        return round_stat(stat_value, 5)

    def roll(self):
        return int(8 + self.stat() + self.rank())

    def __str__(self):
        return f"{self.name}[{self.base_stat.upper()}/{self.rank():.0f}]"


skill_map = {
    "Language Skill": Skill("Language Skill", "int", 0, MinorSkill),
    "Profession Skill": Skill("Profession Skill", "gen", 0, MinorSkill),
    "Knowledge Skill": Skill("Knowledge Skill", "gen", 0, MinorSkill),
    "Acrobatics": Skill("Acrobatics", "dex", 0, MajorSkill)
}


def add_skill(name, base_stat, skill_type):
    skill_map[name] = Skill(name, base_stat, 0, skill_type)


def get_skill(name, pts):
    skill = skill_map[name]
    if skill is None:
        raise IndexError
    skill = copy.deepcopy(skill)
    skill.pts = pts
    return skill


def get_language(name, pts):
    skill = get_skill("Language Skill", pts)
    skill.name = f"LS:{name}"
    return skill


def get_profession(name, pts):
    skill = get_skill("Profession Skill", pts)
    skill.name = f"PS:{name}"
    return skill


def get_knowledge(name, pts):
    skill = get_skill("Knowledge Skill", pts)
    skill.name = f"KS:{name}"
    return skill


def get_area_knowledge(name, pts):
    skill = get_skill("Knowledge Skill", pts)
    skill.name = f"AK:{name}"
    return skill
