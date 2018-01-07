"""Test for llama_class"""
import unittest
from src.llama_class import Llama


class LlamaClassTest(unittest.TestCase):
    """Unit test class for Llama"""

    def get_name(self):
        """Test get_name"""
        calogero = Llama('Calogero')
        self.assertEqual(calogero.get_name(), "Calogero")

    def set_name(self):
        """Test set_name"""
        calogero = Llama('Calogero')
        calogero.set_name('Pippino')
        self.assertEqual(calogero.get_name(), "Pippino")

    def load(self):
        """Test load"""
        self.assertEqual("", "")

    def save(self):
        """Test save"""
        self.assertEqual("", "")

    def to_string(self):
        """Test to_string"""
        calogero = Llama('Calogero')
        self.assertEqual(calogero.to_string(), "Llama\nNome : Calogero\n")
        calogero = Llama('Cal\\!2ogero')
        self.assertEqual(calogero.to_string(), "Llama\nNome : Cal\\!2ogero\n")
        calogero = Llama('')
        self.assertEqual(calogero.to_string(), "Llama\nNome : \n")


if __name__ == '__main__':
    unittest.main()
