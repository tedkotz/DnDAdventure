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

class Monster:
    def __init__(self):
        self.name = ""  # Mb
        self.xp= 0      # K
        self.ac = 0     # AC
        self.hd = 0     # HD
        self.hp_plus= 0 # P
        self.damage= 0  # D
        self.dammod = 0 # Dp
        self.regen= 0   # R
        self.num_att= 0 # MA

class Player:
    def __init__(self):
        self.name = ""         # N$
        self.clas = ""         # C$
        self.weapon = ""       # W$ or Wb
        self.armor = ""        # A$ or Ab
        self.level = 2         # L
        self.co = 1
        self.hpp = 5
        self.food = 30         # Fo
        self.gp = 700          # G
        self.hp = 1            #H
        self.chi = 1           #CH
        self.shield = False    # S
        self.armor_power = -5  # ap
        self.weapon_power = -8 # WP
        self.form = 1          # FORM (1-human, 2-ant, 3-bear)


CLASSES = { "FIGHTER"       : (1   , 5),
            "PRIEST"        : (1.25, 4),
            "MONK": (1.5 , 3),
            "THIEF"         : (1.75, 3),
            "MAGE"          : (2   , 2) }

WEAPONS = [ ("DAGGER"          , -4,  3, False),
            ("QUARTERSTAFF"    , -2,  6, True ),
            ("BATTLE AX"       ,  0, 12, False),
            ("LONG SWORD"      ,  2, 24, False),
            ("TWO HANDED SWORD",  4, 48, True ) ]


ARMOR = [ ("CHAINMAIL"       ,  3,   75),
          ("BRONZEPLATEMAIL" ,  2,  400),
          ("PLATEMAIL"       ,  1, 1000),
          ("FIELD PLATEMAIL" ,  0, 2000),
          ("FULL PLATEMAIL"  , -1, 7000) ]

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

def new_char(name): # line 200
    you = Player()
    you.name = name
    print("CLASSES:")
    for cl in CLASSES:
        print("\t{}".format(cl))
    while you.clas not in CLASSES:
        you.clas = input("WHAT IS YOUR CLASS: ").upper()
    you.co=CLASSES[you.clas][0]
    you.hpp=CLASSES[you.clas][1]
    you.hp = max_hp(you)
    if you.clas == "MAGE":
        you.weapon="DAGGER"
        you.weapon_power = -4
        you.armor_power = 8
        you.gp = 600
        you.chi = 10
    elif you.clas == "MONK":
        you.weapon="MARTIAL ARTS"
        you.weapon_power = you.level - 5
        you.armor_power = 11 - you.level
        you.gp = 600
    elif you.clas == "PRIEST":
        you.weapon="QUARTERSTAFF"
        you.armor="HIDE"
        you.weapon_power = -2
        you.armor_power = 6
        you.chi = 5
    elif you.clas == "THIEF":
        you.armor="LEATHER"
        you.armor_power = 8
    return you

def char_decoder( d ):
    return_val=Player()
    return_val.name         = d["name"         ]
    return_val.clas         = d["clas"         ]
    return_val.weapon       = d["weapon"       ]
    return_val.armor        = d["armor"        ]
    return_val.level        = d["level"        ]
    return_val.co           = d["co"           ]
    return_val.hpp          = d["hpp"          ]
    return_val.food         = d["food"         ]
    return_val.gp           = d["gp"           ]
    return_val.hp           = d["hp"           ]
    return_val.chi          = d["chi"          ]
    return_val.shield       = d["shield"       ]
    return_val.armor_power  = d["armor_power"  ]
    return_val.weapon_power = d["weapon_power" ]
    return_val.form         = d["form"         ]
    return return_val

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
    while A != 4 or u.armor_power < -3 or u.weapon_power < -6:
        print("YOU HAVE {}Gp".format(u.gp))
        print("1-DAGGER             3Gp   1-CHAINMAIL          75Gp")
        print("2-QUARTERSTAFF       6Gp   2-BRONZEPLATEMAIL   400Gp")
        print("3-BATTLE AX         12Gp   3-PLATEMAIL        1000Gp")
        print("4-LONG SWORD        24Gp   4-FIELD PLATEMAIL  2000Gp")
        print("5-TWO HANDED SWORD  48Gp   5-FULL PLATEMAIL   7000Gp")
        A = maybe_int(input("1-WEAPON 2-ARMOR 3-SHIELD 10Gp 4-LEAVE: "))
        if A==1:
            if u.clas=="PRIEST":
                print("PRIEST CAN ONLY USE THE QUARTERSTAFF")
            else:
                w = maybe_int(input("WHAT IS YOUR WEAPON: "))
                if 0 < w <=len(WEAPONS):
                    weapon = WEAPONS[w-1]
                    if u.gp >= weapon[2] and not (u.shield and weapon[3]):
                        u.weapon=weapon[0]
                        u.weapon_power=weapon[1]
                        u.gp = u.gp - weapon[2]
                        # Add refund
                        print("{} PURCHASED".format(weapon[0]))
        elif A==2:
            if u.clas=="THIEF":
                print("THIEF CAN ONLY WEAR LEATHER ARMOR")
            else:
                ar = maybe_int(input("WHAT IS YOUR ARMOR: "))
                if 0 < ar <= len(ARMOR):
                    armor = ARMOR[ar-1]
                    if u.gp >= armor[2]:
                        u.armor=armor[0]
                        u.armor_power=armor[1]
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

def max_hp(u):
    return u.level * (u.hpp + 3) + u.hpp

def gp_to_level(u):
    return 2**(u.level-1)*200

def gp_to_rest(u):
    return u.level * 25

def char_ac(u):
    return u.armor_power-(1 if u.shield else 0)

def monster_getfilename( number ):
    return os.path.join("monsters",chr(63+number)+".mon.json")

def monster_decoder( data ):
    return_val = Monster()
    return_val.name    =     data["name"    ]
    return_val.xp      = int(data["xp"      ])
    return_val.ac      = int(data["ac"      ])
    return_val.hd      = int(data["hd"      ])
    return_val.hp_plus = int(data["hp_plus" ])
    return_val.damage  = int(data["damage"  ])
    return_val.dammod  = int(data["dammod"  ])
    return_val.regen   = int(data["regen"   ])
    return_val.num_att = int(data["num_att" ])
    return return_val


def save_monsters():
    mon = Monster()
    a = 1
    while a==1:
        a = maybe_int(input("MONSTER NUMBER: "))
        mon.name = input("\tNAME: ")
        mon.xp = maybe_int(input("\tXp: "))
        mon.ac = maybe_int(input("\tAC: "))
        mon.hd = maybe_int(input("\tHD: "))
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

def fighter(u):
    mon = Monster()
    mon.name = "FIGHTER"
    mon.xp = gp_to_level(u) // 10 + gp_to_rest(u)
    mon.ac = 2
    mon.hd = u.level
    mon.hp_plus = 5
    mon.damage = 8
    mon.dammod = 7
    mon.regen = 0
    mon.num_att = 1
    return mon

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
        u.armor="HIDE"
        u.weapon_power = -2
        u.armor_power = 6
        u.hpp = 4
        u.hp = max(1, max_hp(u) - damage_taken)
    elif form==2:
        print("YOU ARE NOW A TINY ANT")
        u.weapon="MANDIBLE"
        u.weapon_power = -8
        u.armor_power = -20
        u.hpp = 0
        u.hp = 1
    elif form==3:
        print("YOU ARE NOW A POWERFUL BEAR")
        u.weapon="TOOTH AND CLAW"
        u.weapon_power = -4
        u.armor_power = 7
        u.hpp = 6
        damage_taken = 0
        u.hp = max_hp(u)

def level_up(u):
    # line 3
    u.level = min(100, u.level + 1)
    u.food = u.food - 1
    print("YOU ADVANCE TO {}".format(u.level))
    if u.clas == "MONK":
        u.armor_power=max(-10, 11-u.level)
        u.weapon_power = u.level - 5

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
    mon_hp = roll( mon.hd, 8 ) + mon.hp_plus
    options = "1-ATTACK 2-RUN "
    if u.clas=="MAGE":
        options += "3-MAGIC"
    if u.clas=="PRIEST":
        options += "3-SHAPE SHIFT 4-TURN EVIL"
    if u.clas=="THIEF":
        options += "3-SCROLL 4-BACKSTAB"
    while True:
        print(options)
        b = maybe_int(input(": "))
        if b==2:
            print("IT GETS A FINAL ATTACK")
        elif b==3 and u.clas=="MAGE":
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
                    mon_hp -= fireball(u, 17 - mon.hd)
                elif b==2:
                    print("YOU TELEPORT AWAY")
                    return True
                elif b==3:
                    print("YOU ARE HIDDEN")
                    backstab_mod = 1 + u.level // 4
                    continue # skip monster attacks you are hidden
                elif b==4:
                    save = 19 - mon.hd
                    if roll(1,20) > save:
                        print("IT SAVES")
                    else:
                        mon_hp=0
        elif b==3 and u.clas=="PRIEST":
            shape_shift(u)
            if u.form == 2:
                print("AS AN ANT YOU SNEAK AWAY")
                return True
        elif b==3 and u.clas=="THIEF":
            if u.chi<1:
                print("YOU HAVE NO CHARGES")
            else:
                mon_hp -= fireball(u, 17 - mon.hd)
        elif b==4 and u.clas=="PRIEST":
            if u.form != 1:
                print("YOU MUST BE IN HUMAN FORM TO TURN EVIL")
            else:
                save = 19 - mon.hd
                if roll(1,20) > save:
                    print("IT SAVES")
                else:
                    mon_hp=0
        elif b==4 and u.clas=="THIEF":
            # line 80
            if roll(1,100) <= 10 + u.level * 5:
                print("YOU ARE HIDDEN")
                backstab_mod = 1 + u.level // 4
                continue # skip monster attacks you are hidden
        else:
            num_att = 1
            if u.clas=="FIGHTER":
                num_att = 1 + (u.level // 10)
            if u.clas=="MONK":
                num_att = 1 + (u.level // 5)
            if u.weapon=="DAGGER":
                num_att = num_att * 2
            if u.form==3:
                num_att = 3
            for _ in range(num_att):
                attack_roll = roll(1,20) + 5 + backstab_mod
                if attack_roll < 21 - (u.level/u.co) - mon.ac:
                    print("YOU MISS")
                else:
                    dam_roll = (roll(1,8+u.weapon_power)+7)*backstab_mod
                    backstab_mod = 1
                    print("YOU HIT FOR {} POINTS OF DAMAGE".format(dam_roll))
                    mon_hp = mon_hp - dam_roll
        if mon_hp < 1:
            # line 16
            print ("IT HAS FALLEN. YOU WIN {} Gp".format(mon.xp))
            u.gp = u.gp + mon.xp
            u.food = u.food - 1
            return True
        mon_hp = mon_hp + mon.regen
        for _ in range(mon.num_att):
            attack_roll = roll(1,20)
            if attack_roll < 21 - mon.hd - char_ac(u):
                print("IT MISSES")
            else:
                dam_roll = roll(1,mon.damage) + mon.dammod
                print("IT HITS FOR {} POINTS OF DAMAGE".format(dam_roll))
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
    if u.clas in ["PRIEST",  "THIEF", "MAGE" ]:
        print("\t9-MAGIC, SHAPE SHIFT, SCROLLS 100Gp")
    if u.clas in ["FIGHTER",  "THIEF" ]:
        print("\t10-ARMORER")
    if u.clas == "PRIEST":
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
            if u.clas in ["PRIEST", "MAGE"]:
                u.chi = u.chi + 1
            u.hp = max_hp(u)
            print("YOU REST AND HEAL UP TO {}".format(u.hp))
    elif a==7:
        if u.gp >= gp_to_level(u) and u.food > 1:
            u.gp = u.gp - gp_to_level(u)
            level_up(u)
    elif a==8:
        if u.gp >= 5:
            u.gp = u.gp - 5
            u.food = u.food + 1
            print("FOOD={}".format(u.food))
    elif a==9:
        if u.gp >= 100 and u.clas!="FIGHTER":
            u.gp = u.gp - 100
            u.chi = u.chi + 1
            print("MAGICAL ENERGY={}".format(u.chi))
    elif a==10:
        if u.clas=="PRIEST":
            shape_shift(u)
        elif u.clas in ["FIGHTER",  "THIEF" ]:
            armorer(u)
    elif a==11:
        save_char(u)
    elif a in range(1,6):
        return fight(u)
    return True

def print_char( u ): # line 1
    print("\n\n")
    print(u.name)
    print(u.clas)
    print("STR 18/00              LEVEL={}".format(u.level))
    print("DEX 15                    AC={}".format(char_ac(u)))
    print("CON 17                    HP={}/{}".format(u.hp, max_hp(u)))
    print("INT 14                 Thac0={}".format(21-u.level))
    print("WIS 13                    GP={}".format(u.gp))
    print("CHA 15        MAGICAL ENERGY={}".format(u.chi))
    print("EQUIPMENT:")
    if u.weapon != "":
        print("\t{} (8-{})".format(u.weapon, 15+u.weapon_power))
    if u.armor != "":
        print("\t{}".format(u.armor))
    if u.shield:
        print("\tSHIELD")
    print("\tBACKPACK")
    if u.clas == "MAGE":
        print("\tSPELL BOOK")
    if u.clas == "PRIEST":
        print("\tHOLY SYMBOL")
    if u.clas == "THIEF":
        print("\tTHIEVES TOOLS")
    print("\tLANTERN")
    print("\t{} FOOD RATIONS".format(u.food))
    print("\t50' ROPE")

def main():
    a=0
    while a!=2:
        Intro()
        #Story()
        Clear()
        name = input("WHAT IS YOUR NAME (NO SPACES)(TYPE 'LOAD' TO GET SAVED GAME): ")
        if name == "LOAD":
            you = load_char()
        elif name == "MONSTER":
            return save_monsters()
        else:
            you = new_char(name)
        if you.clas in ["FIGHTER",  "THIEF" ]:
            armorer(you)
        while play(you):
            pass
        a = maybe_int(input("1-AGAIN 2-END: ")) # line 20

if __name__=="__main__":
    main()
