from experta import *


class Restaurant:
    def __init__(self, name, meal,location, cuisines, service, price):
        self.name = name
        self.meal = meal
        self.location = location
        self.cuisines = cuisines
        self.service = service
        self.price = price

class UserInput(Fact):
    pass

class RecommenderSystem(KnowledgeEngine):
    @DefFacts()
    def initial_facts(self):
        yield Fact(action="recommend")

    @Rule(UserInput(meal=MATCH.meal, location=MATCH.location, cuisine=MATCH.cuisine, service=MATCH.service, price=MATCH.price), Fact(action="recommend"))
    def recommend_restaurant(self, meal, location, cuisine, service, price):
        # Define a list of restaurants
        restaurants = [
            Restaurant("Yumpys", ["Lunch", "Dinner", "Late night Snack"],"Mess 1", ["Chinese", "Maggi", "Biryani"], "seating available", "Budget Friendly"),
            Restaurant("Maggi Hotspot",["Lunch", "Dinner", "Late night Snack"],"CP", ["Maggi", "Biryani"], "seating available", "Expensive"),
            Restaurant("Chipotle", ["Lunch", "Dinner", "Late night Snack"],"Mess 1", ["South Indian"], "takeaway only", "Expensive"),
            Restaurant("Wich Please!", ["Dinner", "Late night Snack"],"Mess 2", ["Sandwich"], "seating available", "Moderate"),
            Restaurant("SFC",["Dinner", "Late night Snack"],"Mess 2", ["Burger", "Fries"], "seating available", "Moderate"),
            Restaurant("Fruitful!", ["Dinner"], "CP", ["Desert", "Burger", "Fries"], "seating available", "Expensive"),
            Restaurant("Agra Chaat",["Lunch", "Dinner"],"CP", ["North Indian"], "seating available", "Budget Friendly"),
            Restaurant("Vijay Vahini Foods",["Lunch", "Dinner"],"CP", ["North Indian", "Biryani", "Chinese"], "seating available", "Moderate"),
            Restaurant("Cafetaria", ["Breakfast", "Lunch", "Dinner"],"Academic Block", ["North Indian", "South Indian", "Desert", "Chinese"], "seating available", "Moderate"),
            Restaurant("Cafe Coffee Day",["Breakfast", "Lunch"], "Academic Block", ["Sandwich"], "takeaway only", "Expensive")
        ]

        # Define the weights for each criterion
        weights = {
            "meal": 600,
            "location":200,
            "cuisine": 100,
            "budget": 50,
            "service": 25
        }

        # Calculate scores for each restaurant based on weighted sum
        scores = []
        for restaurant in restaurants:
            score = (
                    (meal.lower() in [c.lower() for c in restaurant.meal]) * weights["meal"]+
                    (location.lower() == restaurant.location.lower()) * weights["location"]+
                    (cuisine.lower() in [c.lower() for c in restaurant.cuisines]) * weights["cuisine"] +
                    (price.lower() == restaurant.price.lower()) * weights["budget"] +
                    (service.lower() == restaurant.service.lower()) * weights["service"]
            )
            scores.append(score)


        # Find the indices of the restaurants with the highest scores
        max_scores = max(scores)
        # Find the indices of the restaurants with the highest scores
        best_restaurant_indices = [i for i, score in sorted(enumerate(scores), key=lambda x: x[1], reverse=True) if score >= 900]

        if best_restaurant_indices:
            print("Recommended restaurants:")
            for index in best_restaurant_indices:
                best_restaurant = restaurants[index]
                print("Restaurant:", best_restaurant.name)
                print("meal:", ', '.join(best_restaurant.meal))
                print("location:", best_restaurant.location)
                print("Cuisines:", ', '.join(best_restaurant.cuisines))
                print("Service:", best_restaurant.service)
                print("Price:", best_restaurant.price)
                print()
        else:
            print("No restaurants found matching the criteria.")


# Create an instance of the recommender system
engine = RecommenderSystem()

# Run the engine to get recommendations based on user input
engine.reset()

meal1 = input("Enter your preferred meal time (e.g., Breakfast,Lunch, Dinner): ")
location1 = input("Enter your preferred location: ")
cuisine1 = input("Enter your preferred cuisine: ")
service1 = input("Enter your preferred service type (e.g., seating available, takeaway only): ")
price1 = input("Enter your preferred price range (e.g., Budget Friendly, Moderate, Expensive): ")

engine.declare(UserInput(meal=meal1, location=location1, cuisine=cuisine1, service=service1, price=price1))
engine.run()
