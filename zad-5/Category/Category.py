class Category:
	def __init__(self, *, id: str, name: str) -> None:
		self.__id = id
		self.__name = name
		self.__meals = dict()
	@property
	def id(self) -> str:
		return self.__id
	@property
	def name(self) -> str:
		return self.__name
	@property
	def meals(self) -> dict:
		return self.__meals
	def __str__(self) -> str:
		return f"Category(name = \"{self.name}\")"
	def __repr__(self) -> str:
		return f"Category(id = \"{self.id}\", name = \"{self.name}\")"