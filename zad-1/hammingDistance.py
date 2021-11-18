def hammingDistance(text1, text2):
	"""
	>>> hammingDistance("abdsbd", "abksba")
	2
	>>> hammingDistance("", "")
	0
	>>> hammingDistance("ab", "ab")
	0
	>>> hammingDistance("abxdd", "abl")
	Traceback (most recent call last):
	...
	ValueError: Texts must be of equal length.
	>>> hammingDistance(set("a"), set("b"))
	Traceback (most recent call last):
	...
	TypeError: Inputs must be strings.
	"""
	if type(text1) != str or type(text2) != str:
		raise TypeError("Inputs must be strings.")
	if len(text1) != len(text2):
		raise ValueError("Texts must be of equal length.")
	differentLettersCount = 0
	for i in range(len(text1)):
		if text1[i] != text2[i]:
			differentLettersCount += 1
	return differentLettersCount

if __name__ == "__main__":
    import doctest
    doctest.testmod()