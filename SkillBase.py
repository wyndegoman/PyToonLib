import json
import copy
from Character import round_stat


# Type of skill (from a mechanics viewpoint)
class SkillType:
    def __init__(self, name, entry_pts, level_pts, is_everyman):
        self.name = name
        self.entry_pts = entry_pts
        self.level_pts = level_pts
        self.is_everyman = is_everyman

    def rank(self, pts):
        if pts < self.entry_pts:
            if pts > 0:
                return "F"
            if self.is_everyman:
                return "E"
            return "U"
        return str(1 + int((pts - self.entry_pts)/self.level_pts))


# The currently known types of skills
MajorSkill = SkillType("Major", 3, 2, False)
EverymanSkill = SkillType("Everyman", 3, 2, True)
MinorSkill = SkillType("Minor", 2, 1, False)
CombatSkill = SkillType("Combat", 3, 3, False)


# The data for a specific skill
class Skill:
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
        stat_value = stats.get_value(self.base_stat)
        if stat_value is None:
            return 2
        return stat_value

    def roll(self, stats):
        rank = self.rank()
        if rank == 'F' or rank == 'E':
            return 8
        if not rank.isnumeric():
            return None
        return int(9 + self.stat(stats) + int(rank))

    def __str__(self):
        return f"{self.name:30s}{self.base_stat.upper():5s}{self.rank():5s}"


# The map of known skills
skill_map = {
    # General Skills
    "Mental Area Skill": Skill("Mental Area Skill", "inf", 0, MinorSkill),
    "Knowledge Area Skill": Skill("Knowledge Area Skill", "skf", 0, MinorSkill),
    "Physical Area Skill": Skill("Physical Area Skill", "dxf", 0, MinorSkill),
    "Presence Area Skill": Skill("Presence Area Skill", "prf", 0, MinorSkill),
    "Melee Skill": Skill("Melee Skill", "mcv", 0, CombatSkill),
    "Ranged Skill": Skill("Ranged Skill", "rcv", 0, CombatSkill),
    # Physical Skills
    "Acrobatics": Skill("Acrobatics", "dxf", 0, MajorSkill),
    "Breakfall": Skill("Breakfall", "dxf", 0, MajorSkill),
    "Climbing": Skill("Climbing", "dxf", 0, MajorSkill),
    "Contortionist": Skill("Contortionist", "dxf", 0, MajorSkill),
    "Driving": Skill("Driving", "dxf", 0, MajorSkill),
    "FastDraw": Skill("FastDraw", "dxf", 0, MajorSkill),
    "Piloting": Skill("Piloting", "dxf", 0, MajorSkill),
    "Lockpicking": Skill("Lockpicking", "dxf", 0, MajorSkill),
    "Riding": Skill("Riding", "dxf", 0, MajorSkill),
    "Running": Skill("Running", "dxf", 0, EverymanSkill),
    "SleightOfHand": Skill("SleightOfHand", "dxf", 0, MajorSkill),
    "Stealth": Skill("Stealth", "dxf", 0, EverymanSkill),
    "Swimming": Skill("Swimming", "dxf", 0, MajorSkill),
    "Teamwork": Skill("Teamwork", "dxf", 0, MajorSkill),
    # Mental Skills
    "Analyze": Skill("Analyze", "inf", 0, MajorSkill),
    "Concealment": Skill("Concealment", "inf", 0, EverymanSkill),
    "Criminology": Skill("Criminology", "inf", 0, MajorSkill),
    "Deduction": Skill("Deduction", "inf", 0, EverymanSkill),
    "Disguise": Skill("Disguise", "inf", 0, MajorSkill),
    "Forgery": Skill("Forgery", "inf", 0, MajorSkill),
    "Gambling": Skill("Gambling", "inf", 0, MajorSkill),
    "Inventor": Skill("Inventor", "inf", 0, MajorSkill),
    "Lipreading": Skill("Lipreading", "inf", 0, MajorSkill),
    "Mechanics": Skill("Mechanics", "inf", 0, MajorSkill),
    "Mimicry": Skill("Mimicry", "inf", 0, MajorSkill),
    "Navigation": Skill("Navigation", "inf", 0, MajorSkill),
    "Surgeon": Skill("Surgeon", "inf", 0, MajorSkill),
    "Shadowing": Skill("Shadowing", "inf", 0, MajorSkill),
    "Survival": Skill("Survival", "inf", 0, MajorSkill),
    "Tactics": Skill("Tactics", "inf", 0, MajorSkill),
    # Presence Skills
    "Acting": Skill("Acting", "prf", 0, MajorSkill),
    "AnimalHandler": Skill("AnimalHandler", "prf", 0, MajorSkill),
    "Bribery": Skill("Bribery", "prf", 0, MajorSkill),
    "Conversation": Skill("Conversation", "prf", 0, MajorSkill),
    "Courtier": Skill("Courtier", "prf", 0, MajorSkill),
    "Intimidation": Skill("Intimidation", "prf", 0, MajorSkill),
    "Streetwise": Skill("Streetwise", "prf", 0, MajorSkill),
    "Oratory": Skill("Oratory", "prf", 0, MajorSkill),
    "Persuasion": Skill("Persuasion", "prf", 0, MajorSkill),
    "Seduction": Skill("Seduction", "prf", 0, MajorSkill),
    "Trading": Skill("Trading", "prf", 0, MajorSkill),
    # General Skills
    "Tracking": Skill("Tracking", "skf", 0, MajorSkill),
    "Ventriloquist": Skill("Ventriloquist", "skf", 0, MajorSkill),
    "Weaponsmith": Skill("Weaponsmith", "skf", 0, MajorSkill),
    # Autofire
    # Martial Arts
    # Power
    # Rapid Attack
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
    skill = get_skill("Presence Area Skill", pts)
    skill.name = f"LS:{name}"
    return skill


def get_culture(name, pts):
    skill = get_skill("Mental Area Skill", pts)
    skill.name = f"CS:{name}"
    return skill


def get_science(name, pts):
    skill = get_skill("Mental Area Skill", pts)
    skill.name = f"SS:{name}"
    return skill


def get_extreme_env(name, pts):
    skill = get_skill("Knowledge Area Skill", pts)
    skill.name = f"ES:{name}"
    return skill


def get_profession(name, pts):
    skill = get_skill("Knowledge Area Skill", pts)
    skill.name = f"PS:{name}"
    return skill


def get_knowledge(name, pts):
    skill = get_skill("Knowledge Area Skill", pts)
    skill.name = f"KS:{name}"
    return skill


def get_area_knowledge(name, pts):
    skill = get_skill("Knowledge Area Skill", pts)
    skill.name = f"AK:{name}"
    return skill


def get_vehicle(name, pts):
    skill = get_skill("Physical Area Skill", pts)
    skill.name = f"TF:{name}"
    return skill


def get_beast(name, pts):
    skill = get_skill("Presence Area Skill", pts)
    skill.name = f"BF:{name}"
    return skill


def get_melee_weapon(name, pts):
    skill = get_skill("Melee Skill", pts)
    skill.name = f"MW:{name}"
    return skill


def get_ranged_weapon(name, pts):
    skill = get_skill("Ranged Skill", pts)
    skill.name = f"RW:{name}"
    return skill
