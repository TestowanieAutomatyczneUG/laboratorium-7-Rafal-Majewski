class PasswordValidator:
	def __init__(self, *, minLettersCount = 0, minUppercaseLettersCount = 0, minDigitsCount = 0, minSpecialCharactersCount = 0):
		self.minLettersCount = minLettersCount
		self.minDigitsCount = minDigitsCount
		self.minSpecialCharactersCount = minSpecialCharactersCount
		self.minUppercaseLettersCount = minUppercaseLettersCount
	def validate(self, password):
		lettersCount = 0
		digitsCount = 0
		specialCharactersCount = 0
		uppercaseLettersCount = 0
		for character in password:
			if character.isupper():
				uppercaseLettersCount += 1
			if character.isalpha():
				lettersCount += 1
			elif character.isdigit():
				digitsCount += 1
			else:
				specialCharactersCount += 1
		if uppercaseLettersCount < self.minUppercaseLettersCount:
			return False
		if lettersCount < self.minLettersCount:
			return False
		if digitsCount < self.minDigitsCount:
			return False
		if specialCharactersCount < self.minSpecialCharactersCount:
			return False
		return True