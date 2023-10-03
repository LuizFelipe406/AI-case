# high = 7-10
# medium = 4-6
# low = 1-3

rpg_roles = """
Warrior: {
	name: user_input + last name
  attack: choose a random number between 4 and 6
	life: choose a random number between  30 and 40
	defense: choose a random number between  4 and 6
	lucky: choose a random number between  1 and 3
},
Mage: {
	name: user_input + last name
	attack: choose a random number between  7 and 10
	life: choose a random number between  25 and 30
	defense: choose a random number between  1 and 3
	lucky: choose a random number between  4 and 6
},
Assassin: {
	name: user_input + last name
	attack: choose a random number between  7 and 10
	life: choose a random number between  23 and 28
	defense: choose a random number between 4 and 6
	lucky: choose a random number between  4 and 6
},
Healer: {
	name: user_input + last name
	heal: choose a random number between  4 and 6
	life: choose a random number between  25 and 30
	defense: choose a random number between  1 and 3
	lucky: choose a random number between  7 and 10
}
"""

rpg_boss = """
Boss: {
	type: generate a boss type
	name: generate a name based on the boss type
	life: random number between 50 and 60
	attack: random number between 4 and 6
	defense: random number between 4 and 6
	lucky: random number between 1 and 3
}
"""