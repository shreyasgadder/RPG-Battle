from classes.game import Person, bColors
from classes.magic import Spell
from classes.inventory import Item
import random
import re


# Create Black magic
fire = Spell("Fire", 25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
blizzard = Spell("Blizzard", 25, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 14, 140, "black")

# Create White magic
cure = Spell("Cure", 25, 650, "white")
cura = Spell("Cura", 32, 1200, "white")
curaga = Spell("Curaga", 50, 60000, "white")

# Create Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hi_potion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
super_potion = Item("Super Potion", "potion", "Heals 50 HP", 1000)
elixir = Item("elixir", "elixir", "Fully restores HP/HP of one party member", 9999)
hi_elixir = Item("Mega Elixir", "elixir", "Fully restores party's HP/HP", 9999)
grenade = Item("Grenade", "attack", "Deals 500 Damage", 500)

# Choosing Items and Spells
player_spells = [fire, thunder, blizzard, meteor, cure, cura]
enemy_spells = [fire, meteor, curaga]

player_items = [{"item": potion, "quantity": 15},
                {"item": hi_potion, "quantity": 5},
                {"item": super_potion, "quantity": 5},
                {"item": elixir, "quantity": 5},
                {"item": hi_elixir, "quantity": 2},
                {"item": grenade, "quantity": 5}]

# Instantiate Players
player1 = Person("Venom :", 3460, 123, 300, 34, player_spells, player_items)
player2 = Person("Beast :", 4650, 135, 310, 34, player_spells, player_items)
player3 = Person("Robot :", 2460, 167, 260, 34, player_spells, player_items)

enemy1 = Person("Sagrus", 1250, 130, 560, 325, enemy_spells, [])
enemy2 = Person("Thanos", 11200, 700, 650, 25, enemy_spells, [])
enemy3 = Person("Netrus", 1250, 130, 560, 325, enemy_spells, [])


players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True

print(bColors.FAIL + bColors.BOLD + "Enemy attacks" + bColors.ENDC)

while running:
    print("=======================================================")

    print("\n\n")
    print("NAME                     HP                                   MP")
    for player in players:
        player.get_stats()

    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        player.choose_action()
        choice = input("    Choose action:")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)

            enemies[enemy].take_damage(dmg)
            print("You attacked " + enemies[enemy].name + " for", dmg, "points of damage.")

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name + " has died.")
                del enemies[enemy]

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose Magic:")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bColors.FAIL + "\nNot Enough MP" + bColors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bColors.OKBLUE + "\n" + spell.name + "heals for", magic_dmg, "HP" + bColors.ENDC)

            elif spell.type == "black":
                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(magic_dmg)
                print(bColors.OKBLUE + "\n" + spell.name + " deals", magic_dmg, "points of damage to "
                      + enemies[enemy].name + bColors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name + " has died.")
                    del enemies[enemy]

        elif index == 2:
            player.choose_item()
            item_choice = int(input("    Choose Item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bColors.FAIL + "\nNONE LEFT........" + bColors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bColors.OKGREEN + "\n" + item.name + " heals for " + str(item.prop) + bColors.ENDC)

            elif item.type == "elixir":
                if item.name == "Mega Elixir":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bColors.OKGREEN + "\n" + item.name + " fully restores HP/HP " + bColors.ENDC)

            elif item.type == "attack":
                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(item.prop)
                print(bColors.FAIL + "\n" + item.name + " deals", item.prop, "points of damage to "
                      + enemies[enemy].name + bColors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name + " has died.")
                    del enemies[enemy]

    # Check if battle is over
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    # Check if player won
    if defeated_enemies == 2:
        print(bColors.OKGREEN + "You Win!" + bColors.ENDC)
        running = False

    # Check if enemy won
    elif defeated_players == 2:
        print(bColors.FAIL + "Your Enemies has defeated you" + bColors.ENDC)
        running = False
    print("\n")
    # Enemy attack phase
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)

        # Chose attack
        if enemy_choice == 0:
            target = random.randrange(0, 2)
            enemy_dmg = enemy.generate_damage()
            players[target].take_damage(enemy_dmg)
            print(enemy.name + " attacked " + players[target].name.replace(":", "")
                  + " for", enemy_dmg, "points of damage.")

        # Chose magic
        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bColors.FAIL + spell.name + " heals " + enemy.name + " for", magic_dmg, "HP" + bColors.ENDC)

            elif spell.type == "black":
                target = random.randrange(0, 2)

                players[target].take_damage(magic_dmg)
                print(bColors.OKBLUE + enemy.name + "'s " + spell.name + " deals", magic_dmg,
                      "points of damage to " + players[target].name + bColors.ENDC)

                if players[target].get_hp() == 0:
                    print(players[target].name + " has died.")
                    del players[target]

            # print("Enemy chose", spell, "damage is", magic_dmg)



