#!/usr/bin/python3
import random
import unittest
import os
import sys
from mock import Mock, MagicMock, patch, PropertyMock

# Diz onde procurar pelo módulo pokemon
sys.path.insert(1, os.path.join(sys.path[0], '../src'))
from pokemon import Pokemon, Ataque, le_tipos, get_eff
le_tipos("tipos.txt")
import batalha
from batalha import ordem_inicio, escolhe_ataque, mostra_pokemons, \
    struggle, acertou, stab, critico, efetividade, realiza_ataque, aleatorio
from random_poke import RandomPoke, gera_ataque


class BatalhaTestCase(unittest.TestCase):
    def setUp(self):
        """ Para suprimir o output das funções do bataha """
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = sys.stdout
        self.a = RandomPoke()
        self.b = RandomPoke()
        self.poke1 = Pokemon(self.a.gera())
        self.poke2 = Pokemon(self.b.gera())

    def test_ordem_inicio(self):
        """Verifica se a função ordem_inicio retorna a tupla com
            o pokemon de maior spd primeiro"""
        if self.poke1.spd > self.poke2.spd:
            self.assertEqual(ordem_inicio(self.poke1, self.poke2),
                             (self.poke1, self.poke2))
            self.assertEqual(ordem_inicio(self.poke2, self.poke1),
                             (self.poke1, self.poke2))
        elif self.poke1.spd < self.poke2.spd:
            self.assertEqual(ordem_inicio(self.poke1, self.poke2),
                             (self.poke2, self.poke1))
            self.assertEqual(ordem_inicio(self.poke2, self.poke1),
                             (self.poke2, self.poke1))

        self.assertRaises(AttributeError, ordem_inicio, None, None)
        self.assertRaises(AttributeError, ordem_inicio, self.poke1, None)
        self.assertRaises(AttributeError, ordem_inicio, None, self.poke1)

    def test_mostra(self):
        """Apenas checa se a função levanta erros de atributos"""
        self.assertRaises(AttributeError, mostra_pokemons, None, None)
        self.assertRaises(AttributeError, mostra_pokemons, self.poke1, None)
        self.assertRaises(AttributeError, mostra_pokemons, None, self.poke1)

    def test_escolhe_ataque(self):
        """Primeiro testamos como se nosso pokemons estivesse sem pp,
        o comportamento esperado é que retorne struggle"""
        batalha.input = Mock(return_value="ok")
        with patch('pokemon.Pokemon.todos_ataques_sem_pp', return_value=True):
            self.assertEqual(self.poke2.todos_ataques_sem_pp(), True)
            self.assertEqual(escolhe_ataque(self.poke1), struggle)

        """Testando se a escolhe_ataque está retornando os ataques corretos"""
        for i in range(4):
            batalha.input = Mock(return_value=i + 1)
            self.assertEqual(escolhe_ataque(self.poke1), self.poke1.ataques[i])

        """Nesse ponto o escolhe_ataque receberá de input 4 valores "errados"
           e um certo. O comportamento esperado é que a função não levante
           exceções com os valores errados e execute normalmente quando chegar
           o certo."""
        valores_errados = [self.poke1.nome, random.uniform(-99, 100), 5, -1, 1]
        batalha.input = Mock(side_effect=valores_errados)
        self.assertTrue(escolhe_ataque(self.poke1) in self.poke1.ataques)

    def test_acertou(self):
        chance = (self.poke1.ataques[0].acu * self.poke1.ataques[0].acu)
        chance /= 10000.0

        valores_menores = []
        valores_maiores = []
        for i in range(100):
            valores_menores.append(random.uniform(0.0, chance))
            valores_maiores.append(random.uniform(chance, 1.0))
        valores = valores_menores + valores_maiores

        """Usamos valores conhecidos para testar a unidade do batalha.acertou
           que usa números pseudo-aleatórios"""
        with patch('batalha.random.uniform', side_effect=valores):
            for i in range(100):
                self.assertTrue(acertou(self.poke1.ataques[0]))
            for i in range(100):
                self.assertFalse(acertou(self.poke1.ataques[0]))

        self.assertRaises(AttributeError, acertou, self.poke1.nome)
        self.assertRaises(AttributeError, acertou, self.poke1.hp)
        self.assertRaises(AttributeError, acertou, None)

    def test_stab(self):
        ataque = self.poke1.ataques[0]
        not_typ = 0
        while not_typ == ataque.typ:
            not_typ = random.randint(0, 255)

        """É esperado que se o typ do ataque for igual ao tipo1 ou tipo2 do
        atacante, a batalha.stab retorna 1.5. Caso contrário, retorna 1."""
        with patch('pokemon.Pokemon.tipo1',
                   PropertyMock(return_value=ataque.typ)):
            with patch('pokemon.Pokemon.tipo2',
                       PropertyMock(return_value=ataque.typ)):
                self.assertEqual(stab(ataque, self.poke1), 1.5)
            with patch('pokemon.Pokemon.tipo2',
                       PropertyMock(return_value=not_typ)):
                self.assertEqual(stab(ataque, self.poke1), 1.5)

        with patch('pokemon.Pokemon.tipo2',
                   PropertyMock(return_value=ataque.typ)):
            with patch('pokemon.Pokemon.tipo1',
                       PropertyMock(return_value=not_typ)):
                self.assertEqual(stab(ataque, self.poke1), 1.5)
                with patch('pokemon.Pokemon.tipo2',
                           PropertyMock(return_value=not_typ)):
                    self.assertEqual(stab(ataque, self.poke1), 1)

    def test_critico(self):
        res = (2 * self.poke1.lvl + 5) / (self.poke1.lvl + 5)
        chance = self.poke1.spd / 512
        valores_menores = []
        valores_maiores = []
        for i in range(100):
            valores_menores.append(random.uniform(0.0, chance))
            valores_maiores.append(random.uniform(chance, 1.0))
        valores = valores_menores + valores_maiores

        """Novamente usamos valores conhecidos para testar a
           unidade do batalha.critico que usa números pseudo-aleatórios.
           Os primeiros 100 valores serão menores que chance e
           ou outros 100, maiores."""

        with patch('batalha.random.uniform', side_effect=valores):
            """Em cada loop, cada iteração chamará batalha.critico duas
            vezes, usando, então, dois valores do side_effect"""
            for i in range(50):
                self.assertEqual(critico(self.poke1, 0), 1)
                self.assertEqual(critico(self.poke1,
                                 random.randint(1, 100)), res)
            for i in range(50):
                self.assertEqual(critico(self.poke1, 0), 1)
                self.assertEqual(critico(self.poke1,
                                 random.randint(1, 100)), 1)

        self.assertRaises(AttributeError, critico, self.poke1.nome, None)
        self.assertRaises(AttributeError, critico, self.poke1.hp, None)
        self.assertRaises(AttributeError, critico, None, self.poke1.nome)
        self.assertRaises(AttributeError, critico, None, self.poke1.hp)

    def test_efetividade(self):
        pass

    def test_realiza_ataque(self):
        batalha.input = Mock(return_value="ok")

        """ Vamos gerar novos pokemons para podermos realizar vários
        testes sem acabar com toda hp deles. """
        for i in range(100):
            a = RandomPoke()
            b = RandomPoke()
            poke3 = poke1 = Pokemon(a.gera())
            poke4 = poke2 = Pokemon(b.gera())
            """ Assumindo que o ataque sempre vai acertar """
            with patch('batalha.random.uniform', return_value=1.0):
                """Aqui começa o cálculo do dano"""
                lvl = poke1.lvl
                ataque = Ataque(gera_ataque())
                if ataque.typ.is_especial:
                    atk = poke1.spc
                    dfs = poke2.spc
                else:
                    atk = poke1.atk
                    dfs = poke2.dfs

                pp = ataque.pp
                hp = poke2.hp
                base = ataque.pwr
                eff = efetividade(ataque, poke2)

                dano = (2*lvl + 10)/250 * atk/dfs * base + 2
                dano *= (stab(ataque, poke1) * critico(poke1, eff)
                         * eff * aleatorio())
                dano = int(dano)
                if (dano > 0):
                    poke1.remove_hp(dano)
                if ataque == struggle:
                    dano //= 2
                    poke2.remove(hp.dano)
                """Vamos verificar se o batalha.realiza_ataque está diminuindo
                aplicando corretamente o dano conforme a fórmula."""
                realiza_ataque(poke3, poke4, ataque)
                self.assertEquals(pp - 1, ataque.pp)
                self.assertEquals(poke1.hp, poke3.hp)
                self.assertEquals(poke2.hp, poke4.hp)

    def test_efetividade(self):
        """ Novamente vamos gerar um novo pokemon para podermos realizar vários
        testes com resultados diferentes """
        for i in range(100):
            a = RandomPoke()
            poke1 = Pokemon(a.gera())
            ataque = Ataque(gera_ataque())

            """ Essa é a fórmula para calcular a efetividade"""
            typ_ataque = ataque.typ.numero
            mult = get_eff(typ_ataque, poke1.tipo1.numero)
            if poke1.tipo2.nome != "Blank":
                mult *= get_eff(typ_ataque, poke1.tipo2.numero)
            """ Vamos checar se batalha.efetividade de fato calcula conforme
                 a fórmula """
            self.assertEquals(mult, efetividade(ataque, poke1))

    def tearDown(self):
        sys.stdout.close()  # Fechando o os.devnull
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

# Inicializa o unittest, que cuidará do resto
if __name__ == '__main__':
    unittest.main()
