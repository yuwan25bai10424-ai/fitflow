# Gym AI — Your Personal Fitness Planner

A command-line fitness assistant that uses machine learning to generate personalized workout and diet plans based on your body stats and goals. No gym trainer needed.

---

## What it does

You enter your age, weight, height, diet preference, and fitness goal — and the app figures out the rest. It predicts your daily calorie needs, picks the right workout routine, and hands you a full meal plan tailored to you.

Everything gets saved to your account so you can come back and check your plan anytime.

---

## Features

- **User accounts** — sign up, log in, and keep your data safe
- **BMI calculator** — instantly know where you stand (Underweight / Normal / Overweight / Obese)
- **AI calorie prediction** — uses Linear Regression trained on real fitness data
- **Smart workout plans** — Decision Tree model picks from 5 different routines based on your profile
- **Diet plans** — separate meal plans for Vegetarian and Non-Vegetarian, matched to your goal
- **Persistent storage** — your data is saved in a local `users.json` file

---

## Fitness Goals Supported

| Goal | What it means |
|------|--------------|
| Weight Loss | Calorie deficit + light to moderate training |
| Muscle Gain | High protein diet + heavy lifting splits |
| Maintain | Balanced diet + mixed cardio/strength routine |

---

## Getting Started

### Requirements

```
Python 3.7+
numpy
scikit-learn
```

Install dependencies:

```bash
pip install numpy scikit-learn
```

### Run the app

```bash
python gym.py
```

---

## How to Use

1. **Sign Up** — create a username and password
2. **Login** — access your personal dashboard
3. **Generate Plan** — enter your stats and get your AI-generated plan
4. **View Previous Data** — check your last saved plan anytime
5. **Update or Delete** — regenerate your plan or clear your data

---

## Project Structure

```
├── gym.py          # Main application
├── users.json      # Auto-generated user data file
└── README.md       # You're reading this
```

---

## How the AI Works

The app is trained on a small dataset of 15 fitness profiles. It uses:

- `LinearRegression` → predicts daily calorie intake based on age, weight, height, BMI, and goal
- `DecisionTreeClassifier` → recommends one of 5 workout plans based on the same inputs

It's lightweight, runs offline, and doesn't need any API or internet connection.

---

## Sample Output

```
BMI: 24.5 (Normal)
AI-Predicted Calories: 2100 kcal
Diet Type: Non-Vegetarian | Goal: Maintain

--- AI Diet Plan ---
  Breakfast: 2 eggs + bread + milk
  Lunch:     Chicken (150g) + 2 roti + salad
  Snack:     Boiled egg / fruit
  Dinner:    Fish / chicken + vegetables + 1 roti

--- AI Workout Plan ---
  Balanced Routine (4 days/week): 2 strength + 2 cardio days
```

---

## Built With

- Python
- NumPy
- scikit-learn

---


