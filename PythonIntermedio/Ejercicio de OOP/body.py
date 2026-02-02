class Head:
    def __init__(self):
        pass


class Hand:
    def __init__(self):
        pass


class Arm:
    def __init__(self, hand):
        self.hand = hand


class Feet:
    def __init__(self):
        pass


class Leg:
    def __init__(self, feet):
        self.feet = feet


class Torso:
    def __init__(self, head, right_arm, left_arm):
        self.head = head
        self.right_arm = right_arm
        self.left_arm = left_arm


class Human:
    def __init__(self, head, torso, right_leg, left_leg):
        self.head = head
        self.torso = torso
        self.right_leg = right_leg
        self.left_leg = left_leg
    

    # Manos
right_hand = Hand()
left_hand = Hand()

# Brazos
right_arm = Arm(right_hand)
left_arm = Arm(left_hand)

# Cabeza
head = Head()

# Torso
torso = Torso(head, right_arm, left_arm)

# Pies
right_feet = Feet()
left_feet = Feet()

# Piernas
right_leg = Leg(right_feet)
left_leg = Leg(left_feet)

# Humano
human = Human(head, torso, right_leg, left_leg)