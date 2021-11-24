class PasswordValidator:
	def __init__(self, *, minLettersCount = 0, minUppercaseLettersCount = 0, minDigitsCount = 0, minSpecialCharactersCount = 0):
		self.minLettersCount = minLettersCount
		self.minDigitsCount = minDigitsCount
		self.minSpecialCharactersCount = minSpecialCharactersCount
		self.minUppercaseLettersCount = minUppercaseLettersCount
	def validate(self, password):
		"""
		test PasswordValidator for parameters:
		minLettersCount = 8,
		minUppercaseLettersCount = 1,
		minDigitsCount = 1,
		minSpecialCharactersCount = 1

		>>> validate("")
		False
		>>> validate("abcdefgh")
		False
		>>> validate("Ab123456@")
		False
		>>> validate("Abcdefgh3@")
		True
		>>> validate("kkiuUkaa2")
		False
		>>> validate("KkiuUkaa2!")
		True
		>>> validate(["a", 2])
		Traceback (most recent call last):
		...
		TypeError: Non string datatype provided in the input
		>>> validate(123)
		Traceback (most recent call last):
		...
		TypeError: Non iterable datatype provided as the input
		"""
		lettersCount = 0
		digitsCount = 0
		specialCharactersCount = 0
		uppercaseLettersCount = 0
		try:
			for character in password:
				if character.isupper():
					uppercaseLettersCount += 1
				if character.isalpha():
					lettersCount += 1
				elif character.isdigit():
					digitsCount += 1
				else:
					specialCharactersCount += 1
		except TypeError:
			raise TypeError("Non iterable datatype provided as the input")
		except AttributeError:
			raise TypeError("Non string datatype provided in the input")

		if uppercaseLettersCount < self.minUppercaseLettersCount:
			return False
		if lettersCount < self.minLettersCount:
			return False
		if digitsCount < self.minDigitsCount:
			return False
		if specialCharactersCount < self.minSpecialCharactersCount:
			return False
		return True


if __name__ == "__main__": # pragma: no cover
    import doctest
    doctest.testmod(extraglobs={"validate": PasswordValidator(minLettersCount = 8, minUppercaseLettersCount = 1, minDigitsCount = 1, minSpecialCharactersCount = 1).validate})