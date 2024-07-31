from subprocess import run
import datetime

command = ['ps', 'aux']
result = run(command, capture_output=True, text=True)

lines = result.stdout.split('\n')

users = {line.split()[0] for line in lines[1:-1]}
memory_list = [float(line.split()[3]) for line in lines[1:-1]]
cpu_list = [float(line.split()[2]) for line in lines[1:-1]]
process_name = [line.split()[10] for line in lines[1:-1]]

# подсчет общей занятой памяти
memory = 0
for number in memory_list:
    memory += number

# подсчет используемого cpu
cpu = 0
for number in cpu_list:
    cpu += number

# формирование строки с пользователями
user_string = ''
for user in users:
    user_string = user_string + ' ' + f"'{user}',"

# создаем словарь вида {'пользователь': число процессов(int)}
user_process = {}
for user in users:
    cnt = 1
    for line in lines[1:-1]:
        if user in line.split()[0]:
            user_process[user] = cnt
            cnt += 1

# сортируем пользователей по количеству процессов
users_sorted_by_process = sorted(user_process.items(), key=lambda item: item[1], reverse=True)

# создаем словарь вида {'имя процесса': количество памяти(float)} и в последствии сортируем его
memory_to_proc_name = dict(zip(process_name, memory_list))
memory_used_sorted = sorted(memory_to_proc_name.items(), key=lambda item: item[1], reverse=True)

# создаем словарь вида {'имя процесса': количество исп. cpu(float)} и в последствии сортируем его
cpu_to_proc_name = dict(zip(process_name, cpu_list))
cpu_used_sorted = sorted(cpu_to_proc_name.items(), key=lambda item: item[1], reverse=True)

print('Отчёт о состоянии системы:')
print(f'Пользователи системы: {user_string[:-1]}')
print(f'Процессов запущено: {len(lines) - 2}')
print("Пользовательских процессов:")
for user in users_sorted_by_process:
    print(f'{user[0]}: {user[1]}')
print(f'Всего памяти используется: {memory}%')
print(f'Всего CPU используется: {cpu}%')
print(f"Больше всего памяти использует: {memory_used_sorted[0][0][:20]}")
print(f'Больше всего CPU использует: {cpu_used_sorted[0][0][:20]}')

now = datetime.datetime.now()
filename = f"{now.strftime('%m-%d-%Y-%H:%M:%S')}-scan.txt"
with open(filename, 'w') as file:
    file.write('Отчёт о состоянии системы:\n')
    file.write(f'Пользователи системы: {user_string[:-1]}\n')
    file.write(f'Процессов запущено: {len(lines) - 2}\n')
    file.write("Пользовательских процессов:\n")
    for user in users_sorted_by_process:
        file.write(f'{user[0]}: {user[1]}\n')
    file.write(f'Всего памяти используется: {memory}%\n')
    file.write(f'Всего CPU используется: {cpu}%\n')
    file.write(f"Больше всего памяти использует: {memory_used_sorted[0][0][:20]}\n")
    file.write(f'Больше всего CPU использует: {cpu_used_sorted[0][0][:20]}\n')
