from datetime import datetime


def calculate_hours(start_hour_string, end_hour_string):
    hours_format = "%H:%M"
    start_hour = datetime.strptime(start_hour_string, hours_format)
    end_hour = datetime.strptime(end_hour_string, hours_format)
    total_hours = end_hour - start_hour
    total_hours_str = str(total_hours)
    hour_strings_list = total_hours_str.split()
    if len(hour_strings_list) == 3:
        return hour_strings_list[2]
    elif len(hour_strings_list) == 1:
        return hour_strings_list[0]

def calculate_total_hours(details_list, index):
    total_seconds_list = [hours_to_seconds((i[index])) for i in details_list]
    total_seconds = sum(total_seconds_list)
    total_hours = total_seconds / 3600
    return total_hours

def calculate_total_hours_for_yearly_summary(details_list, index):
    total_seconds_list = [hours_to_second_for_yearly_total_hour((i[index])) for i in details_list]
    total_seconds = sum(total_seconds_list)
    total_hours = total_seconds / 3600
    return total_hours

def calculate_average_hours(details_list, index):
    constant = len(details_list)
    total_seconds_list = [hours_to_seconds(i[index]) for i in details_list]
    total_seconds = sum(total_seconds_list)
    average_hours = total_seconds / 3600 / constant
    return str(average_hours)

def calculate_average_hours_for_yearly_summary(details_list, index):
    constant = len(details_list)
    total_seconds_list = [hours_to_second_for_yearly_total_hour((i[index])) for i in details_list]
    total_seconds = sum(total_seconds_list)
    average_hours = total_seconds / 3600 / constant
    return str(average_hours)

def hours_to_seconds(time_str):
    h, m, s = map(int, time_str.split(":"))
    return h * 3600 + m * 60 + s

def hours_to_second_for_yearly_total_hour(time_str):
    h, m = map(int, time_str.split("."))
    return h * 3600 + m * 60

def calculate_standard_fuel_usage(kilometers):
    standard_usage = kilometers * 0.25
    return round(standard_usage)

def calculate_fuel_difference(refuel, standard_fuel_usage):
    difference = standard_fuel_usage - refuel
    return difference

def calculate_salary(daily_rate, working_days, hourly_rate, total_hours):
    salary = (daily_rate * working_days) + (hourly_rate * total_hours)
    return round(salary, 2)
