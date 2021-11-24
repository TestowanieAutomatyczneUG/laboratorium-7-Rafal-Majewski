from Category import Category
from Meal import Meal

class MealsManager:
	def __init__(self) -> None:
		self.__categories = dict()
		self.__meals = dict()
	@property
	def categories(self) -> dict:
		return self.__categories
	@property
	def meals(self) -> dict:
		return self.__meals
	def createAndAddCategory(self, *, id: str, name: str) -> Category:
		category = Category(id = id, name = name)
		self.__categories[id] = category
		return category
	def deleteCategory(self, category: Category) -> Category:
		for mealId in category.meals:
			category.meals[mealId]._unsetCategory()
			del self.__meals[mealId]
		category.meals.clear()
		del self.__categories[category.id]
		return category
	def createAndAddMeal(self, *, id: str, name: str, imageUrl: str = None, categoryId: str, instructions: str = None, ingredients: set[str] = None) -> Meal:
		mealCategory = self.__categories[categoryId]
		meal = Meal(id = id, name = name, imageUrl = imageUrl, category = mealCategory, instructions = instructions, ingredients = ingredients)
		mealCategory.meals[id] = meal
		self.__meals[id] = meal
		return meal
	def deleteMeal(self, meal: Meal) -> Meal:
		del meal.category.meals[meal.id]
		meal._unsetCategory()
		del self.__meals[meal.id]
	def getMealsWithIngredients(self, ingredients: set[str]) -> set[Meal]:
		meals = set()
		for mealId in self.__meals:
			meal = self.__meals[mealId]
			if meal.ingredients.issuperset(ingredients):
				meals.add(meal)
		return meals
	def getSimplestMeals(self, maxCount: int = None) -> list[Meal]:
		if maxCount is None:
			maxCount = len(self.__meals)
		meals = list()
		for mealId in self.__meals:
			meal = self.__meals[mealId]
			meals.append(meal)
		meals.sort(reverse = False, key = lambda meal: len(meal.ingredients)*len(meal.instructions) if meal.ingredients and meal.instructions else float("inf"))
			
		return meals[0:maxCount]