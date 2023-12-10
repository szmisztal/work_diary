def year_table_template(year_details):
    print("--------")
    print("{:<7} {:<15} {:<14} {:<26} {:<13} {:<9} {:<17} {:<9} {:<10}".format(
        "YEAR:", "WORKING DAYS:", "TOTAL HOURS:", "AVERAGE HOURS PER MONTH:", "KILOMETERS:", "REFUEL:",
        "FUELS STANDARD:", "SALARY:", "AVERAGE SALARY PER MONTH:"
    ))
    for data in year_details:
        formatted_year = data[1]
        formatted_working_days = data[2]
        formatted_total_hours = data[3]
        formatted_average_hours = data[4]
        formatted_kilometers = data[5]
        formatted_refuel = data[6]
        formatted_fuels_standard = data[7]
        formatted_salary = data[8]
        formatted_average_salary = data[9]
        print("{:<7} {:<15} {:<14} {:<26} {:<13} {:<9} {:<17} {:<9} {:<10}".format(
            formatted_year, formatted_working_days, formatted_total_hours, formatted_average_hours,
            formatted_kilometers, formatted_refuel, formatted_fuels_standard, formatted_salary, formatted_average_salary
            ))


