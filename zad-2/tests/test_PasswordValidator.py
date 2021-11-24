import unittest

from PasswordValidator import PasswordValidator

class TestPasswordValidator(unittest.TestCase):
	def setUp(self):
		self.passwordValidator = PasswordValidator(minLettersCount = 8, minUppercaseLettersCount = 1, minDigitsCount = 1, minSpecialCharactersCount = 1)
	def tearDown(self):
		self.passwordValidator = None
	def test_validate_empty(self):
		self.assertFalse(self.passwordValidator.validate(""))
	def test_validate_8_lowercase_letters(self):
		self.assertFalse(self.passwordValidator.validate("abcdefgh"))
	def test_validate_1_uppercase_letter_and_7_lowercase_letters(self):
		self.assertFalse(self.passwordValidator.validate("Abcdefgh"))
	def test_validate_1_uppercase_letter_and_1_lowercase_letter_and_6_digits_and_at(self):
		self.assertFalse(self.passwordValidator.validate("Ab123456@"))
	def test_validate_1_uppercase_letter_and_7_lowercase_letter_and_1_digit_and_at(self):
		self.assertTrue(self.passwordValidator.validate("Abcdefgh3@"))
	def test_validate_1_uppercase_letter_and_7_lowercase_letter_and_1_digit(self):
		self.assertFalse(self.passwordValidator.validate("kkiuUkaa2"))
	def test_validate_non_iterable_object(self):
		self.assertRaises(TypeError, self.passwordValidator.validate, 123)
	def test_validate_list_with_non_string_elements(self):
		self.assertRaises(TypeError, self.passwordValidator.validate, ["a", 2, 3])
