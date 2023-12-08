def month_table_template(month_details):
    print("--------")
    print("{:<8} {:<7} {:<15} {:<14} {:<24} {:<13} {:<9} {:<17} {:<13} {:<10}".format(
        "MONTH:", "YEAR:", "WORKING DAYS:", "TOTAL HOURS:", "AVERAGE HOURS PER DAY:", "KILOMETERS:", "REFUEL:",
        "FUELS STANDARD:", "DIFFERENCE:", "SALARY:"
    ))
    formatted_month = month_details[1]
    formatted_year = month_details[2]
    formatted_working_days = month_details[3]
    formatted_total_hours = month_details[4]
    formatted_average_hours = month_details[5]
    formatted_kilometers = month_details[6]
    formatted_refuel = month_details[7]
    formatted_fuels_standard = month_details[8]
    formatted_difference = month_details[9]
    formatted_salary = month_details[10]
    print("{:<8} {:<7} {:<15} {:<14} {:<24} {:<13} {:<9} {:<17} {:<13} {:<10}".format(
        formatted_month, formatted_year, formatted_working_days, formatted_total_hours, formatted_average_hours,
        formatted_kilometers, formatted_refuel, formatted_fuels_standard, formatted_difference, formatted_salary
        ))


month_details = (1, 12, 2023, 18, "135,5", "8,34", 4567, 560, 26.5, -50, 8675.5)
month_table_template(month_details)
