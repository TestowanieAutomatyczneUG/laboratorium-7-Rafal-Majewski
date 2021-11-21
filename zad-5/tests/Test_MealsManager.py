import unittest
import requests
from MealsManager import MealsManager
from Meal import Meal
from Category import Category

class Test_MealsManager(unittest.TestCase):
	@classmethod
	def setUpClass(cls) ->	None:
		response = requests.get("https://www.themealdb.com/api/json/v1/1/categories.php")
		if response.status_code != 200:
			raise Exception("Could not fetch categories")
		cls.rawCategories = {}
		for category in response.json()["categories"]:
			cls.rawCategories[category["idCategory"]] = {"id": category["idCategory"], "name": category["strCategory"], "mealsIds": set()}
		cls.rawMeals = {}
		for categoryId in cls.rawCategories:
			response = requests.get(f"https://www.themealdb.com/api/json/v1/1/filter.php?c={cls.rawCategories[categoryId]['name']}")
			if response.status_code != 200:
				raise Exception("Could not fetch meals")
			for partialMeal in response.json()["meals"]:
				response = requests.get(f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={partialMeal['idMeal']}")
				if response.status_code != 200:
					raise Exception("Could not fetch meal")
				meal = response.json()["meals"][0]
				cls.rawCategories[categoryId]["mealsIds"].add(meal["idMeal"])
				cls.rawMeals[meal["idMeal"]] = {"id": meal["idMeal"], "area": meal.get("strArea"), "instructions": meal.get("strInstructions"), "name": meal["strMeal"], "imageUrl": meal["strMealThumb"], "categoryId": categoryId, "ingredients": set([ingredient for ingredient in [meal.get(f"strIngredient{i}") for i in range(1, 21)] if ingredient])}
	def test_init(self) -> None:
		mealsManager = MealsManager()
		self.assertEqual(mealsManager.categories, dict())
		self.assertEqual(mealsManager.meals, dict())
	def test_createAndAddCategory(self) -> None:
		mealsManager = MealsManager()
		category = mealsManager.createAndAddCategory(id = "1", name = "Test category")
		self.assertIn(category.id, mealsManager.categories)
		self.assertEqual(category.id, "1")
		self.assertEqual(category.name, "Test category")
	def test_category_str(self) -> None:
		mealsManager = MealsManager()
		category = mealsManager.createAndAddCategory(id = "1", name = "Test category")
		self.assertEqual(str(category), "Category(name = \"Test category\")")
	def test_category_repr(self) -> None:
		mealsManager = MealsManager()
		category = mealsManager.createAndAddCategory(id = "1", name = "Test category")
		self.assertEqual(repr(category), "Category(id = \"1\", name = \"Test category\")")
	def test_createAndAddMeal(self) -> None:
		mealsManager = MealsManager()
		rawMeal = self.rawMeals[next(iter(self.rawMeals))]
		category = mealsManager.createAndAddCategory(id = rawMeal["categoryId"], name = self.rawCategories[rawMeal["categoryId"]]["name"])
		meal = mealsManager.createAndAddMeal(id = rawMeal["id"], name = rawMeal["name"], imageUrl = rawMeal["imageUrl"], categoryId = rawMeal["categoryId"])
		self.assertEqual(meal.id, rawMeal["id"])
		self.assertEqual(meal.name, rawMeal["name"])
		self.assertEqual(meal.imageUrl, rawMeal["imageUrl"])
		self.assertEqual(meal.category, category)
	def test_meal_str(self) -> None:
		mealsManager = MealsManager()
		rawMeal = self.rawMeals[next(iter(self.rawMeals))]
		category = mealsManager.createAndAddCategory(id = rawMeal["categoryId"], name = self.rawCategories[rawMeal["categoryId"]]["name"])
		meal = mealsManager.createAndAddMeal(id = rawMeal["id"], name = rawMeal["name"], imageUrl = rawMeal["imageUrl"], categoryId = rawMeal["categoryId"])
		self.assertEqual(str(meal), f"Meal(name = \"{rawMeal['name']}\", category = {category})")
	def test_meal_repr(self) -> None:
		mealsManager = MealsManager()
		rawMeal = self.rawMeals[next(iter(self.rawMeals))]
		category = mealsManager.createAndAddCategory(id = rawMeal["categoryId"], name = self.rawCategories[rawMeal["categoryId"]]["name"])
		meal = mealsManager.createAndAddMeal(id = rawMeal["id"], name = rawMeal["name"], imageUrl = rawMeal["imageUrl"], categoryId = rawMeal["categoryId"])
		self.assertEqual(repr(meal), f"Meal(id = \"{rawMeal['id']}\", name = \"{rawMeal['name']}\", category = {category})")
	def test_deleteCategory_only_one_left(self) -> None:
		mealsManager = MealsManager()
		category = mealsManager.createAndAddCategory(id = "1", name = "Test category")
		mealsManager.deleteCategory(category)
		self.assertEqual(mealsManager.categories, dict())
	def test_deleteCategory_many_left(self) -> None:
		mealsManager = MealsManager()
		for categoryId in self.rawCategories:
			category = mealsManager.createAndAddCategory(id = categoryId, name = self.rawCategories[categoryId]["name"])
		mealsManager.deleteCategory(category)
		self.assertNotIn(category.id, mealsManager.categories)
		categoriesLeftIds = set(self.rawCategories.keys())
		categoriesLeftIds.remove(category.id)
		for categoryId in categoriesLeftIds:
			self.assertIn(categoryId, mealsManager.categories)
	def test_createAndAddMeal_many(self) -> None:
		mealsManager = MealsManager()
		rawCategory = self.rawCategories[next(iter(self.rawCategories))]
		category = mealsManager.createAndAddCategory(id = rawCategory["id"], name = rawCategory["name"])
		for mealId in rawCategory["mealsIds"]:
			mealsManager.createAndAddMeal(id = mealId, name = self.rawMeals[mealId]["name"], categoryId = self.rawMeals[mealId]["categoryId"])
			self.assertIn(mealId, mealsManager.meals)
		self.assertEqual(len(mealsManager.meals), len(rawCategory["mealsIds"]))
		for mealId in rawCategory["mealsIds"]:
			self.assertIn(mealId, mealsManager.meals)
			self.assertIsInstance(mealsManager.meals[mealId], Meal)
			self.assertEqual(mealsManager.meals[mealId].id, mealId)
			self.assertEqual(mealsManager.meals[mealId].category, category)
	def test_deleteCategory_with_meals(self) -> None:
		mealsManager = MealsManager()
		rawCategory = self.rawCategories[next(iter(self.rawCategories))]
		category = mealsManager.createAndAddCategory(id = rawCategory["id"], name = rawCategory["name"])
		meals = dict()
		for mealId in rawCategory["mealsIds"]:
			meal = mealsManager.createAndAddMeal(id = mealId, name = self.rawMeals[mealId]["name"], categoryId = self.rawMeals[mealId]["categoryId"])
			meals[mealId] = meal
		mealsManager.deleteCategory(category)
		self.assertNotIn(category.id, mealsManager.categories)
		self.assertEqual(category.meals, dict())
		for mealId in meals:
			self.assertNotIn(mealId, mealsManager.meals)
			self.assertEqual(meals[mealId].category, None)
	def test_deleteMeal(self) -> None:
		mealsManager = MealsManager()
		rawCategory = self.rawCategories[next(iter(self.rawCategories))]
		category = mealsManager.createAndAddCategory(id = rawCategory["id"], name = rawCategory["name"])
		for mealId in rawCategory["mealsIds"]:
			meal = mealsManager.createAndAddMeal(id = mealId, name = self.rawMeals[mealId]["name"], categoryId = self.rawMeals[mealId]["categoryId"])
		mealsManager.deleteMeal(meal)
		self.assertNotIn(meal.id, mealsManager.meals)
		self.assertEqual(meal.category, None)
		self.assertNotIn(meal.id, category.meals)
	def test_getMealsWithIngredients(self) -> None:
		mealsManager = MealsManager()
		for rawCategoryId in self.rawCategories:
			rawCategory = self.rawCategories[rawCategoryId]
			mealsManager.createAndAddCategory(id = rawCategoryId, name = rawCategory["name"])
			for mealId in rawCategory["mealsIds"]:
				mealsManager.createAndAddMeal(id = mealId, name = self.rawMeals[mealId]["name"], categoryId = self.rawMeals[mealId]["categoryId"], ingredients = self.rawMeals[mealId]["ingredients"])
		self.assertEqual(mealsManager.getMealsWithIngredients(set(["water", "soy sauce"])), set([mealsManager.meals["52772"], mealsManager.meals["52774"]]))
	def test_getSimplestMeals_3(self) -> None:
		mealsManager = MealsManager()
		for rawCategoryId in self.rawCategories:
			rawCategory = self.rawCategories[rawCategoryId]
			mealsManager.createAndAddCategory(id = rawCategoryId, name = rawCategory["name"])
			for mealId in rawCategory["mealsIds"]:
				mealsManager.createAndAddMeal(id = mealId, name = self.rawMeals[mealId]["name"], instructions = self.rawMeals[mealId]["instructions"], categoryId = self.rawMeals[mealId]["categoryId"], ingredients = self.rawMeals[mealId]["ingredients"])
		self.assertEqual(mealsManager.getSimplestMeals(2), [mealsManager.meals["53061"], mealsManager.meals["52867"]])
	def test_getSimplestMeals_no_parameter(self) -> None:
		mealsManager = MealsManager()
		for rawCategoryId in self.rawCategories:
			rawCategory = self.rawCategories[rawCategoryId]
			mealsManager.createAndAddCategory(id = rawCategoryId, name = rawCategory["name"])
			for mealId in rawCategory["mealsIds"]:
				mealsManager.createAndAddMeal(id = mealId, name = self.rawMeals[mealId]["name"], instructions = self.rawMeals[mealId]["instructions"], categoryId = self.rawMeals[mealId]["categoryId"], ingredients = self.rawMeals[mealId]["ingredients"])
		expectedSimplestMeals = list(mealsManager.meals.values())
		expectedSimplestMeals.sort(key = lambda meal: len(meal.ingredients) * len(meal.instructions) if meal.ingredients and meal.instructions else float("inf"))
		self.assertEqual(mealsManager.getSimplestMeals(), expectedSimplestMeals)