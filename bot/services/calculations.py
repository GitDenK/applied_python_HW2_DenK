def calculate_water_norm(weight, activity_min, temperature):
    base = weight * 30
    activity_water = (activity_min // 30) * 500
    if temperature > 25:
        activity_water += 500
    return base + activity_water

def calculate_calories(weight, height, age, activity_min):
    base = 10 * weight + 6.25 * height - 5 * age
    activity_calories = (activity_min / 60 * 200)
    return base + activity_calories
