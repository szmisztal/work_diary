def calculate_fuel_difference(refuel, standard_fuel_usage, actual_fuel_difference):
    difference = standard_fuel_usage - refuel
    difference_to_save_in_db = actual_fuel_difference + difference
    return difference_to_save_in_db

print(calculate_fuel_difference(30, 22, 10))
