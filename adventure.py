#!/usr/bin/env python3
"""
This is a translation of an old DnD game I wrote in qbasic

                                D & D
                             BY TED KOTZ
                       WITH MUCH THANKS TO ALL
                     THAT MADE THIS GAME POSSIBLE

                  DO NOT CHANGE THIS PROGRAM AT RISK
                                 OF
                                DEATH
                                 AND
                           MINDLESS MAYHAM

"""
import json
import os
import random
import time

CLASSES = { "FIGHTER"       : (1   , 8, 5),
            "PRIEST"        : (1.25, 6, 4),
            "MONK"          : (1.5 , 6, 3),
            "THIEF"         : (1.75, 5, 3),
            "MAGE"          : (2   , 4, 2) }

WEAPONS = [ ("DAGGER"          ,  4,  2, False),
            ("SHORT SWORD"     ,  6,  5, False),
            ("BATTLE AX"       ,  8, 10, False),
            ("LONG SWORD"      , 10, 22, False),
            ("TWO HANDED SWORD", 14, 50, True ) ]


ARMOR = [ ("CHAINMAIL"       ,  4,   75),
          ("BRONZEPLATEMAIL" ,  3,  225),
          ("PLATEMAIL"       ,  2,  700),
          ("FIELD PLATEMAIL" ,  1, 2000),
          ("FULL PLATEMAIL"  ,  0, 6000) ]

FORMS = { "HUMAN" : (1),
          "ANT"   : (2),
          "BEAR"  : (3) }

class Monster:
    def __init__(self):
        self.name = ""          # Mb
        self.role = "MONSTER"   # C$
        self.gp = 0             # K
        self.ac = 0             # AC
        self.level = 0          # HD
        self.hp_plus = 0        # P
        self.regen = 0          # R
        self.num_att = 0        # MA
        self.damage = 0         # D
        self.dammod = 0         # Dp
        self.hp = 1             # M

def monster_decoder( data ):
    return_val = Monster()
    return_val.name    =     data["name"    ]
    return_val.role    = "MONSTER"
    return_val.gp      = int(data["gp"      ])
    return_val.ac      = int(data["ac"      ])
    return_val.level   = int(data["level"   ])
    return_val.hp_plus = int(data["hp_plus" ])
    return_val.regen   = int(data["regen"   ])
    return_val.num_att = int(data["num_att" ])
    return_val.damage  = int(data["damage"  ])
    return_val.dammod  = int(data["dammod"  ])
    return_val.hp      = return_val.level * 8 + return_val.hp_plus
    return return_val

class Player:
    def __init__(self):
        self.name = ""         # N$
        self.role = ""         # C$
        self.gp = 0            # G
        self.ac = 10           # ap
        self.level = 2         # L
        self.hp_plus = 2
        self.regen = 0
        self.num_att = 1       # ATT
        self.damage = 2        # WP
        self.dammod = 2        # WP
        self.hp = 1            # H
        self.armor = ""        # A$ or Ab
        self.weapon = ""       # W$ or Wb
        self.chi = 1           # CH
        self.food = 30         # Fo
        self.form = 1          # FORM (1-human, 2-ant, 3-bear)
        self.hpp = 5
        self.shield = False    # S

def char_decoder( data ):
    return_val=Player()
    return_val.name    =     data["name"    ]
    return_val.role    =     data["role"    ]
    return_val.gp      = int(data["gp"      ])
    return_val.ac      = int(data["ac"      ])
    return_val.level   = int(data["level"   ])
    return_val.hp_plus = int(data["hp_plus" ])
    return_val.regen   = int(data["regen"   ])
    return_val.num_att = int(data["num_att" ])
    return_val.damage  = int(data["damage"  ])
    return_val.dammod  = int(data["dammod"  ])
    return_val.hp      = int(data["hp"      ])
    return_val.armor   =     data["armor"   ]
    return_val.weapon  =     data["weapon"  ]
    return_val.chi     = int(data["chi"     ])
    return_val.food    = int(data["food"    ])
    return_val.form    =      data["form"   ]
    return_val.hpp     = int(data["hpp"     ])
    return_val.shield  =bool(data["shield"  ])
    return return_val


def maybe_int(x):
    try:
        return int(x)
    except:
        return None

def roll(n, d):
    t = 0
    for _ in range(n):
        t=t+random.randrange(d)+1
    return t

def Clear():
    """Clears screen."""
    if os.system('cls || clear') != 0:
        print('\n' * 100)

def Intro():
    # WIDTH 40,25
    Clear()
    # LOCATE 12,8
    for _ in range(12):
        print()
    print("        THE TARASQUE'S EVIL")
    for _ in range(11):
        print()
    #print("        [HIT ANY KEY TO CONTINUE]")
    input("        [PRESS ENTER TO CONTINUE]")
    #play song missing whole line

def Pause():
    time.sleep(1)

def Story():
    for _ in range(100):
        print()
    # Locate 25, 1
    print("THE EVIL TARASQUE HAS KIDNAPPED THE")
    Pause()
    print("PRINCESS IDA NOE. ON YOUR QUEST TO")
    Pause()
    print("SAVE HER YOU FOUND YOURSELF TRAPPED IN")
    Pause()
    print("A MAGICAL MAZE.  YOU ARE THE LAST")
    Pause()
    print("SERVANT OF THE KING LEFT TO SAVE THE")
    Pause()
    print("PRINCESS.  YOU MUST SUCCEED, AND YOU")
    Pause()
    print("FEEL THE END IS NEAR.")
    Pause()
    print("GOOD LUCK BRAVE SOUL.")
    for _ in range(15):
        #Pause()
        # if keypressed:
        #     return
        print()
    input("        [PRESS ENTER TO CONTINUE]")

def max_hp(u):
    # u.level * (u.hpp) + u.hp_plus
    return u.level * (u.hpp + u.hp_plus) + u.hpp

def gp_to_level(u):
    return 2**(u.level-1)*200

def level_up(u):
    # line 3
    u.level = min(100, u.level + 1)
    u.hp = u.hp + u.hpp + u.hp_plus
    print("YOU ARE LEVEL {}".format(u.level))
    if u.role == "FIGHTER":
        u.num_att = 1 + (u.level // 7)
    elif u.role == "MONK":
        u.num_att = 2 + (u.level // 7)
        u.ac=max(-10, 11-((u.level + 1) // 2))
        u.damage = 2 + (u.level // 2)

def new_char(name): # line 200
    you = Player()
    you.name = name
    print("CLASSES:")
    for cl in CLASSES:
        print("\t{}".format(cl))
    while you.role not in CLASSES:
        you.role = input("WHAT IS YOUR CLASS: ").upper()
    you.hpp = CLASSES[you.role][1]
    you.hp_plus = CLASSES[you.role][2]
    if you.role == "MAGE":
        you.gp = 10
        you.weapon="DAGGER"
        you.damage = 4
        you.ac = 8
        you.chi = 10
    elif you.role == "MONK":
        you.gp = 10
        you.weapon="MARTIAL ARTS"
        you.dammod = 5 # Fighter Strength + Specialization
        you.ac = 11 - you.level
        you.hp_plus = 3
    elif you.role == "PRIEST":
        you.gp = 10
        you.weapon="QUARTERSTAFF"
        you.damage = 6
        you.armor="HIDE"
        you.ac = 5
        you.chi = 5
    elif you.role == "THIEF":
        you.gp = 20
        you.armor="LEATHER"
        you.ac = 7
    elif you.role == "FIGHTER":
        you.gp = 250
        you.hp_plus = 3
        you.dammod = 5 # Fighter Strength + Specialization
    you.level = 1
    # level up to perform any level up cleanups
    level_up(you)
    you.hp = max_hp(you)
    return you

def shape_shift(u):
    form = None
    while form not in range(1,4) or form > (u.chi + 1) :
        form = maybe_int(input("1-HUMAN 2-ANT 3-BEAR: "))
    u.form = form
    u.chi = u.chi + 1 - form
    damage_taken = max_hp(u) - u.hp
    if form==1:
        print("YOU RETURN TO HUMAN FORM")
        u.weapon="QUARTERSTAFF"
        u.num_att = 1
        u.damage = 6
        u.dammod = 2
        u.armor="HIDE"
        u.ac = 5
        u.hpp = 6
        u.hp_plus = 4
        u.hp = max(1, max_hp(u) - damage_taken)
    elif form==2:
        print("YOU ARE NOW A TINY ANT")
        u.weapon="MANDIBLE"
        u.num_att = 1
        u.damage = 3
        u.dammod = -1
        u.ac = -11 - u.level
        u.hpp = 0
        u.hp_plus = 1
        u.hp = 1
    elif form==3:
        print("YOU ARE NOW A POWERFUL BEAR")
        u.weapon="TOOTH AND CLAW"
        u.num_att = 3
        u.damage = 8
        u.dammod = 3
        u.ac = 6
        u.hpp = 7
        u.hp_plus = 4
        u.hp = max_hp(u)

def fighter(u):
    mon = Monster()
    mon.name = "FIGHTER"
    mon.gp = gp_to_level(u) // 10 + gp_to_rest(u)
    mon.ac = 2
    mon.level = u.level
    mon.hp_plus = 5 + (2 * u.level)
    mon.damage = 8
    mon.dammod = 3
    mon.regen = 0
    mon.num_att = 1 + (u.level // 7)
    return mon


def load_char(): # line 70
    name = input("WHAT IS YOUR NAME: ")
    with open(os.path.join("saves",name+".json"), "r") as fin:
        return json.load(fin, object_hook=char_decoder)

def save_char(u):
    with open(os.path.join("saves",u.name+".json"), "w") as fout:
        json.dump(u.__dict__, fout)

def armorer(u): # line 42
    print( "WELCOME STRANGER" )
    A = 0
    while A != 4 or u.ac >= 10 or u.damage < 4:
        print("YOU HAVE {}Gp".format(u.gp))
        for i in range(5):
            print(f"{i+1}-{WEAPONS[i][0]:16} {WEAPONS[i][2]:-3}Gp   {i+1}-{ARMOR[i][0]:15} {ARMOR[i][2]:-5}Gp")
        A = maybe_int(input("1-WEAPON 2-ARMOR 3-SHIELD 10Gp 4-LEAVE: "))
        if A==1:
            if u.role=="PRIEST":
                print("PRIEST CAN ONLY USE THE QUARTERSTAFF")
            else:
                w = maybe_int(input("WHAT IS YOUR WEAPON: "))
                if 0 < w <=len(WEAPONS):
                    weapon = WEAPONS[w-1]
                    if u.gp >= weapon[2] and not (u.shield and weapon[3]):
                        u.weapon=weapon[0]
                        u.damage=weapon[1]
                        u.gp = u.gp - weapon[2]
                        # Add refund
                        print("{} PURCHASED".format(weapon[0]))
        elif A==2:
            if u.role=="THIEF":
                print("THIEF CAN ONLY WEAR LEATHER ARMOR")
            else:
                ar = maybe_int(input("WHAT IS YOUR ARMOR: "))
                if 0 < ar <= len(ARMOR):
                    armor = ARMOR[ar-1]
                    if u.gp >= armor[2]:
                        u.armor=armor[0]
                        u.ac=armor[1]
                        u.gp = u.gp - armor[2]
                        # Add refund
                        print("{} PURCHASED".format(armor[0]))
        elif A==3:
            if u.shield:
                u.shield = False
                u.gp=u.gp+10
                print("SHIELD SOLD")
            elif u.gp >= 10 and u.weapon != "TWO HANDED SWORD":
                u.shield = True
                u.gp=u.gp-10
                print("SHIELD PURCHASED")

def gp_to_rest(u):
    return u.level * 25

def char_ac(u):
    return u.ac-(1 if u.shield else 0)

def char_thac0(u):
    if u.role in ["FIGHTER", "MONK"]:
        # 1 better strength modifier, +1 Weapon Spec
        return 18 - (u.level // CLASSES[u.role][0])
    return 20 - (u.level // CLASSES[u.role][0])


def monster_getfilename( number ):
    return os.path.join("monsters",chr(63+number)+".mon.json")

def save_monsters():
    mon = Monster()
    a = 1
    while a==1:
        a = maybe_int(input("MONSTER NUMBER: "))
        mon.name = input("\tNAME: ")
        mon.gp = maybe_int(input("\tXp: "))
        mon.ac = maybe_int(input("\tAC: "))
        mon.level = maybe_int(input("\tHD: "))
        mon.hp_plus = maybe_int(input("\tHp+: "))
        mon.regen = maybe_int(input("\tREGENERATION: "))
        mon.num_att = maybe_int(input("\tATTACKS: "))
        mon.damage = maybe_int(input("\tDAMAGE: "))
        mon.dammod = maybe_int(input("\tDAMAGE PLUS: "))
        with open(monster_getfilename(a), "w") as fout:
            json.dump(mon.__dict__, fout)
        a = maybe_int(input("1-AGAIN: "))

def random_monster(u): #before line 12
    try:
        a = roll(1, min(10, u.level))
        #a = 2
        if 1 < a <= 10:
            with open(monster_getfilename(a), "r") as fin:
                return json.load(fin, object_hook=monster_decoder)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
    return None

def fireball(u, save):
    print(u.chi)
    a = -1
    while a<1 or a>u.chi or a>(u.level*2):
        a = maybe_int(input("HOW MANY CHARGES: "))
    u.chi = u.chi - a
    damage = roll( 6*a, 4)
    if save < 3:
        save = 3
    if roll(1,20) >= save:
        damage = damage / 2
    print("IT TAKES {} POINTS OF DAMAGE".format(damage))
    return damage

def fight(u):
    backstab_mod = 1 # BAK
    #Try reading a monster from a file
    mon = random_monster(u)
    if mon is None:
        mon = fighter(u)
    if mon.name[0] in 'aeiouAEIOU':
        print("YOU ARE ATTACKED BY AN {}".format(mon.name))
    else:
        print("YOU ARE ATTACKED BY A {}".format(mon.name))
    mon.hp = roll( mon.level, 8 ) + mon.hp_plus
    options = "1-ATTACK 2-RUN "
    if u.role=="MAGE":
        options += "3-MAGIC"
    if u.role=="PRIEST":
        options += "3-SHAPE SHIFT 4-TURN EVIL"
    if u.role=="THIEF":
        options += "3-SCROLL 4-BACKSTAB"
    while True:
        print(options)
        b = maybe_int(input(": "))
        if b==2:
            print("IT GETS A FINAL ATTACK")
        elif b==3 and u.role=="MAGE":
            if u.chi<1:
                print("YOU HAVE NO CHARGES. RECOVER ONE")
                u.chi = u.chi + 1
            else:
                # select a spell
                b = None
                while b not in range(1,5) :
                    b = maybe_int(input("1-FIREBALL 2-TELEPORT 3-STEALTH 4-SLEEP: "))
                u.chi = u.chi + 1 - b
                if b==1:
                    mon.hp -= fireball(u, 17 - mon.level)
                elif b==2:
                    print("YOU TELEPORT AWAY")
                    return True
                elif b==3:
                    print("YOU ARE HIDDEN")
                    backstab_mod = 2
                    continue # skip monster attacks you are hidden
                elif b==4:
                    save = 19 - mon.level
                    if roll(1,20) > save:
                        print("IT SAVES")
                    else:
                        mon.hp=0
        elif b==3 and u.role=="PRIEST":
            shape_shift(u)
            if u.form == 2:
                print("AS AN ANT YOU SNEAK AWAY")
                return True
        elif b==3 and u.role=="THIEF":
            if u.chi<1:
                print("YOU HAVE NO CHARGES")
            else:
                mon.hp -= fireball(u, 17 - mon.level)
        elif b==4 and u.role=="PRIEST":
            if u.form != 1:
                print("YOU MUST BE IN HUMAN FORM TO TURN EVIL")
            else:
                save = 19 - mon.level
                if roll(1,20) > save:
                    print("IT SAVES")
                else:
                    mon.hp=0
        elif b==4 and u.role=="THIEF":
            # line 80
            if roll(1,100) <= 10 + u.level * 5:
                print("YOU ARE HIDDEN")
                backstab_mod = 2 + ((u.level-1) // 4)
                continue # skip monster attacks you are hidden
        else:
            num_att = u.num_att
            if u.weapon=="DAGGER" and not u.shield:
                num_att = num_att + 1
            for _ in range(num_att):
                attack_roll = roll(1,20)
                if attack_roll < char_thac0(u) - mon.ac - backstab_mod:
                    print(f"{attack_roll:2}: YOU MISS")
                else:
                    if attack_roll == 20:
                        attack_roll = "!!! CRITCAL HIT !!!"
                        backstab_mod = backstab_mod + 1
                    dam_roll = (roll(1,u.damage) + u.dammod)*backstab_mod
                    backstab_mod = 1
                    print(f"{attack_roll:2}: YOU HIT FOR {dam_roll} POINTS OF DAMAGE")
                    mon.hp = mon.hp - dam_roll
        if mon.hp < 1:
            # line 16
            print ("IT HAS FALLEN. YOU WIN {} Gp".format(mon.gp))
            u.gp = u.gp + mon.gp
            u.food = u.food - 1
            return True
        mon.hp = mon.hp + mon.regen
        for _ in range(mon.num_att):
            attack_roll = roll(1,19)
            if attack_roll < 20 - mon.level - char_ac(u):
                print(f"{attack_roll:2}: IT MISSES")
            else:
                dam_roll = roll(1,mon.damage) + mon.dammod
                print(f"{attack_roll:2}: IT HITS FOR {dam_roll} POINTS OF DAMAGE")
                u.hp = u.hp - dam_roll
                if u.hp < 1:
                    # line 18
                    print ("{} MASTER OF THE {} HAS FALLEN".format( u.name, u.weapon))
                    return False
            if b == 2:
                print("YOU SURVIVED AND RUN AWAY")
                return True

def play(u): # line 5
    way_out =  roll(1,5) #B
    #way_out = 3
    if u.food < 1:
        print("YOU DIE OF STARVATION")
        return False
    if u.food < 5:
        print("YOU ARE RUNNING LOW ON RATIONS")
    print("THERE ARE 5 CAVES ONE LEADS TO FREEDOM THE REST LEAD TO BATTLE. PICK ONE:")
    print("\t0-CHARACTER")
    print("\t1-5-CAVES")
    if u.hp < max_hp(u):
        print("\t6-HEAL {}Gp".format(gp_to_rest(u)))
    if u.level < 100: # something about monks and level 17??
        print("\t7-ADVANCE {}Gp".format(gp_to_level(u)))
    print("\t8-FOOD 5Gp")
    if u.role in ["PRIEST",  "THIEF", "MAGE" ]:
        print("\t9-MAGIC, SHAPE SHIFT, SCROLLS 100Gp")
    if u.role in ["FIGHTER",  "THIEF" ]:
        print("\t10-ARMORER")
    if u.role == "PRIEST":
        print("\t10-SHAPE SHIFT")
    print("\t11-SAVE")
    a = maybe_int(input("CHOOSE: "))
    if a==way_out:
        print("YOU FOUND THE WAYOUT AND {}Gp".format(gp_to_level(u) // 5))
        u.gp = u.gp + (gp_to_level(u) // 5)
        a=maybe_int(input("1-BACK INTO CAVES 2-ALONG NEW PATH: "))
        if a==2:
            print_char(u)
            return False
    elif a==0:
        print_char(u)
    elif a==6:
        if u.gp >= gp_to_rest(u) and u.food > 2:
            # line 2
            u.gp = u.gp - gp_to_rest(u)
            u.food = u.food - 2
            if u.role in ["PRIEST", "MAGE"]:
                u.chi = u.chi + 1
            u.hp = max_hp(u)
            print("YOU REST AND HEAL UP TO {}".format(u.hp))
    elif a==7:
        if u.gp >= gp_to_level(u) and u.food > 1:
            u.gp = u.gp - gp_to_level(u)
            u.food = u.food - 1
            level_up(u)
    elif a==8:
        if u.gp >= 5:
            u.gp = u.gp - 5
            u.food = u.food + 1
            print("FOOD={}".format(u.food))
    elif a==9:
        if u.gp >= 100 and u.role!="FIGHTER":
            u.gp = u.gp - 100
            u.chi = u.chi + 1
            print("MAGICAL ENERGY={}".format(u.chi))
    elif a==10:
        if u.role=="PRIEST":
            shape_shift(u)
        elif u.role in ["FIGHTER",  "THIEF" ]:
            armorer(u)
    elif a==11:
        save_char(u)
    elif a in range(1,6):
        return fight(u)
    return True

def print_char( u ): # line 1
    print("\n\n")
    print(u.name)
    print(u.role)
    if u.role in ["FIGHTER", "MONK"]:
        print("STR 18/70              LEVEL={}".format(u.level))
    else:
        print("STR 18                 LEVEL={}".format(u.level))
    print("DEX 15                    AC={}".format(char_ac(u)))
    print("CON 17                    HP={}/{}".format(u.hp, max_hp(u)))
    print("INT 14                 Thac0={}".format(21-u.level))
    print("WIS 13                    GP={}".format(u.gp))
    print("CHA 15        MAGICAL ENERGY={}".format(u.chi))
    if u.form != 1:
        print(f"\t{u.weapon} ({u.dammod+1}-{u.dammod+u.damage})")
    else:
        print("EQUIPMENT:")
        if u.weapon != "":
            print(f"\t{u.weapon} ({u.dammod+1}-{u.dammod+u.damage})")
        if u.armor != "":
            print("\t{}".format(u.armor))
        if u.shield:
            print("\tSHIELD")
        print("\tBACKPACK")
        if u.role == "MAGE":
            print("\tSPELL BOOK")
        if u.role == "PRIEST":
            print("\tHOLY SYMBOL")
        if u.role == "THIEF":
            print("\tTHIEVES TOOLS")
        print("\tLANTERN")
        print("\t{} FOOD RATIONS".format(u.food))
        print("\t50' ROPE")

def main():
    Intro()
    #Story()
    a=0
    while a!=2:
        Clear()
        name = input("WHAT IS YOUR NAME (NO SPACES)(TYPE 'LOAD' TO GET SAVED GAME): ")
        if name == "LOAD":
            you = load_char()
        elif name == "MONSTER":
            return save_monsters()
        else:
            you = new_char(name)
        if you.role in ["FIGHTER",  "THIEF" ]:
            armorer(you)
        while play(you):
            pass
        print_char(you)
        a = maybe_int(input("1-AGAIN 2-END: ")) # line 20

if __name__=="__main__":
    main()
