from Character import Character
import SkillBase

# Press Shift+F10 to execute it or replace it with your code.


def test_character(name):
    toon = Character(name)
    toon.gen.strPts = 5
    toon.gen.dexPts = 21
    toon.gen.conPts = 6
    toon.skills.append(SkillBase.get_skill("Acrobatics", 5))
    toon.recalc()
    print(toon)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test_character('ZeroHero')
