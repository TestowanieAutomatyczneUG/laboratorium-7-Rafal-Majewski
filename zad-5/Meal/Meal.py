from Category import Category

class Meal:
	def __init__(self, *, id: str, name: str, imageUrl: str = None, category: Category, instructions: str = None, ingredients: set[str] = None) -> None:
		self.__id = id
		self.__name = name
		self.__imageUrl = imageUrl
		self.__category = category
		self.__instructions = instructions
		self.__ingredients = ingredients
	
	def _unsetCategory(self) -> None:
		self.__category = None
	@property
	def id(self) -> str:
		return self.__id
	@property
	def name(self) -> str:
		return self.__name
	@property
	def imageUrl(self) -> str:
		return self.__imageUrl
	@property
	def category(self) -> Category:
		return self.__category
	@property
	def instructions(self) -> str:
		return self.__instructions
	@property
	def ingredients(self) -> set[str]:
		return self.__ingredients

	def __str__(self) -> str:
		return f"Meal(name = \"{self.name}\", category = {self.category})"
	def __repr__(self) -> str:
		return f"Meal(id = \"{self.id}\", name = \"{self.name}\", category = {self.category})"
	

