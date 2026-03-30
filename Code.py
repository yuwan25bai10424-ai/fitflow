import json
import os
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LinearRegression

FILE = "users.json"

TRAIN_X = np.array([
    [20, 90, 175, 29.4, 0], [25, 85, 170, 29.4, 0], [30, 95, 168, 33.7, 0],
    [22, 55, 165, 20.2, 1], [27, 60, 172, 20.3, 1], [24, 65, 178, 20.5, 1],
    [35, 75, 175, 24.5, 2], [40, 70, 168, 24.8, 2], [28, 68, 170, 23.5, 2],
    [19, 100, 180, 30.9, 0],[45, 80, 165, 29.4, 0],[32, 58, 160, 22.7, 1],
    [26, 72, 174, 23.8, 2],[38, 88, 176, 28.4, 0],[21, 62, 169, 21.7, 1],
])

CALORIE_Y = np.array([
    1700, 1800, 1600, 2600, 2500, 2700,
    2100, 2000, 2050, 1650, 1750, 2450,
    2100, 1850, 2550,
])

WORKOUT_Y = np.array([1, 1, 0, 3, 3, 2, 4, 4, 4, 0, 1, 2, 4, 1, 3])

WORKOUT_PLANS = {
    0: "Light Cardio (3 days/week): 30 min walk/jog, yoga, stretching",
    1: "Cardio + Strength (4 days/week): 20 min cardio + full body weights",
    2: "Strength Focus (5 days/week): Upper/Lower split, progressive overload",
    3: "Push Pull Legs (6 days/week): Chest/Shoulders, Back/Biceps, Legs/Core",
    4: "Balanced Routine (4 days/week): 2 strength + 2 cardio days",
}

DIET_PLANS = {
    (0, "Vegetarian"): [
        "Breakfast: Oats + low-fat milk + 1 banana",
        "Lunch:     2 roti + dal + salad (no rice)",
        "Snack:     1 apple + green tea",
        "Dinner:    Vegetable soup + 1 roti + curd",
    ],
    (1, "Vegetarian"): [
        "Breakfast: Oats + full-fat milk + banana + peanut butter",
        "Lunch:     3 roti + paneer curry + rice + salad",
        "Snack:     Peanut butter sandwich + banana shake",
        "Dinner:    Soyabean curry + 2 roti + rice + curd",
    ],
    (2, "Vegetarian"): [
        "Breakfast: Poha / upma + milk",
        "Lunch:     2 roti + dal + sabzi + rice",
        "Snack:     Sprouts / fruit",
        "Dinner:    2 roti + paneer / tofu + salad",
    ],
    (0, "Non-Vegetarian"): [
        "Breakfast: 2 boiled eggs + brown bread + green tea",
        "Lunch:     Grilled chicken (150g) + salad + 1 roti",
        "Snack:     1 boiled egg + cucumber",
        "Dinner:    Steamed fish + vegetables (no rice)",
    ],
    (1, "Non-Vegetarian"): [
        "Breakfast: 4 eggs (2 whole + 2 whites) + bread + milk",
        "Lunch:     Chicken breast (200g) + rice + salad",
        "Snack:     Peanut butter + bread + protein shake",
        "Dinner:    Chicken/fish + rice + vegetables + curd",
    ],
    (2, "Non-Vegetarian"): [
        "Breakfast: 2 eggs + bread + milk",
        "Lunch:     Chicken (150g) + 2 roti + salad",
        "Snack:     Boiled egg / fruit",
        "Dinner:    Fish / chicken + vegetables + 1 roti",
    ],
}

GOAL_DIET_KEY = {0: 0, 1: 1, 2: 2}  

calorie_model = LinearRegression().fit(TRAIN_X, CALORIE_Y)
workout_model = DecisionTreeClassifier(max_depth=4, random_state=42).fit(TRAIN_X, WORKOUT_Y)


def ai_generate(age, weight, height, bmi, goal_encoded, diet_type):
    features = np.array([[age, weight, height, bmi, goal_encoded]])
    calories = int(calorie_model.predict(features)[0])
    workout_label = workout_model.predict(features)[0]
    diet_key = (GOAL_DIET_KEY[goal_encoded], diet_type)
    diet_plan = DIET_PLANS.get(diet_key, DIET_PLANS[(2, diet_type)])
    workout_plan = WORKOUT_PLANS[workout_label]
    return calories, diet_plan, workout_plan


def load_users():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            data = json.load(f)
            for user in data:
                if isinstance(data[user], str):
                    data[user] = {"password": data[user], "data": None}
            return data
    return {}

def save_users(users):
    with open(FILE, "w") as f:
        json.dump(users, f, indent=4)

users = load_users()

def signup():
    print("\n--- Sign Up ---")
    username = input("Create username: ")
    password = input("Create password: ")
    if username in users:
        print("User already exists!")
    else:
        users[username] = {"password": password, "data": None}
        save_users(users)
        print("Account created!")

def login():
    print("\n--- Login ---")
    username = input("Enter username: ")
    password = input("Enter password: ")
    if username in users and users[username]["password"] == password:
        print(f"Welcome {username}!")
        user_dashboard(username)
    else:
        print("Invalid credentials!")

def user_dashboard(username):
    while True:
        print("\n===== Dashboard =====")
        print("1. View Previous Data")
        print("2. Generate / Update Fitness Plan")
        print("3. Delete Data")
        print("4. Logout")
        choice = input("Enter choice: ")

        if choice == "1":
            if users[username]["data"]:
                data = users[username]["data"]
                print("\n--- Previous Data ---")
                for key, value in data.items():
                    if key == "Diet Plan":
                        print("\nDiet Plan:")
                        for item in value:
                            print(" ", item)
                    else:
                        print(f"{key}: {value}")
            else:
                print("No previous data found!")

        elif choice == "2":
            data = generate_plan()
            users[username]["data"] = data
            save_users(users)
            print("Data updated & saved!")

        elif choice == "3":
            users[username]["data"] = None
            save_users(users)
            print("Data deleted!")

        elif choice == "4":
            print(f"Logged out {username}")
            break
        else:
            print("Invalid choice!")


def generate_plan():
    age = int(input("Enter your age: "))
    weight = float(input("Enter your weight (kg): "))
    height = float(input("Enter your height (cm): "))

    print("\nSelect your diet type:\n1. Vegetarian\n2. Non-Vegetarian")
    diet_type = "Vegetarian" if input("Enter choice: ").strip() == "1" else "Non-Vegetarian"

    print("\nSelect your goal:\n1. Weight Loss\n2. Muscle Gain\n3. Maintain")
    goal_map = {"1": (0, "Weight Loss"), "2": (1, "Muscle Gain"), "3": (2, "Maintain")}
    goal_encoded, goal = goal_map.get(input("Enter choice: ").strip(), (2, "Maintain"))

    height_m = height / 100
    bmi = round(weight / (height_m ** 2), 2)

    calories, diet_plan, workout_plan = ai_generate(age, weight, height, bmi, goal_encoded, diet_type)

    bmi_category = (
        "Underweight" if bmi < 18.5 else
        "Normal"      if bmi < 25   else
        "Overweight"  if bmi < 30   else
        "Obese"
    )

    print(f"\nBMI: {bmi} ({bmi_category})")
    print(f"AI-Predicted Calories: {calories} kcal")
    print(f"Diet Type: {diet_type} | Goal: {goal}")
    print("\n--- AI Diet Plan ---")
    for item in diet_plan:
        print(" ", item)
    print("\n--- AI Workout Plan ---")
    print(" ", workout_plan)

    return {
        "Age": age, "Weight": weight, "Height": height,
        "BMI": bmi, "BMI Category": bmi_category,
        "Goal": goal, "Calories": calories,
        "Diet Type": diet_type,
        "Diet Plan": diet_plan,
        "Workout Plan": workout_plan,
    }


while True:
    print("\n===== Gym AI =====")
    print("1. Sign Up")
    print("2. Login")
    print("3. Exit")
    option = input("Enter choice: ")
    if option == "1":
        signup()
    elif option == "2":
        login()
    elif option == "3":
        print("Exiting...")
        break
    else:
        print("Invalid choice!")
