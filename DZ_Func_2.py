import csv


def read_employees(input_file: str) -> list:
    with open(input_file, 'r', encoding='utf-8') as employee_file:
        employees_list = list(csv.reader(employee_file, delimiter=';'))
        return employees_list[1:]


def print_department_teams(input_file: str) -> None:
    department_teams_dict = {}
    employees = read_employees(input_file)
    for employee in employees:
        if employee[1] not in department_teams_dict:
            department_teams_dict[employee[1]] = []
        if employee[2] not in department_teams_dict[employee[1]]:
            department_teams_dict[employee[1]].append(employee[2])
    for department, teams in department_teams_dict.items():
        print(department, ', его команды:', sep='')
        for team in teams:
            print('  ', team, sep='')


def get_summary(input_file: str) -> dict:
    department_summary_dict = {}
    employees = read_employees(input_file)
    for employee in employees:
        salary = int(employee[5])
        if employee[1] not in department_summary_dict:
            department_summary_dict[employee[1]] = {
                'number_of_employees': 1,
                'min_salary': salary,
                'max_salary': salary,
                'salary_sum': salary,
            }
        else:
            department_summary_dict[employee[1]]['number_of_employees'] += 1
            department_summary_dict[employee[1]]['salary_sum'] += salary
            if salary < department_summary_dict[employee[1]]['min_salary']:
                department_summary_dict[employee[1]]['min_salary'] = salary
            if salary > department_summary_dict[employee[1]]['max_salary']:
                department_summary_dict[employee[1]]['max_salary'] = salary
    for department in department_summary_dict:
        department_summary_dict[department]['mean_salary'] = (
            department_summary_dict[department]['salary_sum']
            / department_summary_dict[department]['number_of_employees']
        )
    return department_summary_dict


def print_department_summary(input_file: str) -> None:
    summary = get_summary(input_file)
    for department, features in summary.items():
        print(department, ':', sep='')
        print('  Количество человек:', features['number_of_employees'])
        print('  Минимальная зарплата:', features['min_salary'])
        print('  Максимальная зарплата:', features['max_salary'])
        print('  Средняя зарплата:', features['mean_salary'])


def csv_save_department_summary(
    input_file: str,
    output_file: str,
) -> None:
    summary = get_summary(input_file)
    with open(output_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([
            'department', 'number_of_employees', 'min_salary',
            'max_salary', 'mean_salary',
        ])
        for department, features in summary.items():
            writer.writerow([
                department, features['number_of_employees'],
                features['min_salary'], features['max_salary'],
                features['mean_salary'],
            ])
    print('Сохранено в', output_file)


def main(
    report_version: int,
    input_file: str = 'Corp_Summary.csv',
    output_file: str = 'Department_summary.csv',
) -> None:
    if report_version == 1:
        print_department_teams(input_file)
    elif report_version == 2:
        print_department_summary(input_file)
    elif report_version == 3:
        csv_save_department_summary(input_file, output_file)
    else:
        raise ValueError('Неверное значение аргумента версии отчета')


if __name__ == '__main__':
    main(3)
