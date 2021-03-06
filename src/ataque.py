"""Contém a classe que representa um ataque."""

import random
from tipo import get_tipo


class Ataque:

    """Representa um ataque de Pokémon."""

    def __init__(self, _dados):
        """Recebe uma lista de dados e cria um ataque."""
        dados = list(_dados)
        dados.reverse()

        self._nome = dados.pop()
        self._typ = get_tipo(dados.pop())
        self._acu = dados.pop()
        self._pwr = dados.pop()
        self._pp = self.pp_max = dados.pop()

    def mostra(self, full=False):
        """Exibe nome e PP atual/máximo do ataque.
        Se full=True, mostra também os atributos restantes."""
        if not full:
            print(self.nome, "(" + str(self.typ.nome) + ")",
                  "[" + str(self.pp) + "/" + str(self.pp_max) + "]")
        else:
            print(self.nome, "(" + str(self.typ.nome) + ")")
            print(str(self.pp) + "/" + str(self.pp_max), "PP")
            print("Acurácia:", self.acu)
            print("Poder:", self.pwr)

    @property
    def nome(self):
        return self._nome

    @property
    def typ(self):
        return self._typ

    @property
    def acu(self):
        return self._acu

    @property
    def pwr(self):
        return self._pwr

    @property
    def pp(self):
        return self._pp

    def usa_pp(self):
        self._pp -= 1

    def sem_pp(self):
        return self.pp <= 0

    def acertou(self):
        """Verifica se o ataque resultou em acerto ou erro."""
        chance = (self.acu * self.acu)/10000
        return random.uniform(0, 1) <= chance

    def calcula_dano(self, atacante, defensor, is_basico=False):
        """Calcula o dano causado pelo ataque usando a fórmula da 1ª geração.
           Se is_basico=True, aleatório e crítico não são contabilizados."""
        # Reúne os valores básicos para calcular dano
        lvl = atacante.lvl
        base = self.pwr
        if self.typ.is_especial:
            atk = atacante.spc
            dfs = defensor.spc
        else:
            atk = atacante.atk
            dfs = defensor.dfs

        eff = self.efetividade(defensor, is_basico)

        # Calcula o dano base, sem modificadores aleatórios
        dano = (2*lvl + 10)/250 * atk/dfs * base + 2
        dano *= self.stab(atacante) * eff

        # Aplica o modificador de crítico e aleatório
        if not is_basico:
            dano *= self.critico(atacante, eff) * self.aleatorio()

        return int(dano)

    def stab(self, atacante):
        """Confere um bônus de dano se tipo de ataque e atacante são iguais."""
        typ = self.typ
        if atacante.tipo1 == typ or atacante.tipo2 == typ:
            return 1.5
        return 1

    def critico(self, atacante, eff):
        """Verifica se o atacante causou um golpe crítico."""
        lvl = atacante.lvl
        chance = atacante.spd/512

        if random.uniform(0, 1) <= chance and eff > 0:
            print("> Golpe crítico!")
            return (2*lvl + 5)/(lvl + 5)
        return 1

    def efetividade(self, defensor, is_basico):
        """Aplica o multiplicador de efetividade presente na tabela."""
        # Calcula o multiplicador
        mult = self.typ.get_eff_contra(defensor.tipo1)
        if defensor.tipo2.nome != "Blank":
            mult *= self.typ.get_eff_contra(defensor.tipo2)

        # Exibe mensagem
        if not is_basico:
            if mult > 1:
                print("> Foi super efetivo!")
            elif 0 < mult < 1:
                print("> Não foi muito efetivo...")
            elif mult == 0:
                print("> Não teve efeito. :(")

        return mult

    def aleatorio(self):
        """Gera um número aleatório a ser usado na fórmula de dano."""
        return random.uniform(0.85, 1)
