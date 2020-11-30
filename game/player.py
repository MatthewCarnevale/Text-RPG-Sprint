"""
    Container for player stats
"""
import random


class Player:
    """ Class for player stats and data """

    def __init__(self):
        self.id = "name"
        # stats
        # Strength: Used for slapping and stronging things
        self.strength = 0
        # Dexterity: Used for going fast and being fast
        self.dex = 0
        # Constitution: Healthiness and not-die ability
        self.con = 0
        # Intelligence: The BIG BRAIN
        self.intel = 0
        # Charisma: How likeable or punchable you are
        self.cha = 0
        # Luck: Lucky you, huh?
        self.luk = 0
        # totals
        # Health: Your life.
        self.max_health = 100 + self.con * 10
        self.health = self.max_health
        # Mana: Magic is a thing?
        self.max_mana = self.intel * 5
        self.mana = 0
        # money
        self.money = self.luk * 5
        self.gen = "gender"
        self.character_class = "class"
        self.checkpoint = "start"

    def attack(self, type, target):
        """ Attack the target """
        if type == "melee":
            crit_state = self.luk < random.randrange(1, 100)  # Is this hit a crit?
            crit_mult = 1.00  # The critical damage multiplier
            if crit_state:
                crit_mult = 2.00
            expected_damage = self.str * crit_mult
            return target.damage(expected_damage, self)
        if type == "ranged":
            crit_state = self.luk < random.randrange(1, 100)  # Is this hit a crit?
            crit_mult = 1.00  # The critical damage multiplier
            if crit_state:
                crit_mult = 2.00
            expected_damage = self.dex * crit_mult
            return target.damage(expected_damage, self)
        if type == "magic":
            crit_state = self.luk < random.randrange(1, 100)  # Is this hit a crit?
            crit_mult = 1.00  # The critical damage multiplier
            if crit_state:
                crit_mult = 2.00
            expected_damage = self.int * crit_mult
            return target.damage(expected_damage, self)

    def is_dead(self):
        """ Has the player died? """
        return self.health <= 0

    def damage(self, dmg_rcv, target_rcv=None):
        """ Player receives damage """
        self.health -= dmg_rcv
        from_string = ""
        if target_rcv:
            from_string = " from " + target_rcv.id
        if self.is_dead():  # if attack causes death
            return (
                self.id + " has " + str(self.health) + " health and has died.",
                "death",
            )
        # otherwise
        return (
            self.id
            + " took "
            + str(dmg_rcv)
            + " damage"
            + from_string
            + " and is now at "
            + str(self.health)
            + "/"
            + str(self.max_health)
            + ".",
            "damage",
        )

    def make_neet(self):
        """ Create 'neet' archetype character. """
        # Strength: Used for slapping and stronging things
        self.strength = 65
        # Dexterity: Used for going fast and being fast
        self.dex = 80
        # Constitution: Healthiness and not-die ability
        self.con = 50
        # Intelligence: The BIG BRAIN
        self.intel = 75
        # Charisma: How likeable or punchable you are
        self.cha = 70
        # Luck: Lucky you, huh?
        self.luk = 50
        # totals
        # Health: Your life.
        self.max_health = 100 + self.con * 10
        self.health = self.max_health
        # Mana: Magic is a thing?
        self.max_mana = self.intel * 5
        # money
        self.money = self.luk * 5

    def make_bookworm(self):
        """ Create 'bookworm' archetype character. """
        # Strength: Used for slapping and stronging things
        self.strength = 35
        # Dexterity: Used for going fast and being fast
        self.dex = 75
        # Constitution: Healthiness and not-die ability
        self.con = 80
        # Intelligence: The BIG BRAIN
        self.intel = 90
        # Charisma: How likeable or punchable you are
        self.cha = 25
        # Luck: Lucky you, huh?
        self.luk = 60
        # totals
        # Health: Your life.
        self.max_health = 100 + self.con * 10
        self.health = self.max_health
        # Mana: Magic is a thing?
        self.max_mana = self.intel * 5
        # money
        self.money = self.luk * 5

    def make_jock(self):
        """ Create 'jock' archetype character. """
        # Strength: Used for slapping and stronging things
        self.strength = 90
        # Dexterity: Used for going fast and being fast
        self.dex = 40
        # Constitution: Healthiness and not-die ability
        self.con = 20
        # Intelligence: The BIG BRAIN
        self.intel = 35
        # Charisma: How likeable or punchable you are
        self.cha = 50
        # Luck: Lucky you, huh?
        self.luk = 50
        # totals
        # Health: Your life.
        self.max_health = 100 + self.con * 10
        self.health = self.max_health
        # Mana: Magic is a thing?
        self.max_mana = self.intel * 5
        # money
        self.money = self.luk * 5
