from library import structure
import csv
import re
from termcolor import colored
import itertools
import pandas as pd


class Main:

    def __init__(self):
        # regular expression:

        self.number_with_dash = re.compile(r'\d+-\d+')
        self.number_with_slash = re.compile(r'\d+/\d+')
        self.numbers = re.compile(r'\d+')
        self.and_word = re.compile(r'^AND$')
        self.start_parenthese = re.compile(r'^(\()')
        self.end_parenthese_or_odd = re.compile(r'(\))$|(\)\.)$')
        self.start_number_letter = re.compile(r'^\d+[A-Z]+|^\d+[A-Z]+-\d+[A-Z]+|\d+')
        self.sub1 = re.compile(r'(\d+)TO')
        self.sub2 = re.compile(r'TO(\d+)')
        self.capital_letter = re.compile(r'[A-Z]+')
        self.space_dash = re.compile(r'(\d+) - (\d+)')
        self.dash_without_space = re.compile(r'(\d+)-(\d+)')
        self.postcode = re.compile(r'\(\w+ \w+\)')

        self.ow = structure.CommercialOwnershipStructure()
        self.st = structure.CommercialOwnership()
        self.st.start_address()
        self.data = []
        self.list_not_interested = ['LAND AND', 'LAND AT', 'SITES OF', 'PUMPING STATION', 'BEING LAND',
                                    'LAND TO', 'LAND IN', 'LAND LYING', 'PART OF ', 'PARTS OF',
                                    'LAND ADJOINING', 'THE AIRSPACE', 'LAND ON', 'LAND FORMING',
                                    'THE SITES', 'LAND FRONTING', 'ON THE', 'THE SITE', 'ALL THE',
                                    'PORTIONS ', 'LAND BEING']
        self.file = '1_CCOD_FULL_2019_05.csv'

        # all simple numbers and odd list

        self.multiplicate_list = {}
        self.all_odd_address_list = {}

        # simplification name for address
        self.pa = ''

    def start_commercial_ownership(self, the_file):
        # fh.collation_latin_to_utf8(the_file)
        # tsv = fh.csv2tsv(the_file, the_file)
        self.load_data(the_file)
        self.extract_land_and_other_items()
        self.find_multiplication(self.data)

    def find_multiplication(self, data):
        odd = False
        for list_address in data:
            pa = list_address[self.ow.Property_Address]
            # deal with odd/even numbers
            # if "(ODD)" in list_address[self.ow.Property_Address] \
            #          or "INCLUSIVE" in list_address[self.ow.Property_Address]:
            #     odd = True
            #     self.deal_with_odd_and_even(list_address)

            if len(self.numbers.findall(pa[0:len(pa) - 10])) <= 1:
                # print(list_address[self.ow.Title_Number], pa)
                pass
            # else:
            #     print(list_address[self.ow.Title_Number], pa)
            # if re.findall(r'\(\w+ \w+\)', pa):
            #     print(pa)
            # if re.findall(r'INC', pa) and not re.findall(r'INCLUSIVE', pa):
            #     print(list_address[self.ow.Title_Number], pa)

            # deal with simple numbers
            self.simple_numbers_case(pa, list_address)
        return odd

    def simple_numbers_case(self, pa, list_address):
        # pass

        if "ODD" not in pa \
                and "EVEN" not in pa \
                and "INCLUSIVE" not in pa \
                and "INC" not in pa \
                and not self.number_with_dash.findall(pa) \
                and not self.number_with_slash.findall(pa) \
                and len(self.numbers.findall(pa[0:len(pa) - 10])) > 1:

            self.deal_with_simple_numbers(list_address)

    def deal_with_simple_numbers(self, list_address):
        s2 = list_address[self.ow.Property_Address]
        self.get_the_numbers_simple_number(s2, list_address)

    def get_the_numbers_simple_number(self, tl2, list_address):
        original_string = [tl2]
        string_with_nb = ''

        for string in original_string:
            string = string.replace(',', ' ').strip()
            string = string.split(' ')
            string = [x.strip() for x in string if x]  # remove empty value
            # string = [re.sub(r'^AND$', '', x) for x in string if x]  # remove 'AND' value
            # string = [x.strip() for x in string if x]  # remove empty value
            string_with_nb = string
        self.get_the_numbers_simple_number_2(string_with_nb, tl2, list_address)

        return string_with_nb

    def get_the_numbers_simple_number_2(self, string_with_nb, tl2, list_address):
        original_string = [tl2]
        string_without_nb = ''

        for idx, string in enumerate(original_string):
            string = string.replace(',', ' ').strip()
            string = string.split(' ')
            string = [x.strip() for x in string if x]  # remove empty value
            string = [self.and_word.sub('', x) for x in string if x]  # remove 'AND' value
            string_without_nb = string

        self.get_the_numbers_simple_number_2_bis(string_with_nb, string_without_nb, list_address)

    def get_the_numbers_simple_number_2_bis(self, string_with_nb, string_without_nb, list_address):
        for k in range(0, len(string_without_nb)):
            if self.start_parenthese.findall(string_without_nb[k]) or \
                    self.end_parenthese_or_odd.findall(string_without_nb[k]):
                pass
            else:
                if self.start_number_letter.findall(string_without_nb[k]):
                    string_without_nb[k] = ''
        self.group_number(string_with_nb, string_without_nb, list_address)

        return string_without_nb

    def group_number(self, string_with_nb, string_without_nb, list_address):
        simple_nb_list = []
        temporary_list = []

        for k in range(0, len(string_with_nb) - 1):
            if self.start_parenthese.findall(string_with_nb[k]) or \
                    self.end_parenthese_or_odd.findall(string_with_nb[k]):
                pass
            else:
                self.group_number_conditional(k, simple_nb_list, temporary_list, string_with_nb)
        self.remove_redundant_in_group_number(simple_nb_list, string_without_nb, list_address)

    def group_number_conditional(self, k, simple_nb_list, temporary_list, string_with_nb):
        if self.start_number_letter.findall(string_with_nb[k]):
            if self.and_word.match(string_with_nb[k]):
                pass
            temporary_list.append(string_with_nb[k])
            simple_nb_list.append(temporary_list)
        # if re.findall(r'^[A-Z]+$', string_with_nb[k]) and not \
        #         re.match(r'^AND$|^FLAT$|^UNIT$', string_with_nb[k]):
        #     temporary_list = []

    def remove_redundant_in_group_number(self, simple_nb_list, string_without_nb, list_address):
        b_set = set(tuple(x) for x in simple_nb_list)
        group_nb_list = [list(x) for x in b_set]
        group_nb_list.sort(key=lambda x: simple_nb_list.index(x))
        self.group_street_name(group_nb_list, string_without_nb, list_address)

        return group_nb_list

    def group_street_name(self, group_nb_list, string_without_nb, list_address):
        simple_street_name = []
        temporary_list = []
        for k in range(0, len(string_without_nb)-1):  # goes through until the penultimate element
            if string_without_nb[k] == '':
                pass
            else:
                self.group_street_name_conditional(k, simple_street_name, temporary_list, string_without_nb)
        self.remove_redundant_in_group_street_name(simple_street_name, group_nb_list, list_address)
        return simple_street_name

    @staticmethod
    def group_street_name_conditional(k, simple_street_name, temporary_list, string_without_nb):
        temporary_list.append(string_without_nb[k])
        simple_street_name.append(temporary_list)
        # print(k, len(string_without_nb)-1)
        if k == len(string_without_nb) - 2:  # add the last element of the list
            temporary_list.append(string_without_nb[k + 1])
            simple_street_name.append(temporary_list)
        if string_without_nb[k + 1] == '':
            temporary_list = []

    def remove_redundant_in_group_street_name(self, simple_street_name, group_nb_list, list_address):
        b_set = set(tuple(x) for x in simple_street_name)
        group_street_name_list = [list(x) for x in b_set]
        group_street_name_list.sort(key=lambda x: simple_street_name.index(x))

        self.join_street_name(group_nb_list, group_street_name_list, list_address)

    def join_street_name(self, group_nb_list, group_street_name_list, list_address):
        temporary_list = []

        for idx, number_list in enumerate(group_nb_list):
            # group_street_name_list[idx]
            for idx2, street_name in enumerate(group_street_name_list):
                if idx == idx2:
                    for k in range(0, len(number_list)):
                        self.join_street_name_conditional_1(temporary_list, k, number_list, street_name,
                                                            group_street_name_list, list_address)

    def join_street_name_conditional_1(self, temporary_list, k, number_list, street_name, group_street_name_list,
                                       list_address):
        if street_name[0] == 'UNIT' or street_name[0] == 'UNITS':  # deal with 'UNIT' word
            try:
                join = street_name[0] + ' ' + number_list[k] + ' ' + ' '.join(group_street_name_list[1])

                # self.multiplicate_list.append(join)
                temporary_list.append(join)
                self.multiplicate_list[list_address[self.ow.Title_Number]] = temporary_list
            except:
                pass
                # print(colored('Exception: ', 'red'), group_street_name_list, k)
        else:
            self.join_street_name_conditional_2(temporary_list, k, number_list, street_name, list_address)

    def join_street_name_conditional_2(self, temporary_list, k, number_list, street_name, list_address):
        join = number_list[k] + ' ' + ' '.join(street_name)
        # self.multiplicate_list.append(join)
        temporary_list.append(join)
        # print(list_address)
        self.multiplicate_list[list_address[self.ow.Title_Number]] = temporary_list

    def deal_with_odd_and_even(self, list_address):
        s1 = list_address[self.ow.Property_Address]
        s1 = s1.replace('(EVEN)', '(ODD)').replace('(EVENS)', '(ODD)').replace('(EVEN NUMBERS)', '(ODD)')
        s1 = s1.replace('EVEN NUMBERS', '(ODD)').replace('(ODD NUMBERS)', '(ODD)')
        s1 = s1.replace('(CONSECUTIVE NUMBERS)', '(INCLUSIVE)').replace('CONSECUTIVE NUMBERS)', '(INCLUSIVE)')
        s1 = self.sub1.sub(r'\1 TO', s1)
        s1 = self.sub2.sub(r'TO \1', s1)

        self.get_the_numbers_odd(s1.split('(ODD)'), s1, list_address)
        return s1

    def get_the_numbers_odd(self, tl, original_string, list_address):
        the_range = []

        for idx, item in enumerate(tl):
            index_list_next_to = []
            item = item.replace(',', ' ').replace('  ', ' ')
            tm = item.split(' ')

            self.retrieve_index_with_to(the_range, tm, index_list_next_to)
        self.flatten_list_of_element(the_range, original_string, list_address)
        return self.flatten_list_of_element(the_range, original_string, list_address)

    def retrieve_index_with_to(self, the_range, tm, index_list_next_to):
        for n in range(0, len(tm)):  # retrieve index of 'TO'
            if tm[n] == 'TO':
                index_list_next_to.append(n + 1)
        self.retrieve_index_with_dash(the_range, tm, index_list_next_to)
        return index_list_next_to

    def retrieve_index_with_dash(self, the_range, tm, index_list_next_to):
        temporary_list_single_odd = []
        street_name_list = []
        dash_exception_index = ''

        for n in range(0, len(tm)):  # retrieve index with dash
            if n == len(tm) - 2 and re.findall(r'\d+-\d+', tm[n]):
                dash_exception_index = n
        self.retrieve_numbers_with_dash(temporary_list_single_odd, the_range, dash_exception_index, tm,
                                        index_list_next_to, street_name_list)

    def retrieve_numbers_with_dash(self, temporary_list_single_odd, the_range, dash_exception_index, tm,
                                   index_list_next_to, street_name_list):
        for index, i in enumerate(tm[:-1]):  # retrieve odd/even number with 'to'
            if index == dash_exception_index:
                dash_range = i.split('-')
                dash_range.append('')
                for n in range(0, len(dash_range)):
                    the_range.append(dash_range)
                i = ''

            self.retrieve_numbers_with_to(temporary_list_single_odd, index, tm, the_range, i, index_list_next_to,
                                          street_name_list)

    def retrieve_numbers_with_to(self, temporary_list_single_odd, index, tm, the_range, i, index_list_next_to,
                                 street_name_list):
        if i == 'TO' and not self.capital_letter.findall(tm[index - 1]) and not \
                self.capital_letter.findall(tm[index + 1]):
            the_range.append([tm[index - 1], tm[index + 1], ''])
            tm[index - 1] = ''
            tm[index] = ''
            tm[index + 1] = ''
            self.retrieve_if_odd_inclusive(temporary_list_single_odd, index, tm, the_range)
        self.skip_some_element(temporary_list_single_odd, index, tm, the_range, i, index_list_next_to,
                               street_name_list)

    @staticmethod
    def retrieve_if_odd_inclusive(temporary_list_single_odd, index, tm, the_range):
        if index + 2 < len(tm):
            if tm[index + 2] == '(INCLUSIVE)' or tm[index + 2] == '(INC)' or \
                    tm[index + 2] == '(EVEN)' or tm[index + 2] == '(ODD)':
                the_range[-1][2] = tm[index + 2]
                tm[index + 2] = ''
        temporary_list_single_odd = []

    def skip_some_element(self, temporary_list_single_odd, index, tm, the_range, i, index_list_next_to,
                          street_name_list):
        if tm[index + 1] == 'TO' or i == 'TO':  # skip the first odd number, ex: '2' TO 6
            i = ''
        if i == 'TO' or i == 'AND':  # skip the 'TO' and 'AND' words
            pass
            i = ''
        self.check_index(temporary_list_single_odd, index, the_range, i, index_list_next_to, street_name_list)

    def check_index(self, temporary_list_single_odd, index, the_range, i, index_list_next_to, street_name_list):
        if index in index_list_next_to:  # check if the index correspond to the list index
            i = ''
        self.reinitialize_temporary_list(temporary_list_single_odd, the_range, i, street_name_list)

    def reinitialize_temporary_list(self, temporary_list_single_odd, the_range, i, street_name_list):
        if self.capital_letter.findall(i):  # reinitialize the temporary list when match with street name
            temporary_list_single_odd = []
        self.get_simple_numbers(temporary_list_single_odd, the_range, i, street_name_list)

    def get_simple_numbers(self, temporary_list_single_odd, the_range, i, street_name_list):
        if self.numbers.findall(i) and not i.startswith('(') and not i.endswith(')'):
            temporary_list_single_odd.append(i)
            the_range.append(temporary_list_single_odd)
            i = ''
        self.skip_some_element_2(the_range, i, street_name_list)

    def skip_some_element_2(self, the_range, i, street_name_list):
        if i == '(INCLUSIVE)' or i == '(ODD)' or i == '(INC)':  # skip some words
            i = ''

        self.add_element(the_range, i, street_name_list)

    @staticmethod
    def add_element(the_range, i, street_name_list):
        if i != '':
            # print(index, i)
            the_range.append([i])
            street_name_list.append(i)

    def flatten_list_of_element(self, the_range, original_string, list_address):
        the_range = list(the_range for the_range, _ in itertools.groupby(the_range))
        self.get_the_full_numbers_odd(the_range, original_string, list_address)

        return the_range

    def get_the_full_numbers_odd(self, the_range, original_string, list_address):
        the_entire_range = []
        for elem_list in the_range:
            # print(elem_list)
            if elem_list[-1] == '':
                try:
                    for j in range(int(elem_list[0]), int(elem_list[1]) + 2, 2):
                        the_entire_range.append(str(j))
                except:
                    print(colored('Exception: ', 'red'), the_range)
            self.get_the_full_numbers_inclusive(elem_list, the_entire_range)
        self.add_last_element(the_entire_range, original_string, list_address)

    def get_the_full_numbers_inclusive(self, elem_list, the_entire_range):
        if elem_list[-1] == '(INCLUSIVE)':
            for j in range(int(elem_list[0]), int(elem_list[1]) + 1):
                the_entire_range.append(str(j))
        self.add_2_entire_range(elem_list, the_entire_range)

    @staticmethod
    def add_2_entire_range(elem_list, the_entire_range):
        if elem_list[-1] != '' and elem_list[-1] != '(INCLUSIVE)':
            for nb in elem_list:
                the_entire_range.append(str(nb))

    def add_last_element(self, the_entire_range, original_string, list_address):
        the_entire_range.append(original_string.split(' ')[-1])  # add the last element
        entire_range_length = len(the_entire_range)

        self.standardise_range(the_entire_range, entire_range_length, list_address)

    def standardise_range(self, the_entire_range, entire_range_length, list_address):
        index_start = []
        index_end = []

        for n in range(0, len(the_entire_range) - 1):
            if self.capital_letter.findall(the_entire_range[n]) and self.numbers.findall(the_entire_range[n - 1]):
                index_start.append(n)
            if self.capital_letter.findall(the_entire_range[n]) and self.numbers.findall(the_entire_range[n + 1]):
                index_end.append(n + 1)

        self.get_choice(the_entire_range, index_start, index_end, entire_range_length, list_address)

    def get_choice(self, the_entire_range, index_start, index_end, entire_range_length, list_address):
        choice = 0
        if len(index_start) > 2 or len(index_start) == 2:
            choice = len(index_start) - 1
        if len(index_start) == 1:
            choice = len(index_start)

        self.conditional_with_index_list_first_case_1(the_entire_range, index_start, index_end, choice,
                                                      entire_range_length, list_address)

    def conditional_with_index_list_first_case_1(self, the_entire_range, index_start, index_end, choice,
                                                 entire_range_length, list_address):
        for n in range(0, choice):
            if len(index_start) > 2:  # if there are more than 2 element in start_index_list
                if n == 0:
                    the_entire_range[index_start[n]:index_end[n]] = [
                        ' '.join(the_entire_range[index_start[n]:index_end[n]])]

                else:
                    self.conditional_with_index_list_second_case_1(the_entire_range, index_start, index_end, n)
                self.conditional_with_index_list_last_case_1(the_entire_range, index_start, index_end, n)
            self.conditional_with_index_list_first_case_2(the_entire_range, index_start, index_end, n,
                                                          entire_range_length)
            self.conditional_with_index_list_fisrt_case_3(the_entire_range, index_start, n, entire_range_length)
        self.group_by_street_name(the_entire_range, list_address)

    @staticmethod
    def conditional_with_index_list_second_case_1(the_entire_range, index_start, index_end, n):
        try:
            the_entire_range[index_start[n] - n:index_end[n] - n] = [
                ' '.join(the_entire_range[index_start[n] - n:index_end[n] - n])]
        except:
            pass
            # print(colored('Execption: line 406, ', 'red'), the_entire_range)

    @staticmethod
    def conditional_with_index_list_last_case_1(the_entire_range, index_start, n, entire_range_length):
        if n == len(index_start) - 2:
            # print(colored(n+1, 'blue'))
            t = (entire_range_length - 1) - index_start[n + 1]
            the_entire_range[index_start[n + 1] - t:entire_range_length] = [
                ' '.join(the_entire_range[index_start[n + 1] - t:entire_range_length])]

    def conditional_with_index_list_first_case_2(self, the_entire_range, index_start, index_end, n,
                                                 entire_range_length):
        if len(index_start) == 2:  # if there are only one element in start_index_list
            if n == 0:
                try:
                    the_entire_range[index_start[n]:index_end[n]] = [
                        ' '.join(the_entire_range[index_start[n]:index_end[n]])]
                except:
                    print(colored('Exception: conditional - index', 'red'), the_entire_range)
                self.conditional_with_index_list_first_case_2_bis(the_entire_range, index_start, n, entire_range_length)

    @staticmethod
    def conditional_with_index_list_first_case_2_bis(the_entire_range, index_start, n, entire_range_length):
        the_entire_range[index_start[n + 1] - 1:entire_range_length] = [
            ' '.join(the_entire_range[index_start[n + 1] - 1:entire_range_length])]

    @staticmethod
    def conditional_with_index_list_fisrt_case_3(the_entire_range, index_start, n, entire_range_length):
        if len(index_start) == 1:  # if there is only one element in start_index_list
            if n == 0:
                the_entire_range[index_start[n]:entire_range_length] = [
                    ' '.join(the_entire_range[index_start[n]:entire_range_length])]

    def group_by_street_name(self, the_entire_range, list_address):
        group_street_name = []
        temporary_list = []

        for elem in the_entire_range:
            temporary_list.append(elem)
            if self.capital_letter.findall(elem):
                group_street_name.append(temporary_list)
                temporary_list = []
        # print(colored(group_street_name, 'yellow'))
        self.join_street_name_with_numbers(group_street_name, list_address)

        return temporary_list

    def join_street_name_with_numbers(self, group_street_name, list_address):
        for elem_list in group_street_name:
            address_list = []
            # address_list.append(list_address[self.ow.Title_Number])
            for n in range(0, len(elem_list) - 1):
                # print(elem_list[n], elem_list[len(elem_list) - 1])
                join = elem_list[n] + ' ' + elem_list[len(elem_list) - 1]
                address_list.append(join)
        # self.all_odd_address_list.append(address_list)
        self.all_odd_address_list[list_address[self.ow.Title_Number]] = address_list
        return self.all_odd_address_list
        # print(address_list)

    def load_data(self, the_file):
        with open(the_file, 'r') as f:
            f.readline()
            for line in f:
                tl = line.replace('\n', '').upper().split('\t')
                self.standardise_data(tl)
                self.data.append(tl)

    def standardise_data(self, tl):
        pa = self.ow.Property_Address
        tl[pa] = tl[pa].replace('(EVEN)', '(ODD)').replace('(EVENS)', '(ODD)').replace('(EVEN NUMBERS)', '(ODD)').\
            replace('(EVENS ONLY)', '(ODD)').replace(' EVENS,', '(ODD),').replace(' EVENS ', ' (ODD) ')
        tl[pa] = tl[pa].replace('EVEN NUMBERS', '(ODD)').replace('(ODD NUMBERS)', '(ODD)').replace('(ODDS)', '(ODD)')
        tl[pa] = tl[pa].replace('(EVEN ONLY)', '(ODD)')
        self.inclusive_case_replacement(tl, pa)
        self.standardise_data2(tl, pa)
        return tl

    def inclusive_case_replacement(self, tl, pa):  # all inclusive replacement
        tl[pa] = re.sub('\(INC 32A\)', ' (INCLUSIVE), 32A', tl[pa])
        tl[pa] = tl[pa].replace('(EVENS INCLUSIVE)', '(ODD)').replace('(ODD INCLUSIVE)', '(ODD)')
        tl[pa] = tl[pa].replace('(CONSECUTIVE NUMBERS)', '(INCLUSIVE)').\
            replace('CONSECUTIVE NUMBERS)', '(INCLUSIVE)').\
            replace('(INC)', '(INCLUSIVE)').replace('(INCL)', '(INCLUSIVE)').replace('(INCL )', '(INCLUSIVE)')
        tl[pa] = re.sub(' INC ', '(INCLUSIVE)', tl[pa])
        tl[pa] = re.sub(' INC,', '(INCLUSIVE)', tl[pa])

    def standardise_data2(self, tl, pa):
        if self.space_dash.findall(tl[pa]) or self.dash_without_space.findall(tl[pa]):
            if 'INCLUSIVE' in tl[pa]:
                tl[pa] = self.space_dash.sub(r'\1 TO \2', tl[pa])  # remove space between dash
                tl[pa] = self.dash_without_space.sub(r'\1 TO \2', tl[pa])  # remove space between dash
            else:
                tl[pa] = self.space_dash.sub(r'\1-\2', tl[pa])  # remove space between dash
        # if self.postcode.findall(tl[pa]):  # retrieve address with postcode
        #     tl[pa] = self.postcode.sub('', tl[pa])
        #     print(tl)

        return tl

    def extract_land_and_other_items(self):
        tmp = []
        for address in self.data:
            if self.confirm_not_land_or_other(address):
                tmp.append(address)
        self.data[:] = tmp

    def confirm_not_land_or_other(self, address):
        for items in self.list_not_interested:
            if address[self.ow.Property_Address].startswith(items):
                return False
        return True

    @staticmethod
    def print_test_address(self, address, tl, title='SYK210490'):
        if address[self.st.title_number] == title:
            print(address[self.ow.Property_Address])
            print(tl)

    def simple_numbers_list2csv(self):
        lt = self.data
        # print(self.multiplicate_list)

        with open(self.st.data_simple_numbers + self.file, mode='w') as output_file:
            field = ['title_number', 'tenure', 'multiplicate', 'land', 'property_address', 'district', 'county',
                     'region', 'postcode', 'multiple_address_indicator', 'price_paid', 'proprietor_name_(1)',
                     'company_registration_no_(1)', 'proprietorship_category_(1)', 'proprietor_(1)_address_(1)',
                     'proprietor_(1)_address_(2)', 'proprietor_(1)_address_(3)', 'proprietor_name_(2)',
                     'company_registration_no_(2)', 'proprietorship_category_(2)', 'proprietor_(2)_address_(1)',
                     'proprietor_(2)_address_(2)', 'proprietor_(2)_address_(3)', 'proprietor_name_(3)',
                     'company_registration_no_(3)', 'proprietorship_category_(3)', 'proprietor_(3)_address_(1)',
                     'proprietor_(3)_address_(2)', 'proprietor_(3)_address_(3)', 'proprietor_name_(4)',
                     'company_registration_no_(4)', 'proprietorship_category_(4)', 'proprietor_(4)_address_(1)',
                     'proprietor_(4)_address_(2)', 'proprietor_(4)_address_(3)', 'date_proprietor_added',
                     'additional_proprietor_indicator']

            output_writer = csv.writer(output_file, delimiter='\t')
            output_writer.writerow(field)

            for list_address in lt:
                if list_address[self.ow.Title_Number] in self.multiplicate_list:
                    for address in self.multiplicate_list[list_address[self.ow.Title_Number]]:
                        list_address[self.ow.Property_Address] = address
                        try:
                            output_writer.writerow(list_address)
                        except:
                            # pass
                            print(colored('Exception: ', 'red'), list_address)
                # try:
                #     output_writer.writerow(list_address)
                # except:
                #     pass
                    # print(colored('Exception: ', 'red'), dictio)

    def odd_even_inclusive_numbers2csv(self):
        lt = self.data
        # for address in lt:
        #     if "INC" in address[self.ow.Property_Address]:
        #         print(address[self.ow.Title_Number], address[self.ow.Property_Address])

        with open(self.st.data_odd_numbers + self.file, mode='w') as output_file:
            field = ['title_number', 'tenure', 'multiplicate', 'land', 'property_address', 'district', 'county',
                     'region', 'postcode', 'multiple_address_indicator', 'price_paid', 'proprietor_name_(1)',
                     'company_registration_no_(1)', 'proprietorship_category_(1)', 'proprietor_(1)_address_(1)',
                     'proprietor_(1)_address_(2)', 'proprietor_(1)_address_(3)', 'proprietor_name_(2)',
                     'company_registration_no_(2)', 'proprietorship_category_(2)', 'proprietor_(2)_address_(1)',
                     'proprietor_(2)_address_(2)', 'proprietor_(2)_address_(3)', 'proprietor_name_(3)',
                     'company_registration_no_(3)', 'proprietorship_category_(3)', 'proprietor_(3)_address_(1)',
                     'proprietor_(3)_address_(2)', 'proprietor_(3)_address_(3)', 'proprietor_name_(4)',
                     'company_registration_no_(4)', 'proprietorship_category_(4)', 'proprietor_(4)_address_(1)',
                     'proprietor_(4)_address_(2)', 'proprietor_(4)_address_(3)', 'date_proprietor_added',
                     'additional_proprietor_indicator']

            output_writer = csv.writer(output_file, delimiter='\t')
            output_writer.writerow(field)

            # print(self.all_odd_address_list)
            for list_address in lt:
                if list_address[self.ow.Title_Number] in self.all_odd_address_list:
                    for address in self.all_odd_address_list[list_address[self.ow.Title_Number]]:
                        list_address[self.ow.Property_Address] = address
                        try:
                            output_writer.writerow(list_address)
                        except:
                            print(colored('Exception: ', 'red'), list_address)

    @staticmethod
    def remove_redundant(path, name):
        pd.set_option('display.max_columns', 40)
        df = pd.read_csv(path + name, delimiter='\t')
        df.drop_duplicates(inplace=True)
        df.to_csv(path + 'clean_' + name, sep='\t', index=None)


if __name__ == '__main__':
    fg = Main()
    fg.start_commercial_ownership('/media/pc2/Backup/Stage_doorda/property_product/address/data/0_raw/'
                                  'all_1_CCOD_FULL_2019_05.tsv')

    fg.simple_numbers_list2csv()
    fg.odd_even_inclusive_numbers2csv()

    fg.remove_redundant('/media/pc2/Backup/Stage_doorda/property_product/address/data/output/simple_numbers/',
                        '1_CCOD_FULL_2019_05.csv')
    fg.remove_redundant('/media/pc2/Backup/Stage_doorda/property_product/address/data/output/odd_numbers/',
                        '1_CCOD_FULL_2019_05.csv')
