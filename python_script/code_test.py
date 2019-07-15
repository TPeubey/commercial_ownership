import re
import itertools
from termcolor import colored

data = '2 to 6 even numbers and 12 to 26 (even numbers) Sevenoaks Street, 15, 17, 21, 29 to 35 (odd numbers) 38, 42 and 46 (even numbers) 57 to 59 (consecutive numbers) 61 and 73 Oakley Street, 7 to 13 (odd numbers) 16, 19 to 22 (consecutive numbers) 25, 27, 30, 33 and 35 Knole Street, 7, 9, 17, 19, 29to 33 (odd numbers) Holmesdale Street 4 to 12 (even numbers) 13, 14 17 to 20 (consecutive numbers) 22, 38, 46, 47, 49, 50, 52, 55 to 57 (Consecutive numbers) 59 to 65 consecutive numbers) 67 to 71 (consecutive numbers) 73 and 75 Hewell Street, Grange Town, Cardiff'
# data = '28-32 KIMBERLEY TERRACE AND 11-19 (ODD) STATION ROAD, LLANISHEN'
# data = '20-30 (EVEN), LLANGATTOCK ROAD, CARDIFF (CF5 3BQ)'
# data = '1-58 WESTFIELD ROAD, TIVERTON (EX16 5EU), 1-23 (ODD) HOWDEN ROAD, TIVERTON (EX16 5HS) AND 22-36 (EVEN), HOWDEN ROAD, TIVERTON (EX16 5EY)'


data = data.upper()
original_string = data
original_string = original_string.replace(',', ' ').replace('  ', ' ')
original_string = [original_string]

# Test: 'string with nb odd' for odd case  #

for idx, string in enumerate(original_string):
    string = string.replace(',', ' ').strip()
    string = re.sub(r'(\d+)TO', r'\1 TO', string)
    string = re.sub(r'TO(\d+)', r'TO \1', string)
    string = string.split(' ')
    string = [x.strip() for x in string if x]  # remove empty value
    # string = [re.sub(r'^AND$', '', x) for x in string if x]  # remove 'AND' value
    # string = [x.strip() for x in string if x]  # remove empty value

    string_with_nb_odd = string

# print(string_with_nb_odd)

# Test: 'string without number' for odd case  #

# for idx, string in enumerate(original_string):
#     string = string.replace(',', ' ').strip()
#     string = re.sub(r'(\d+)TO', r'\1 TO', string)
#     string = re.sub(r'TO(\d+)', r'TO \1', string)
#     string = string.split(' ')
#     string = [x.strip() for x in string if x]  # remove empty value
#     string = [re.sub(r'^AND$', '', x) for x in string if x]  # remove 'AND' value
#     # print(string)
#     string_without_nb_odd = string
#     # print(string_without_nb_odd)
#     for k in range(0, len(string_without_nb_odd)):
#         if re.findall(r'^(\()', string_without_nb_odd[k]) or re.findall(r'(\))$|(\)\.)$',
#                                                                         string_without_nb_odd[k]):
#             pass
#         else:
#             if re.findall(r'^\d+[A-Z]+|^\d+[A-Z]+-\d+[A-Z]+|\d+', string_without_nb_odd[k]):
#                 string_without_nb_odd[k] = ''
#
# print(string_without_nb_odd)

# Test: get numbers for odd  #

s1 = data
s1 = s1.replace('(EVEN)', '(ODD)').replace('(EVENS)', '(ODD)').replace('(EVEN NUMBERS)', '(ODD)')
s1 = s1.replace('EVEN NUMBERS', '(ODD)').replace('(ODD NUMBERS)', '(ODD)')
s1 = s1.replace('(CONSECUTIVE NUMBERS)', '(INCLUSIVE)').replace('CONSECUTIVE NUMBERS)', '(INCLUSIVE)')
s1 = re.sub(r'(\d+)TO', r'\1 TO', s1)
s1 = re.sub(r'TO(\d+)', r'TO \1', s1)

# get the street name and the previous number before the street name
row_address = s1
row_address = row_address.replace(',', ' ')
row_address = row_address.split(' ')

# print(row_address)
word_not_interested = ['', '(ODD)', 'AND', 'TO', '(INCLUSIVE)']
row_address = [x.replace('(ODD)', '').replace('AND', '').replace('TO', '').replace('(INCLUSIVE)', '')
               for x in row_address if x]
row_address = [x for x in row_address if x]

street_name_list_test = []
for idx, elem in enumerate(row_address):
    if elem not in word_not_interested and not re.findall(r'\d+', elem):
        if re.findall(r'[A-Z]+', row_address[idx-1]):
            pass
        else:
            street_name_list_test.append(row_address[idx-1])  # add the street number
        street_name_list_test.append(elem)  # add the street name

street_name_raw_length = len(street_name_list_test)

# print(street_name_list_test, len(street_name_list_test))

index_start = []
index_end = []

for n in range(0, len(street_name_list_test)):
    if re.findall(r'\d+', street_name_list_test[n]):
        index_start.append(n+1)
        index_end.append(n)

for n in range(0, len(index_start)-1):
    # print(colored(n, 'red'))
    if n == 0:
        street_name_list_test[index_start[n]:index_end[n+1]] = [
            ' '.join(street_name_list_test[index_start[n]:index_end[n+1]])]

    else:
        # print(index_start[n]-n, index_end[n+1]-n)
        street_name_list_test[index_start[n]-n:index_end[n+1]-n] = [
            ' '.join(street_name_list_test[index_start[n]-n:index_end[n+1]-n])]

    if n == len(index_start)-2:
        # print(colored(n+1, 'blue'))
        street_name_list_test[index_start[n]-1:street_name_raw_length] = [
            ' '.join(street_name_list_test[index_start[n]-1:street_name_raw_length])]

# print(street_name_list_test)

# print(re.split(r'\d+', ' '.join(street_name_list_test)))

tl = s1.split('(ODD)')

the_range = []

tl_length = len(tl)
for idx, item in enumerate(tl):
    index_list_next_to = []
    index_list_dash = []

    item = item.replace(',', ' ').replace('  ', ' ')

    tm = item.split(' ')
    # print(tm)

    for n in range(0, len(tm)):  # retrieve index of 'TO'
        if tm[n] == 'TO':
            index_list_next_to.append(n+1)

    temporary_list_single_odd = []
    street_name_list = []
    dash_exception_index = ''

    for n in range(0, len(tm)):  # retrieve index with dash
        if n == len(tm) - 2 and re.findall(r'\d+-\d+', tm[n]):
            dash_exception_index = n

    for index, i in enumerate(tm[:-1]):  # retrieve odd/even number with 'to'
        if index == dash_exception_index:
            dash_range = i.split('-')
            dash_range.append('')
            for n in range(0, len(dash_range)):
                the_range.append(dash_range)
            i = ''

        if i == 'TO':
            the_range.append([tm[index - 1], tm[index + 1], ''])
            tm[index - 1] = ''
            tm[index] = ''
            tm[index + 1] = ''
            if index + 2 < len(tm):
                if tm[index + 2] == '(INCLUSIVE)' or tm[index + 2] == '(INC)' or \
                        tm[index + 2] == '(EVEN)' or tm[index + 2] == '(ODD)':
                    the_range[-1][2] = tm[index + 2]
                    tm[index + 2] = ''

            temporary_list_single_odd = []

        if tm[index + 1] == 'TO' or i == 'TO':  # skip the first odd number, ex: '2' TO 6
            # print(tm)
            i = ''
        if i == 'TO' or i == 'AND':  # skip the 'TO' and 'AND' words
            pass
            i = ''
        if index in index_list_next_to:  # check if the index correspond to the list index
            i = ''

        if re.findall(r'[A-Z]+', i):  # reinitialize the te;porary list when match with street name
            temporary_list_single_odd = []

        if re.findall(r'\d+', i) and not i.startswith('(') and not i.endswith(')'):
            temporary_list_single_odd.append(i)
            the_range.append(temporary_list_single_odd)
            i = ''

        if i == '(INCLUSIVE)' or i == '(ODD)' or i == '(INC)':  # skip some words
            i = ''

        if i != '':
            # print(index, i)
            the_range.append([i])
            street_name_list.append(i)

            # print(street_name_list)

    # print(colored(' '.join(street_name_list), 'blue'))
    # the_range.append(' '.join(street_name_list))

the_range = list(the_range for the_range, _ in itertools.groupby(the_range))
# print(the_range)

the_entire_range = []

for elem_list in the_range:
    # print(elem_list)
    if elem_list[-1] == '':
        for j in range(int(elem_list[0]), int(elem_list[1]) + 2, 2):
            the_entire_range.append(str(j))
    if elem_list[-1] == '(INCLUSIVE)':
        for j in range(int(elem_list[0]), int(elem_list[1]) + 1):
            the_entire_range.append(str(j))
    if elem_list[-1] != '' and elem_list[-1] != '(INCLUSIVE)':
        for nb in elem_list:
            the_entire_range.append(str(nb))

the_entire_range.append(row_address[-1])
entire_range_length = len(the_entire_range)
# print(the_entire_range)
print(data)
# print(the_entire_range)

index_start = []
index_end = []

for n in range(0, len(the_entire_range)-1):
    # print(the_entire_range[n])
    if re.findall(r'[A-Z]+', the_entire_range[n]) and re.findall(r'\d+', the_entire_range[n - 1]):
        index_start.append(n)
    if re.findall(r'[A-Z]+', the_entire_range[n]) and re.findall(r'\d+', the_entire_range[n + 1]):
        index_end.append(n + 1)
    # if n == len(the_entire_range)-2:
    #     index_end.append(n + 1)

# print('Intervalle: ', index_start, index_end)
choice = 0
if len(index_start) > 2 or len(index_start) == 2:
    choice = len(index_start) - 1
if len(index_start) == 1:
    choice = len(index_start)


for n in range(0, choice):
    if len(index_start) > 2:
        if n == 0:
            the_entire_range[index_start[n]:index_end[n]] = [
                ' '.join(the_entire_range[index_start[n]:index_end[n]])]

        else:
            # print(index_start[n]-n, index_end[n+1]-n)
            the_entire_range[index_start[n]-n:index_end[n]-n] = [
                ' '.join(the_entire_range[index_start[n]-n:index_end[n]-n])]

        if n == len(index_start)-2:
            # print(colored(n+1, 'blue'))
            t = (entire_range_length - 1) - index_start[n + 1]
            the_entire_range[index_start[n + 1] - t:entire_range_length] = [
                ' '.join(the_entire_range[index_start[n + 1] - t:entire_range_length])]

    if len(index_start) == 2:
        # print(n)
        if n == 0:
            the_entire_range[index_start[n]:index_end[n]] = [
                ' '.join(the_entire_range[index_start[n]:index_end[n]])]

            the_entire_range[index_start[n + 1]-1:entire_range_length] = [
                ' '.join(the_entire_range[index_start[n + 1]-1:entire_range_length])]

    if len(index_start) == 1:
        if n == 0:
            the_entire_range[index_start[n]:entire_range_length] = [
                ' '.join(the_entire_range[index_start[n]:entire_range_length])]

# print(colored(data, 'blue'))
#
# print(colored(the_entire_range, 'green'))

# Group street name with numbers  #

group_street_name = []
temporary_list = []

for elem in the_entire_range:
    temporary_list.append(elem)
    if re.findall(r'[A-Z]+', elem):
        group_street_name.append(temporary_list)
        temporary_list = []

print(colored(group_street_name, 'blue'))

# Join street name with numbers

for elem_list in group_street_name:
    print(elem_list)
    for n in range(0, len(elem_list) - 1):
        print(elem_list[n], elem_list[len(elem_list)-1])
