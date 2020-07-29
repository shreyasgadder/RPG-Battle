import random
from classes.magic import Spell
from classes.inventory import Item
import pprint


class bColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Person:
    def __init__(self, name, hp, mp, atk, df, magic, items):
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df
        self.magic = magic
        self.items = items
        self.actions = ['Attack', 'Magic', 'Item']
        self.name = name

    def generate_damage(self):
        return random.randrange(self.atkl, self.atkh)

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, dmg):
        self.hp += dmg
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.maxmp

    def reduce_mp(self, cost):
        self.mp -= cost

    def choose_action(self):
        i = 1
        print("\n    " + bColors.BOLD + self.name + bColors.ENDC)
        print(bColors.OKBLUE + bColors.BOLD + "    ACTIONS" + bColors.ENDC)
        for item in self.actions:
            print("        " + str(i) + ".", item)
            i += 1

    def choose_magic(self):
        i = 1
        print("\n" + bColors.OKBLUE + bColors.BOLD + "    MAGICS" + bColors.ENDC)
        for spell in self.magic:
            print("        " + str(i) + ".", spell.name, "(cost:", str(spell.cost) + ")")
            i += 1

    def choose_item(self):
        i = 1
        print("\n" + bColors.OKGREEN + bColors.BOLD + "    ITEMS" + bColors.ENDC)
        for item in self.items:
            print("        " + str(i) + ".", item["item"].name, ":", item["item"].desc, "(x" + str(item["quantity"]) + ")")
            i += 1

    def choose_target(self, enemies):
        i = 1
        print("\n" + bColors.FAIL + bColors.BOLD + "    TARGET:" + bColors.ENDC)
        for enemy in enemies:
            if enemy.get_hp() != 0:
                print("        " + str(i) + "." + enemy.name)
                i += 1
        choice = int(input("    Choose target:")) - 1
        return choice

    def get_enemy_stats(self):
        hp_bar = ""
        bar_ticks = (self.hp / self.maxhp) * 50

        while bar_ticks > 0:
            hp_bar += "█"
            bar_ticks -= 1

        while len(hp_bar) < 50:
            hp_bar += " "

        hp_str = str(self.hp) + "/" + str(self.maxhp)
        current_hp = ""

        if len(hp_str) < 11:
            decreased = 11 - len(hp_str)

            while decreased > 0:
                current_hp += " "
                decreased -= 1

            current_hp += hp_str

        else:
            current_hp = hp_str

        print("                           __________________________________________________")
        print(bColors.BOLD + self.name + "        " + current_hp + " |"
              + bColors.FAIL + hp_bar + bColors.ENDC + "|")

    def get_stats(self):
        hp_bar = ""
        bar_ticks = (self.hp / self.maxhp) * 25

        mp_bar = ""
        mp_ticks = (self.mp / self.maxmp) * 10

        while bar_ticks > 0:
            hp_bar += "█"
            bar_ticks -= 1

        while len(hp_bar) < 25:
            hp_bar += " "

        while mp_ticks > 0:
            mp_bar += "█"
            mp_ticks -= 1

        while len(mp_bar) < 10:
            mp_bar += " "

        hp_str = str(self.hp) + "/" + str(self.maxhp)
        current_hp = ""

        if len(hp_str) < 9:
            decreased = 9 - len(hp_str)

            while decreased > 0:
                current_hp = " "
                decreased -= 1

            current_hp += hp_str

        else:
            current_hp = hp_str

        mp_str = str(self.mp) + "/" + str(self.maxmp)
        current_mp = ""

        if len(mp_str) < 7:
            decreased = 7 - len(mp_str)

            while decreased > 0:
                current_mp = " "
                decreased -= 1

            current_mp += mp_str

        else:
            current_mp = mp_str

        print("                            _________________________              __________")
        print(bColors.BOLD + self.name + "          " + current_hp + " |"
              + bColors.OKGREEN + hp_bar + bColors.ENDC +
              bColors.BOLD + "|    " + current_mp + " |"
              + bColors.OKBLUE + mp_bar + bColors.ENDC + "|")

    def choose_enemy_spell(self):
        magic_choice = random.randrange(0, len(self.magic))
        spell = self.magic[magic_choice]
        magic_dmg = spell.generate_damage()

        pct = self.hp / self.maxhp * 100

        if self.mp < spell.cost or spell.type == "white" and pct > 50:
            self.choose_enemy_spell()

        else:
            return spell, magic_dmg