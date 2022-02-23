#!/usr/bin/python3
import re
from . dict_es import dict_es

diccionario_es = [x for x in dict_es if not x.endswith('-')]


class WordleFilter():
    """Filtra las palabras del diccionario en base a los resultados de Wordle.

    Se inicializa con una palabra y la lista de valores que devuelve el juego.
    Se puede llamar varias veces con nuevas palabras y valores que reducirá
    las posibilidades.
    """
    # target = ""  # Future improvement
    last_word = ""
    last_match = []
    posibles = diccionario_es

    def __init__(self, word: str, values: list = []):
        """Recibe una palabra y la lista de valores.

        Valores:
            0: No existe la letra.
            1: Letra en el lugar correcto.
            2: No está en el lugar correcto.

        Si la palabra contiene más de una letra:
            0: Esa letra no está más veces.
            2: Esa letra está en otro lugar.

        Args:
            word (str): Palabra con la que empiezas el juego.
            values (list, optional): Coincidencias. Defaults to [].
        """
        self.last_word = word.lower()
        self.last_match = values
        if values:
            assert len(values) == len(word)
        restantes = self.discard_words()
        print(f"{len(restantes)} palabras restantes")

    def contain_letters(self, letters_yes: list, word: str):
        if len(set(letters_yes)) != len(letters_yes):
            for letter in letters_yes:
                if letter not in word:
                    return False
                else:
                    reps = letters_yes.count(letter)
                    if word.count(letter) < reps:
                        return False
            return True

        return set(letters_yes).issubset(set(word))

    def discard_words(self) -> list:
        """Reduce el diccionario de posibles palabras.

        Returns:
            list: Lista de posibles palabras restantes.
        """
        if not self.last_word:
            return None

        letters_yes = []  # Letras que si están en la palabra
        letters_no = []  # Letras que no están en la palabra
        letters_fixed = []
        for i, m in enumerate(self.last_match):
            letter = self.last_word[i]
            if m:
                letters_yes.append(letter)
                if m == 1:
                    # Letra en el lugar correcto
                    letters_fixed.append(letter)
                if m == 2:
                    # No está en el lugar correcto
                    letters_fixed.append(f"[^{letter}]")
            else:
                letters_fixed.append('\\w')
                # Si la letra está repetida en la palabra podría ser un falso negativo
                if self.last_word.count(letter, i) == 1 and letter not in letters_yes:
                    letters_no.append(letter)


        no_str = f"^[^{''.join(letters_no)}]*$" if letters_no else ''
        fixed_str = "".join(letters_fixed)

        c_no = re.compile(no_str)
        c_ok = re.compile(fixed_str)

        self.posibles = [
            word for word in self.posibles if
            c_ok.match(word) and
            c_no.match(word) and
            self.contain_letters(letters_yes, word)
        ]

        return self.posibles

    def next_word(self, word: str, values: list = []):
        """Recibe la siguiente palabra y una lista de valores.

        Toma las pistas previas de Wordle y le añade nuevas.

        Args:
            word (str): Palabra con la que empiezas el juego.
            values (list, optional): Coincidencias. Defaults to [].
        """
        self.last_word = word.lower()
        self.last_match = values
        if values:
            assert len(values) == len(word)
        restantes = self.discard_words()
        print(f"{len(restantes)} palabras restantes")

