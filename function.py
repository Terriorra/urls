from random import choice
from random import randint
from random import sample
from string import ascii_uppercase as lt
from itertools import permutations
import os
import sys
from os.path import exists

os.system("CLS")


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


# Загрузка терминов
path = resource_path('Class_9\\terms1.txt')
if not exists(path):
    path = resource_path('terms1.txt')

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()
terms = [(i.split('\t')) for i in text.split('\n')]

# Загрузка расширений
path = resource_path('Class_9\\extension.txt')
if not exists(path):
    path = resource_path('extension.txt')

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

ext = [i for i in text.split('\n')]

# Загрузка доменов
path = resource_path('Class_9\\domains.txt')
if not exists(path):
    path = resource_path('domains.txt')

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()
dom = [i for i in text.split('\n')]

# Загрузка английских слов
path = resource_path('Class_9\\words.txt')
if not exists(path):
    path = resource_path('words.txt')

with open(path, 'r', encoding='ansi') as f:
    text = f.read()
words = [i for i in text.split('\n')]


class Question:
    """
    Форма вопросов
    """

    def __init__(self, quest, var, ant):
        self.quest = quest  # Вопрос
        self.var = var  # Варианты ответов
        self.ant = ant  # Ответы

    def __str__(self):
        var = self.var

        if var:
            var = '\n'.join([f'{i}) {j}' for i, j in enumerate(var, 1)])

        return f'{self.quest}\n{var}'


def quest7():
    ip = []

    for i in range(5):
        # Существующий IP
        now = '.'.join(
            [str(randint(0, 255)),
             str(randint(0, 255)),
             str(randint(0, 255)),
             str(randint(0, 255))]
        )
        ip.append((1, now))

        # Не существующий IP
        now = '.'.join(
            sample([str(randint(256, 300)),
                    str(randint(0, 255)),
                    str(randint(0, 255)),
                    str(randint(0, 255))], 4)
        )
        ip.append((0, now))

    # Отберу 6 вариантов
    ip = sample(ip, 6)

    q = [i[1] for i in ip]

    ant = [str(j) for j, i in enumerate(ip, 1) if i[0] == 1]

    q = Question('Найди существующие ip адреса.', q, ant)

    return q


def quest8():
    """
    На обрывках бумаги были обнаружены записанные фрагменты IP-адреса компьютера. Восстанови адрес.
    """
    count = 0

    s = ''

    while count != 1:
        count = 0

        # Создадим IP
        ip, s = rand_ip()

        # Получу все перестановки
        q = [''.join(i) for i in permutations(s, 4)]
        q = [i.split('.') for i in q]
        q = [i for i in q if '' not in i]

        for i in q:
            if (len(i) == 4) and (max([int(x) for x in i]) <= 255):
                count += 1

    # Перемещать
    sm = sample([(i, j) for i, j in enumerate(s)], 4)

    q = [i[1] for i in sm]

    # Ответ
    ant = sorted([(j, i) for j, i in enumerate(sm, 1)], key=lambda x: x[1])
    ant = [str(i[0]) for i in ant]

    q = Question('Собери существующий ip адрес из обрывков бумаги. Запищи последовательность.', q, ant)

    return q


def rand_ip():
    # Создадим случайный IP

    ip = '.'.join(
        [str(randint(0, 255)),
         str(randint(0, 255)),
         str(randint(0, 255)),
         str(randint(0, 255))]
    )

    index = [i for i in range(0, len(ip), len(ip) // 4)]

    s = ip[index[0]:index[1]], ip[index[1]:index[2]], ip[index[2]:index[3]], ip[index[3]:]

    return ip, s


def quest9():
    """
    Запиши 32-битовый IP-адрес в виде четырех десятичных чисел, разделенных точками
    """
    # Создадим IP
    ip = [randint(0, 255),
          randint(0, 255),
          randint(0, 255),
          randint(0, 255),
          ]

    quest = ''.join(
        [bin(i)[2:].zfill(8) for i in ip]
    )

    ant = '.'.join([str(i) for i in ip])

    q = Question(f'Запиши IP адрес в форме четырёх десятеричных чисел, разделённых точкой. {quest}', '', ant)

    return q


def quest11():
    """
    Доступ к файлу book.txt, находящемуся на сервере bibl.ru, осуществляется по протоколу http.
    Фрагменты адреса файла закодированы буквами от А до Ж.
    Запишите последовательность этих букв, кодирующую адрес указанного файла в сети Интернет.
    """
    protocol = choice(['http', 'https'])
    ex = choice(ext)
    dm = choice(dom)
    word = sample(words, 4)
    word = [i.strip().replace(' ', '_') for i in word]
    file = f'{word[0]}_{word[1]}{ex}'
    serv = f'{word[2]}_{word[3]}{dm}'

    quest = f'''Доступ к файлу {file}, находящемуся на сервере {serv},
осуществляется по протоколу {protocol}.
Фрагменты адреса файла закодированы буквами от А до I.
Запишите последовательность этих букв, кодирующую адрес указанного файла в сети Интернет.
    '''
    ans = [f'{protocol}', '://', f'{word[2]}', f'_{word[3]}', f'{dm}', '/', f'{word[0]}_', f'{word[1]}', f'{ex}']
    ans = sample([(i, j) for i, j in enumerate(ans)], 9)
    ans = [(j, i) for i, j in zip(ans, lt)]

    answer = ''.join([i[0] for i in sorted([(i[0], i[1][0]) for i in ans], key=lambda x: x[1])])
    ans = '\n'.join([f'{i[0]}) {i[1][1]}' for i in ans])

    q = Question(quest + '\n' + ans, '', answer)

    return q


def rand_name_file():
    """
    Случайное имя файла
    """
    space = choice(' _-')
    word = space.join(sample(words, randint(1, 3)))
    ex = choice(ext).strip()

    q = Question(f'Какое расширение у этого файла? {word}{ex}', '', ex)
    return q


def rand_server_name():
    """
    Случайное имя сервера
    """
    space = choice('_-')
    word = space.join(sample(words, randint(1, 3)))
    dm = choice(dom)

    q = Question(f'Какое домен у этого сервера? {word}{dm}', '', dm)
    return q


def quest12():
    """
    Почтовый ящик teacher находится на сервере shkola1.mos.ru.
    В таблице фрагменты адреса электронной почты закодированы цифрами от 1 до 6.
    Запишите последовательность цифр, кодирующую этот адрес.
    """
    dm = choice(dom)

    word = sample(words, 4)
    word = [i.strip().replace(' ', '_') for i in word]

    name = f'{word[0]}_{word[1]}'
    serv = f'{word[2]}_{word[3]}{dm}'

    quest = f'''Почтовый ящик {name} находится на сервере {serv}.
В таблице фрагменты адреса электронной почты закодированы цифрами от 1 до 6. 
Запишите последовательность цифр, кодирующую этот адрес.
    '''

    ans = [f'{word[0]}_', f'{word[1]}', '@', f'{word[2]}_', f'{word[3]}', f'{dm}']
    ans = sample([(i, j) for i, j in enumerate(ans)], 6)
    ans = [(i, j) for i, j in enumerate(ans, 1)]

    answer = ''.join([str(i[0]) for i in sorted([(i[0], i[1][0]) for i in ans], key=lambda x: x[1])])
    ans = '\n'.join([f'{i[0]}) {i[1][1]}' for i in ans])

    q = Question(quest + '\n' + ans, '', answer)

    return q
