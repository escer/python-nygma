# -*- coding: utf-8 -*-

import string
import random

"""Python implementation of Enigma encryption/decryption algorithm"""


class Rotor(object):

    def __init__(self, permutation, cycle_points, moveable):
        self.permutation = permutation
        self.code_to_position = {}
        for i, n in enumerate(permutation):
            self.code_to_position[n] = i
        self.length = len(permutation)
        self.cycle_points = cycle_points
        self.moveable = moveable
        self.current_cycle = 0

    def forward(self, code):
        return self.get_code_at(code)

    def backward(self, code):
        return self.get_position_of(code)

    def get_code_at(self, position):
        computed_position = (position + self.current_cycle) % self.length
        return self.permutation[computed_position]

    def get_position_of(self, code):
        value = self.code_to_position[code]
        return (value - self.current_cycle) % self.length

    def move(self, go):
        if go:
            self.current_cycle += 1
        return self.moveable and self.get_code_at(0) in self.cycle_points

    def reset(self):
        self.current_cycle = 0


class Reflector(object):

    def __init__(self, pairs):
        self._map = {}
        for a, b in pairs:
            self._map[a] = b
            self._map[b] = a

    def reflect(self, code):
        return self._map[code]


class Plugboard(object):

    def __init__(self, pairs):
        self._map = {}
        for a, b in pairs:
            self._map[a] = b
            self._map[b] = a

    def switch(self, code):
        if code in self._map:
            return self._map[code]
        else:
            return code


class Enigma(object):

    rotor_class = Rotor
    reflector_class = Reflector
    plugboard_class = Plugboard

    alphabet = list(string.uppercase)

    config = None

    @classmethod
    def get_config(cls, num_rotors=3, num_plugs=None, seed=None):
        alphabet_len = len(cls.alphabet)
        numbers = range(alphabet_len)
        rand = random.Random(seed)
        # rotors
        rotors = []
        for i in range(num_rotors):
            cycle_points = (rand.choice(numbers),)
            permutation = numbers[:]
            rand.shuffle(permutation)
            rotors.append({
                'permutation': permutation,
                'cycle_points': cycle_points,
                'moveable': True
            })
        # plugboard
        num_plugs = num_plugs or rand.randint(1, alphabet_len / 2)
        plugged_signs = rand.sample(numbers, num_plugs * 2)
        plugboard = []
        current_plug = []
        for i, ps in enumerate(plugged_signs):
            current_plug.append(ps)
            if i % 2:
                plugboard.append(current_plug)
                current_plug = []
        # reflector
        reflector_signs = numbers[:]
        rand.shuffle(reflector_signs)
        reflector = []
        current_pair = []
        for i, rs in enumerate(reflector_signs):
            current_pair.append(rs)
            if i % 2:
                reflector.append(current_pair)
                current_pair = []
        return {
            'rotors': rotors, 'reflector': reflector, 'plugboard': plugboard
        }

    def __init__(self, config=None, **config_kwargs):
        self.config = config or self.config or self.get_config(**config_kwargs)
        self.char_to_number = {}
        for i, char in enumerate(self.alphabet):
            self.char_to_number[char] = i
        self.rotors = [
            self.rotor_class(**kwargs) for kwargs in self.config['rotors']
        ]
        self.reflector = self.reflector_class(self.config['reflector'])
        self.plugboard = self.plugboard_class(self.config['plugboard'])

    def code(self, message):
        result = ''
        for ch in message:
            self.move_rotors()
            n = self.char_to_number[ch]
            n = self.plugboard.switch(n)
            for rotor in self.rotors:
                n = rotor.forward(n)
            n = self.reflector.reflect(n)
            for rotor in reversed(self.rotors):
                n = rotor.backward(n)
            n = self.plugboard.switch(n)
            new_ch = self.alphabet[n]
            result += new_ch
        return result

    def reset(self):
        for rotor in self.rotors:
            rotor.reset()

    def move_rotors(self):
        go = True
        for rotor in self.rotors:
            go = rotor.move(go)


class ClassicEnigma(Enigma):

    REFLECTOR_B = [
        (0, 24),
        (1, 17),
        (2, 20),
        (3, 7),
        (4, 16),
        (5, 18),
        (6, 11),
        (8, 15),
        (9, 23),
        (10, 13),
        (12, 14),
        (19, 25),
        (21, 22)
    ]
    REFLECTOR_C = [
        (0, 5),
        (1, 21),
        (2, 15),
        (3, 9),
        (4, 8),
        (6, 14),
        (7, 24),
        (10, 17),
        (11, 25),
        (12, 23),
        (13, 22),
        (16, 19),
        (18, 20)
    ]

    ROTOR_I = {
        'permutation': [
            4, 10, 12, 5, 11, 6, 3, 16, 21, 25, 13, 19, 14,
            22, 24, 7, 23, 20, 18, 15, 0, 8, 1, 17, 2, 9
        ],
        'cycle_points': (17,),
        'moveable': True
    }
    ROTOR_II = {
        'permutation': [
            0, 9, 3, 10, 18, 8, 17, 20, 23, 1, 11, 7, 22, 19,
            12, 2, 16, 6, 25, 13, 15, 24, 5, 21, 14, 4
        ],
        'cycle_points': (5,),
        'moveable': True
    }
    ROTOR_III = {
        'permutation': [
            1, 3, 5, 7, 9, 11, 2, 15, 17, 19, 23, 21, 25, 13,
            24, 4, 8, 22, 6, 0, 10, 12, 20, 18, 16, 14
        ],
        'cycle_points': (22,),
        'moveable': True
    }
    ROTOR_IV = {
        'permutation': [
            4, 18, 14, 21, 15, 25, 9, 0, 24, 16, 20, 8, 17, 7,
            23, 11, 13, 5, 19, 6, 10, 3, 2, 12, 22, 1
        ],
        'cycle_points': (10,),
        'moveable': True
    }
    ROTOR_V = {
        'permutation': [
            21, 25, 1, 17, 6, 8, 19, 24, 20, 15, 18, 3, 13, 7,
            11, 23, 0, 22, 12, 9, 16, 14, 5, 4, 2, 10
        ],
        'cycle_points': (0,),
        'moveable': True
    }

    @classmethod
    def get_config(cls, num_plugs=None, seed=None):
        rand = random.Random(seed)
        rotors = rand.sample(
            (cls.ROTOR_I, cls.ROTOR_II, cls.ROTOR_III, cls.ROTOR_IV,
             cls.ROTOR_V), 3
        )
        reflector = rand.choice((cls.REFLECTOR_B, cls.REFLECTOR_C))
        # plugboard
        alphabet_len = len(cls.alphabet)
        numbers = range(alphabet_len)
        num_plugs = num_plugs or rand.randint(1, alphabet_len / 2)
        plugged_signs = rand.sample(numbers, num_plugs * 2)
        plugboard = []
        current_plug = []
        for i, ps in enumerate(plugged_signs):
            current_plug.append(ps)
            if i % 2:
                plugboard.append(current_plug)
                current_plug = []
        return {
            'rotors': rotors, 'reflector': reflector, 'plugboard': plugboard
        }


class M4ClassicEnigma(ClassicEnigma):

    REFLECTOR_B = [
        (0, 4),
        (1, 13),
        (2, 10),
        (3, 16),
        (5, 20),
        (6, 24),
        (7, 22),
        (8, 9),
        (11, 14),
        (12, 15),
        (17, 23),
        (18, 25),
        (19, 21)
    ]
    REFLECTOR_C = [
        (0, 17),
        (1, 3),
        (2, 14),
        (4, 9),
        (5, 13),
        (6, 19),
        (7, 10),
        (8, 21),
        (11, 12),
        (15, 22),
        (16, 25),
        (18, 23),
        (20, 24)
    ]

    ROTOR_VI = {
        'permutation': [
            9, 15, 6, 21, 14, 20, 12, 5, 24, 16, 1, 4, 13, 7,
            25, 17, 3, 10, 0, 18, 23, 11, 8, 2, 19, 22
        ],
        'cycle_points': (0, 13),
        'moveable': True
    }
    ROTOR_VII = {
        'permutation': [
            13, 25, 9, 7, 6, 17, 2, 23, 12, 24, 18, 22, 1, 14,
            20, 5, 0, 8, 21, 11, 15, 4, 10, 16, 3, 19
        ],
        'cycle_points': (0, 13),
        'moveable': True
    }
    ROTOR_VIII = {
        'permutation': [
            5, 10, 16, 7, 19, 11, 23, 14, 2, 1, 9, 18, 15, 3,
            25, 17, 0, 12, 4, 22, 13, 8, 20, 24, 6, 21
        ],
        'cycle_points': (0, 13),
        'moveable': True
    }
    ROTOR_BETA = {
        'permutation': [
            11, 4, 24, 9, 21, 2, 13, 8, 23, 22, 15, 1, 16, 12,
            3, 17, 19, 0, 10, 25, 6, 5, 20, 7, 14, 18
        ],
        'cycle_points': (0, 13),
        'moveable': False
    }
    ROTOR_GAMMA = {
        'permutation': [
            5, 18, 14, 10, 0, 13, 20, 4, 17, 7, 12, 1, 19, 8,
            24, 2, 22, 11, 16, 15, 25, 23, 21, 6, 9, 3
        ],
        'cycle_points': (0, 13),
        'moveable': False
    }

    @classmethod
    def get_config(cls, num_plugs=None, seed=None):
        rand = random.Random(seed)
        rotors = rand.sample(
            (cls.ROTOR_I, cls.ROTOR_II, cls.ROTOR_III, cls.ROTOR_IV,
             cls.ROTOR_V, cls.ROTOR_VI, cls.ROTOR_VII, cls.ROTOR_VIII), 3
        ) + [rand.choice((cls.ROTOR_BETA, cls.ROTOR_GAMMA))]
        reflector = rand.choice((cls.REFLECTOR_B, cls.REFLECTOR_C))
        # plugboard
        alphabet_len = len(cls.alphabet)
        numbers = range(alphabet_len)
        num_plugs = num_plugs or rand.randint(1, alphabet_len / 2)
        plugged_signs = rand.sample(numbers, num_plugs * 2)
        plugboard = []
        current_plug = []
        for i, ps in enumerate(plugged_signs):
            current_plug.append(ps)
            if i % 2:
                plugboard.append(current_plug)
                current_plug = []
        return {
            'rotors': rotors, 'reflector': reflector, 'plugboard': plugboard
        }


class Base64Enigma(Enigma):

    alphabet = list(string.ascii_letters + string.digits + '_-+=')


if __name__ == '__main__':
    import base64, json

    print('\n* Classic Enigma: *')
    classic_enigma = ClassicEnigma()
    plain = 'HERMENEGILDEXKOMM'
    print("PLAIN: {0}".format(plain))
    encrypted = classic_enigma.code(plain)
    print("ENCRYPTED: {0}".format(encrypted))
    classic_enigma.reset()
    decrypted = classic_enigma.code(encrypted)
    print("DECRYPTED: {0}".format(decrypted))

    print('\n* M4 Classic Enigma: *')
    m4_enigma = M4ClassicEnigma()
    plain = 'HERMENEGILDEXKOMM'
    print("PLAIN: {0}".format(plain))
    encrypted = m4_enigma.code(plain)
    print("ENCRYPTED: {0}".format(encrypted))
    m4_enigma.reset()
    decrypted = m4_enigma.code(encrypted)
    print("DECRYPTED: {0}".format(decrypted))

    print('\n* Base64Enigma: *')
    b64_enigma = Base64Enigma()
    plain = json.dumps({'hello': 'world'})
    print("PLAIN: {0}".format(plain))
    encrypted = b64_enigma.code(base64.b64encode(plain))
    print("ENCRYPTED: {0}".format(encrypted))
    b64_enigma.reset()
    decrypted = base64.b64decode(b64_enigma.code(encrypted))
    print("DECRYPTED: {0}".format(decrypted))
