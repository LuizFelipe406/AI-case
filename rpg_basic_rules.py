# high = 7-10
# medium = 4-6
# low = 1-3

rpg_roles = """
Warrior: {
	role: Warrior
	name: user_input + last name
  attack: choose a random number between 4 and 6
	life: choose a random number between  30 and 40
	defense: choose a random number between  4 and 6
	lucky: choose a random number between  1 and 3
},
Mage: {
	role: Mage
	name: user_input + last name
	attack: choose a random number between  7 and 10
	life: choose a random number between  25 and 30
	defense: choose a random number between  1 and 3
	lucky: choose a random number between  4 and 6
},
Assassin: {
	role: Assassin
	name: user_input + last name
	attack: choose a random number between  7 and 10
	life: choose a random number between  23 and 28
	defense: choose a random number between 4 and 6
	lucky: choose a random number between  4 and 6
},
Healer: {
	role: Healer
	name: user_input + last name
	heal: choose a random number between  4 and 6
	life: choose a random number between  25 and 30
	defense: choose a random number between  1 and 3
	lucky: choose a random number between  7 and 10
}
"""

rpg_boss = """
Boss: {
	role: Boss
	type: generate a boss type
	name: generate a name based on the boss type
	life: random number between 80 and 100
	attack: random number between 4 and 6
	defense: random number between 4 and 6
	lucky: random number between 1 and 3
}
"""