#!/usr/bin/python3

from random import choice
from . dict_es import dict_es

dict_es = [x for x in dict_es if not x.endswith('-')]

class WordleMatcher:
    """Core del juego Wordle. Devuelve las pistas de la palabra objetivo.

        Valores:
            0: No existe la letra. Gris.
            1: Letra en el lugar correcto. Verde.
            2: No está en el lugar correcto. Amarillo.
    """

    def __init__(self, target: str = None) -> None:
        """Recibe la palabra objetivo."""

        if not target or len(target) != 5:
            target = choice(dict_es)
        self.target = target.lower()
        self.last_word = ""
        self.last_match = []

    def guess(self, word: str) -> list:
        """Recibe una palabra y devuelve los valores de Wordle.

        Valores:
            0: No existe la letra. Gris.
            1: Letra en el lugar correcto. Verde.
            2: No está en el lugar correcto. Amarillo.

        Si la palabra contiene más de una misma letra:
            0: Esa letra no está más veces.
            2: Esa letra está en otro lugar.

        Args:
            word (str): Palabra con la que empiezas el juego.
        """

        self.last_word = word.lower()
        self.last_match = [None] * 5

        assert self.target, "No se ha definido la palabra objetivo"

        letters_done = []
        for i, letter in enumerate(word):
            if letter not in self.target:
                # Caso negativo: Valor 0
                self.last_match[i] = 0
            elif self.target[i] == letter:
                # Caso exacto: Valor 1
                self.last_match[i] = 1
                letters_done.append(letter)
            else:
                if word.count(letter) == 1:
                    # Distinto lugar, pero letra única.
                    self.last_match[i] = 2
                    letters_done.append(letter)
                else:
                    # Distinto lugar, pero letra repetida.
                    pass

        # Caso donde hay letras repetidas
        # Letras de sobra serán grises
        # Se hace en segunda vuelta para dar prioridad a las verdes
        if None in self.last_match:
            for i, value in enumerate(self.last_match):
                if value is None:
                    letter = word[i]
                    rest_letters = self.target.count(letter) - letters_done.count(letter)
                    if rest_letters <= 0:
                        # No está más veces
                        self.last_match[i] = 0
                        letters_done.append(letter)
                    else:
                        # Está en otro lugar
                        self.last_match[i] = 2
                        letters_done.append(letter)

        return self.last_match
