#!/usr/bin/python3
import unittest
import random
from pokemon import *

class PrimesTestCase(unittest.TestCase):
    def setUp(self):
        self.nome  = "pedro" 
        self.lvl   = random.randint(0, 100)     
        self.hp    = random.randint(0, 100)   
        self.atk   = random.randint(0, 100)   
        self.defe  = random.randint(0, 100)    
        self.spd   = random.randint(0, 100)   
        self.spc   = random.randint(0, 100)   
        self.tipo1 = random.randint(0, 100)   
        self.tipo2 = random.randint(0, 100)   
        self.n_atk = random.randint(0, 100)   
        self.t     = Pokemon(self.nome, self.lvl, self.tipo1, self.tipo2)
       
    def teste_cria_pokemons(self):
        self.assertEqual(self.t.nome, self.nome)
        self.assertEqual(self.t.lvl, self.lvl)
        self.assertEqual(self.t.tipo1, self.tipo1)
        self.assertEqual(self.t.tipo2, self.tipo2)
       
    def teste_cria_atributos(self):
        self.t.cria_atributos(self.hp, self.atk, self.defe, self.spd, self.spc)
        self.assertEqual(self.t.atributos["HP" ], self.hp)
        self.assertEqual(self.t.atributos["ATK"], self.atk)
        self.assertEqual(self.t.atributos["DEF"], self.defe)
        self.assertEqual(self.t.atributos["SPD"], self.spd)
        self.assertEqual(self.t.atributos["SPC"], self.spc)
    
    def teste_ataques(self):
        self.t.adiciona_ataque("bla", 1, 21, 10, 246)
        self.t.adiciona_ataque("blo", 2, 22, 11, 247)
        self.t.adiciona_ataque("ble", 3, 23, 12, 248)
        self.t.adiciona_ataque("bliu", 4, 24, 13, 249)
        with self.assertRaises(Exception):
            self.t.adiciona_ataque("bleh", 5, 25, 14, 250)         
         


if __name__ == '__main__':
    unittest.main()
