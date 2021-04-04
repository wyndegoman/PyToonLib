from Character import Character
import SkillBase

# Press Shift+F10 to execute it or replace it with your code.


def test_character(name):
    toon = Character(name)
    toon.gen.str_pts = 5
    toon.gen.dex_pts = 21
    toon.gen.con_pts = 6
    toon.gen.spd_pts = 3
    toon.skills.append(SkillBase.get_skill("Acrobatics", 3))
    toon.skills.append(SkillBase.get_skill("Riding", 5))
    toon.skills.append(SkillBase.get_skill("Teamwork", 3))
    toon.skills.append(SkillBase.get_skill("Running", 0))
    toon.skills.append(SkillBase.get_skill("Swimming", 1))
    toon.skills.append(SkillBase.get_melee_weapon("Sword", 12))
    toon.skills.append(SkillBase.get_ranged_weapon("Bow", 12))
    toon.skills.append(SkillBase.get_profession("Ranger", 2))
    toon.recalc()
    print(toon)
    print(toon.roll("MW:Sword"))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test_character('ZeroHero')
