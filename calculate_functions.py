from datetime import datetime
from config_variables import daily_rate, hourly_rate

def calculate_hours(start_hour_string, end_hour_string):
    hours_format = "%H:%M"
    start_hour = datetime.strptime(start_hour_string, hours_format)
    end_hour = datetime.strptime(end_hour_string, hours_format)
    total_hours = end_hour - start_hour
    return str(total_hours)

def calculate_total_hours(details_list):
    total_seconds_list = [time_to_seconds((i[6])) for i in details_list]
    print(total_seconds_list, type(total_seconds_list))
    total_seconds = sum(total_seconds_list)
    total_hours = total_seconds / 3600
    return str(total_hours)

def calculate_average_hours_per_day(details_list):
    days = len(details_list)
    total_seconds_list = [time_to_seconds(i[6]) for i in details_list]
    total_seconds = sum(total_seconds_list)
    average_hours_per_day = total_seconds / 3600 / days
    return str(average_hours_per_day)

def time_to_seconds(time_str):
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s

def calculate_standard_fuel_usage(kilometers):
    standard_usage = kilometers * 0.25
    return round(standard_usage)

def calculate_fuel_difference(refuel, standard_fuel_usage):
    difference = standard_fuel_usage - refuel
    return difference

def calculate_salary(working_days, total_hours):
    salary = (daily_rate * working_days) + (hourly_rate * total_hours)
    return round(salary, 2)
