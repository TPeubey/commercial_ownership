from library import structure
import re
from termcolor import colored
import itertools
import pandas as pd
import csv
import string
import time


class Main:

    def __init__(self):
        # regular expression:

        # for multiplicate numbers
        self.multiplicate_nb = re.compile(r'\b(\d+[A-Z]?-\d+[A-Z]?)\b|'
                                          r'\b(\d+[A-Z]? - \d+[A-Z]?)\b|'
                                          r'\b(\d+[A-Z]?\/\d+[A-Z]?)\b|'
                                          r'\b(\d+[A-Z]?)\b')
        self.get_num = re.compile(r'^[A-Z]+|^\(|\)$|[A-Z]{1,2}\d{1,2}[A-Z]?|\d[A-Z]{2}')

        # for odd and inclusive numbers part
        self.sub1 = re.compile(r'(\d+)TO')
        self.sub2 = re.compile(r'TO(\d+)')
        self.capital_letter = re.compile(r'[A-Z]+')
        self.capital_letter_word = re.compile(r'^[A-Z]+')
        self.number_capital_letter = re.compile(r'^\d+[A-Z]')
        self.numbers = re.compile(r'\d+')
        self.entire_numbers = re.compile(r'^\d+$')
        self.start_parenthese = re.compile(r'^(\()')
        self.end_parenthese_or_odd = re.compile(r'(\))$|(\)\.)$')
        self.flat_inclusive = re.compile(r'(FLAT \d+ TO FLAT \d+)|(FLAT [A-Z] TO FLAT [A-Z])')
        self.unit_inclusive = re.compile(r'(UNIT \d+ TO UNIT \d+)|(UNIT [A-Z] TO UNIT [A-Z])')
        self.dash_numbers = re.compile(r'\d+-\d+')
        self.multiple_space = re.compile(r'\s+')
        self.only_letters = re.compile(r'^[A-Z]+$')
        self.numbers_index_start_end = re.compile(r'(^\d+$)|(^\d+-\d+$)|(^\d+[A-Z]$)')
        self.word_index_start = re.compile(r'(^[A-Z]+)|(^\()|(\)$)')
        self.word_index_end = re.compile(r'(^[A-Z]+)|(^\()|(\)$)|(^\d[A-Z]{2})')
        self.retrieve_second_part_pstc = re.compile(r'^\d[A-Z]{2}$')

        # used for normalised the data 1
        self.tight_dash_odd = re.compile('(\d+-\d+)\(ODD\)')
        self.tight_dash_right_odd = re.compile(r'(\d+) -(\d+) \(ODD\)')
        self.space_dash_odd = re.compile('(\d+) - (\d+) \(ODD\)')

        # used for normalised the data 2
        self.tight_dash_inclusive = re.compile(r'(\d+)-(\d+) INCLUSIVE')
        self.tight_dash_inclusive_bracket = re.compile('(\d+-\d+)\(INCLUSIVE\)')
        self.tight_nb_inclusive = re.compile(r'(\d+)\(INCLUSIVE\)')
        self.flat_inclusive_normalized = re.compile(r'L?FLATS (\d+) TO (\d+) \(INCLUSIVE\)')
        self.inclusive_letter = re.compile(r'\(INCLUSIVE\)([A-Z]+)')

        # used for normalised the data 3
        self.postcode_digit = re.compile(r'(\([A-Z]{1,2}\d{1,2}[A-Z]?\s\d[A-Z]{2}\))(\d+)')
        self.parenthese_postcode = re.compile(r'(\()(\([A-Z]{1,2}\d{1,2}[A-Z]?\s\d[A-Z]{2}\))')
        self.inv_parenthese_postcode = re.compile(r'(\))([A-Z]{1,2}\d{1,2}[A-Z]?\s\d[A-Z]{2}\))')
        self.tight_dash_right_inclusive = re.compile(r'(\d+) -(\d+) \(INCLUSIVE\)')
        self.space_dash_inclusive = re.compile(r'(\d+) - (\d+) \(INCLUSIVE\)')
        self.space_dash = re.compile(r'(\d+) - (\d+)')
        self.tight_dash_left = re.compile(r'(\d+)- (\d+)')
        self.tight_dash_right = re.compile(r'(\d+) -(\d+)')

        # used for normalised the data 4
        self.remove_formerly = re.compile(r'\(FORMERLY [A-Z0-9\s]+\)\,?\s?')
        self.remove_land_side_of = re.compile(r'LAND [A-Z\s]+ OF\s?')
        self.remove_plot = re.compile(r'PLOT\s?\d*[A-Z]*\s?')
        self.remove_site = re.compile(r'SITE\s?\d*[A-Z]*\s?')

        self.ow = structure.CommercialOwnershipStructure()
        self.st = structure.CommercialOwnership()
        self.st.start_address()
        self.data = []
        self.list_not_interested = ['LAND AND', 'LAND AT', 'SITES OF', 'PUMPING STATION', 'BEING LAND',
                                    'LAND TO', 'LAND IN', 'LAND LYING', 'PART OF ', 'PARTS OF',
                                    'LAND ADJOINING', 'THE AIRSPACE', 'LAND ON', 'LAND FORMING',
                                    'THE SITES', 'LAND FRONTING', 'ON THE', 'THE SITE', 'ALL THE',
                                    'PORTIONS ', 'LAND BEING', 'PLOTS', 'STORAGE', 'LAND COMPRISING',
                                    'LAND FORMERLY', 'PLOT']
        self.file = '1_CCOD_FULL_2019_05.csv'

        # all simple numbers and odd list

        self.multiplicate_list = {}
        self.all_odd_address_list = {}

        # simplification name for address
        self.pa = self.ow.Property_Address

        self.alphabet_dict = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'H',
                              11: 'I', 12: 'J', 13: 'K', 14: 'L', 15: 'M'}

    def start_commercial_ownership(self, the_file):
        self.load_data(the_file)
        if not self.check_other_data():
            self.standardise_data(self.data)
            self.standardise_data2(self.data)
            self.standardise_data3(self.data)
            self.standardise_data4(self.data)

            self.extract_land_and_other_items()
            self.find_multiplication(self.data)

    def check_other_data(self):
        for line in self.data:
            if self.determine_if_two_addresses_using_and(line):
                return True
        return False

    def find_multiplication(self, data):
        """
        This is a function conditionnal:
        - if the address contains odd number it returns a function to deal with it
        - otherwise it returns another function to deal with multiplicate numbers
        :param data:
        :return: Boolean
        """

        odd = False
        for list_address in data:
            # if list_address[0] == 'CYM39140':
                # print(list_address[self.pa])

            # deal with odd/even numbers
            if "(ODD)" in list_address[self.pa] or "(INCLUSIVE)" in list_address[self.pa]:
                odd = True
                self.deal_with_odd_and_even(list_address)

            # deal with simple numbers
            else:  # directly take all address without odd or inclusive
                if len(self.multiplicate_nb.findall(list_address[self.pa])) > 1 \
                        and 'APARTMENT' not in list_address[self.pa]:  # multiple number
                    self.deal_with_multiple_nb(list_address)
                else:  # get the simple address
                    pass
                    # print(list_address[self.ow.Title_Number], list_address[self.pa])

        return odd

    def deal_with_multiple_nb(self, list_address):
        s1 = list_address[self.pa]
        s1 = re.sub(r'\bAND\b', r'', s1)
        s1 = s1.replace(',', ' ').replace('INCLUSIVE', '').strip()
        s1 = self.multiple_space.sub(r' ', s1)  # normalised space
        s1 = s1.split(' ')
        # print(list_address[self.ow.Title_Number], list_address[self.pa])
        self.get_inclusive_missing(s1, list_address)

    def get_inclusive_missing(self, s1, list_address):
        """
        This function get the inslusive missing from the multiple numbers
        :param s1:
        :param list_address:
        :return:
        """
        if 'TO' in s1 and re.findall(r'\d+[A-Z]?',
                                     s1[s1.index('TO') - 1]):  # check there is TO and precedent element is nb
            # print(list_address[self.ow.Title_Number], colored(s1, 'blue'))  # DN340787
            try:
                self.add_inclusive(s1, list_address)
            except:
                print(colored('Exception: ', 'red'), s1)
        else:  # get the multiple number
            self.get_index_street_name(s1, list_address)
            self.group_numbers(s1, list_address)

    def get_index_street_name(self, s1, list_address):
        #print(list_address[self.ow.Title_Number], colored(s1, 'blue'))
        temporary_group_list = []
        new_address = []
        join_street_name = ''

        for idx, elem in enumerate(s1):
            if self.get_num.findall(elem):
                temporary_group_list.append(elem)
                join_street_name = ' '.join(temporary_group_list)
                if s1[idx] == s1[-1]:
                    # print(join_street_name)
                    new_address.append(join_street_name)
            else:
                # print(join_street_name)
                if join_street_name != '':
                    new_address.append(join_street_name)
                new_address.append(elem)
                temporary_group_list = []  # reinitialize the temporary list when 'elem' is a number
                join_street_name = ''  # reinitialize the street name
                # print(colored(elem, 'red'))

            # if s1[idx] == s1[-1]:
            #     print(new_address)

    def determine_if_two_addresses_using_and(self, line):
        num = re.findall(r'[A-Z]+S \d+ & \d+', line[self.pa])
        num2 = re.findall(r'ODD|INCLUSIVE', line[self.pa])
        if num and not num2:
            self.deal_if_two_addresses_using_and(line)

            return True
        return False

    def deal_if_two_addresses_using_and(self, line):
        print(colored(line[self.pa], 'blue'))
        s1 = line[self.pa]
        s1 = re.sub(r'\bAND\b', r'', s1)
        s1 = s1.replace(',', ' ').strip()
        s1 = self.multiple_space.sub(r' ', s1)  # normalised space
        s1 = s1.split('&')
        s1[0] = s1[0].strip()
        s1[1] = s1[1].strip()
        self.deal_if_two_addresses_using_and2(s1, line)

    def deal_if_two_addresses_using_and2(self, s1, line):
        get_numbers = []
        street_name = ''
        for idx, elem in enumerate(s1):
            if idx == 0:
                first_word = elem.split(' ')[0]
                get_numbers.append(elem.split(' ')[1])  # retrieve the number
            if idx == 1:
                get_numbers.append(elem.split(' ')[0])
                street_name = elem.split(' ', 1)[1]
            self.deal_if_two_addresses_using_and2_join(first_word, get_numbers, street_name, line)

    def deal_if_two_addresses_using_and2_join(self, first_word, get_numbers, street_name, line):
        for k in range(0, len(get_numbers)):
            if len(get_numbers) == 2:
                join_and = first_word + ' ' + str(get_numbers[k]) + ' ' + street_name
                print(join_and)
            self.multiplicate_list[line[self.ow.Title_Number]] = temporary_list

    def group_numbers(self, s1, list_address):
        """
        This function group multiple numbers
        :param s1:
        :param list_address:
        :return:
        """
        temporary_list = []
        group_numbers = []
        for idx, elem in enumerate(s1):
            if self.multiplicate_nb.findall(elem):
                temporary_list.append(elem)
                s1[idx] = ''
            if self.capital_letter_word.findall(elem) and temporary_list != []:
                group_numbers.append(temporary_list)
                # self.multiplicate_list[list_address[self.ow.Title_Number]] = group_numbers
                temporary_list = []  # reinitilize the list
        self.group_street_name_multiple_nb(group_numbers, s1, list_address)
        # print(self.multiplicate_list)

    def group_street_name_multiple_nb(self, group_numbers, s1, list_address):
        """
        This function group the street name by list
        :param group_numbers:
        :param s1:
        :param list_address:
        :return:
        """
        temporary_list = []
        group_street_name = []

        for elem in s1:
            # last condition retrieve the second part of the postcode
            if self.capital_letter_word.findall(elem) or elem.startswith('(') or elem.endswith(')') \
                    or self.retrieve_second_part_pstc.findall(elem):
                temporary_list.append(elem)
                group_street_name.append(temporary_list)
            if elem == '':
                temporary_list = []
        self.remove_redundant_and_join_street_name(group_numbers, group_street_name, list_address)

    def remove_redundant_and_join_street_name(self, group_numbers, group_street_name, list_address):
        """
        The group street name list, has redundant in previous method, this function remove them
        :param group_numbers:
        :param group_street_name:
        :param list_address:
        :return:
        """
        group_street_name = list(the_range for the_range, _ in itertools.groupby(group_street_name))

        for idx, elem_list in enumerate(group_street_name):
            group_street_name[idx] = ' '.join(group_street_name[idx])
        self.join_nb_to_street_name(group_numbers, group_street_name, list_address)

    def join_nb_to_street_name(self, group_numbers, group_street_name, list_address):
        """
        This function join the numbers with street name
        :param group_numbers:
        :param group_street_name:
        :param list_address:
        :return:
        """
        if len(group_numbers) == len(group_street_name):
            # print(list_address[self.ow.Title_Number], colored(list_address[self.pa], 'blue'))
            # print(group_numbers, group_street_name)
            temporary_list = []
            for k in range(0, len(group_numbers)):
                for l in range(0, len(group_numbers[k])):
                    join = group_numbers[k][l] + ' ' + group_street_name[k]
                    temporary_list.append(join)
                    # print(list_address[self.ow.Title_Number], colored(join, 'green'), temporary_list)  # DN607364
                self.multiplicate_list[list_address[self.ow.Title_Number]] = temporary_list
        else:
            self.join_nb_to_street_name2(group_numbers, group_street_name, list_address)

    def join_nb_to_street_name2(self, group_numbers, group_street_name, list_address):
        """
        This function join the numbers with the street name
        :param group_numbers:
        :param group_street_name:
        :param list_address:
        :return:
        """
        if group_street_name[0] == 'FLAT' and len(group_numbers) == 2:
            join = group_street_name[0] + ' ' + str(group_numbers[0][0]) + ' ' + group_street_name[1] + ' ' + \
                   str(group_numbers[1][0]) + ' ' + group_street_name[2]
            self.multiplicate_list[list_address[self.ow.Title_Number]] = [join]
            # print(list_address[self.ow.Title_Number], colored(join, 'blue'))
        # print(self.multiplicate_list)
        else:
            self.join_nb_to_street_name3(group_numbers, group_street_name, list_address)

    def join_nb_to_street_name3(self, group_numbers, group_street_name, list_address):
        """
        This function join the numbers with the street name
        :param group_numbers:
        :param group_street_name:
        :param list_address:
        :return:
        """
        if len(group_numbers) == 1 and len(group_numbers[0]) == 2:
            join2 = group_street_name[0] + ' ' + group_numbers[0][0] + ', ' + group_numbers[0][1] + ' ' + group_street_name[1]
            self.multiplicate_list[list_address[self.ow.Title_Number]] = [join2]
        else:
            if len(group_numbers[0]) > 2 and len(group_street_name) == 2:
                # print(list_address[self.ow.Title_Number], colored(group_numbers, 'blue'), colored(group_street_name, 'blue'))
                temporary_join3_list = []
                for k in range(0, len(group_numbers[0])):
                    join3 = group_street_name[0] + ' ' + str(group_numbers[0][k]) + ' ' + group_street_name[1]
                    temporary_join3_list.append(join3)
                    self.multiplicate_list[list_address[self.ow.Title_Number]] = temporary_join3_list
            else:
                self.join_nb_to_street_name4(group_numbers, group_street_name, list_address)

    def join_nb_to_street_name4(self, group_numbers, group_street_name, list_address):
        """
        This function join the numbers with the street name
        :param group_numbers:
        :param group_street_name:
        :param list_address:
        :return:
        """
        if len(group_street_name) > 2:
            self.join_nb_to_street_name6(group_numbers, group_street_name, list_address)
        else:
            if len(group_street_name) == 1 or (len(group_street_name) == 2 and group_street_name[1].startswith('(')):
                group_street_name = [' '.join(group_street_name)]  # join the postcode the the street name
                self.join_nb_to_street_name4_bis(group_numbers, group_street_name, list_address)
            else:
                self.join_nb_to_street_name5(group_numbers, group_street_name, list_address)

    def join_nb_to_street_name4_bis(self, group_numbers, group_street_name, list_address):
        """
        This function join the numbers with the street name
        :param group_numbers:
        :param group_street_name:
        :param list_address:
        :return:
        """
        temporary_join4_bis_list = []
        for k in range(0, len(group_numbers)):
            for l in range(0, len(group_numbers[k])):
                try:
                    join4_bis = group_numbers[k][l] + ' ' + group_street_name[0]
                    temporary_join4_bis_list.append(join4_bis)
                    self.multiplicate_list[list_address[self.ow.Title_Number]] = temporary_join4_bis_list
                except:
                    print(colored('Exception', 'red'), join4_bis)

    def join_nb_to_street_name5(self, group_numbers, group_street_name, list_address):
        """
        This function join the numbers with the street name
        :param group_numbers:
        :param group_street_name:
        :param list_address:
        :return:
        """
        temporary_join5_list = []
        try:
            for k in range(0, len(group_numbers)):
                for l in range(0, len(group_numbers[k])):
                    join5 = group_street_name[0] + ' ' + group_numbers[k][l] + ' ' + group_street_name[1]
                    temporary_join5_list.append(join5)
                    self.multiplicate_list[list_address[self.ow.Title_Number]] = temporary_join5_list
        except:
            print(colored('Exception: ', 'red'), list_address[self.ow.Title_Number], join5)

    def join_nb_to_street_name6(self, group_numbers, group_street_name, list_address):
        """
        This function join the numbers with the street name
        :param group_numbers:
        :param group_street_name:
        :param list_address:
        :return:
        """
        if len(group_street_name) == 3 and len(group_numbers[0]) == 2:
            temporary_join6_list = []
            for k in range(0, len(group_numbers[0])):
                for l in range(0, len(group_numbers[1])):
                    try:
                        join6 = group_street_name[0] + ' ' + group_numbers[0][k] + ' ' + group_street_name[1] + ' ' + \
                                group_numbers[1][l] + ' ' + group_street_name[2]
                        temporary_join6_list.append(join6)
                        self.multiplicate_list[list_address[self.ow.Title_Number]] = temporary_join6_list
                    except:
                        print(colored('Exception: ', 'red'), list_address[self.ow.Title_Number], join6)
        self.join_nb_to_street_name7(group_numbers, group_street_name, list_address)

    def join_nb_to_street_name7(self, group_numbers, group_street_name, list_address):
        """
        This function join the numbers with the street name
        :param group_numbers:
        :param group_street_name:
        :param list_address:
        :return:
        """
        # print(list_address[self.ow.Title_Number], colored(group_numbers, 'green'),
        #       colored(group_street_name, 'blue'))
        try:
            temporary_join7_list = []
            for k in range(0, len(group_numbers)):
                if k == 0:
                    join = group_street_name[k] + ' ' + group_numbers[0][k] + ' ' + group_street_name[k + 1]
                    temporary_join7_list.append(join)
                if k > 0:
                    for l in range(0, len(group_numbers[k])):
                        join7 = str(group_numbers[k][l]) + ' ' + group_street_name[k + 1]
                        temporary_join7_list.append(join7)
            self.multiplicate_list[list_address[self.ow.Title_Number]] = temporary_join7_list
        except:
            print(colored('Exception: ', 'red'), list_address[self.ow.Title_Number], join)

    def add_inclusive(self, s1, list_address):
        """
        This function add the address when there is a 'TO' clause and returns to the method:
        - deal_with_odd_and_even
        :param s1:
        :param list_address:
        :return:
        """
        if s1[s1.index('TO') + 1] == 'FLAT':
            del s1[s1.index('TO') + 1]
            s1.insert(s1.index('TO') + 2, '(INCLUSIVE)')
            list_address[self.pa] = ' '.join(s1)
            self.deal_with_odd_and_even(list_address)
        else:
            s1.insert(s1.index('TO') + 2, '(INCLUSIVE)')
            # print(list_address[self.ow.Title_Number], colored(s1, 'green'))  # DN340787
            self.deal_with_odd_and_even(list_address)

    def deal_with_odd_and_even(self, list_address):
        """
        This function manage some replacement for ODD numbers
        :param list_address:
        :return: address
        """

        list_address[self.pa] = self.sub1.sub(r'\1 TO', list_address[self.pa])
        list_address[self.pa] = self.sub2.sub(r'TO \1', list_address[self.pa])

        if self.flat_inclusive.findall(list_address[self.pa]):
            self.deal_with_flat(list_address)
            # print(list_address[self.pa])
        if self.unit_inclusive.findall(list_address[self.pa]):
            self.deal_with_unit(list_address)
            # print(list_address[self.pa])
        else:
            self.get_the_numbers_odd(list_address[self.pa], list_address)

        return list_address[self.pa]

    def deal_with_unit(self, list_address):
        """
        Retrieve 'UNIT' word in address and deal with it in the next function
        :param list_address:
        :return:
        """
        the_unit_range = []
        unit_address = list_address[self.pa].replace(',', '').split(' ')
        if 'UNIT' in unit_address:
            # print(unit_address)
            self.get_numbers_for_unit(the_unit_range, unit_address)
        self.get_entire_range_for_unit(the_unit_range, unit_address, list_address)
            # print(colored(unit_address, 'blue'))

    def get_numbers_for_unit(self, the_unit_range, unit_address):
        """
        This function retrieve the range when there is 'UNIT' WORD
        :param the_unit_range:
        :param unit_address:
        :return:
        """
        for i in range(0, len(unit_address)):  # retrieve numbers and if inclusive or odd
            if unit_address[i] == 'UNIT':
                the_unit_range.append(unit_address[i + 1])
                unit_address[i] = ''
                unit_address[i + 1] = ''
            if unit_address[i] == '(INCLUSIVE)':
                the_unit_range.append(unit_address[i])
                unit_address[i] = ''
                unit_address[i + 1] = ''
            if unit_address[i] == 'TO':
                unit_address[i] = ''

    def get_entire_range_for_unit(self, the_unit_range, unit_address, list_address):
        """
        This function get the entire range for inclusive
        :param the_unit_range:
        :param unit_address:
        :param list_address:
        :return:
        """
        the_entire_unit_range = []
        full_unit_address_list = []
        # print(the_flat_range, colored(flat_address, 'blue'))
        try:
            if float(the_unit_range[0]).is_integer() \
                    and the_unit_range[2] == '(INCLUSIVE)':  # check if it is a numbers in the range
                for k in range(int(the_unit_range[0]), int(the_unit_range[1]) + 1):
                    the_entire_unit_range.append(k)
            # print(the_entire_unit_range)
        except:
            self.deal_with_letter_for_unit(the_entire_unit_range, the_unit_range, unit_address, list_address)
        self.group_street_name_add_nb_for_unit(full_unit_address_list, the_entire_unit_range, unit_address,
                               list_address)

    def deal_with_letter_for_unit(self, the_entire_unit_range, the_unit_range, unit_address, list_address):
        """
        This function deal when there is letter in the range for 'UNIT' word
        :param the_entire_unit_range:
        :param the_unit_range:
        :param unit_address:
        :param list_address:
        :return:
        """
        if isinstance(the_unit_range[0], str):  # check if it is a character
            for k in range(string.ascii_lowercase.index(the_unit_range[0].lower()),
                           string.ascii_lowercase.index(the_unit_range[1].lower()) + 1):
                the_entire_unit_range.append(self.alphabet_dict[k])

    def group_street_name_add_nb_for_unit(self, full_unit_address_list, the_entire_unit_range, unit_address,
                               list_address):
        """
        This function:
        - Group the street name
        - Join the numbers UNIT with the right street name
        :param full_unit_address_list:
        :param the_entire_unit_range:
        :param unit_address:
        :param list_address:
        :return:
        """
        join_unit_address = ' '.join(unit_address).strip()
        for k in range(0, len(the_entire_unit_range)):
            full_unit_address = 'UNIT ' + str(the_entire_unit_range[k]) + ' ' + join_unit_address
            full_unit_address_list.append(full_unit_address)
        self.all_odd_address_list[list_address[self.ow.Title_Number]] = full_unit_address_list
        # print(self.all_flat_address_list)

    def deal_with_flat(self, list_address):
        """
        This function deal with flat
        :param list_address:
        :return:
        """
        the_flat_range = []
        flat_address = list_address[self.pa].replace(',', '').split(' ')
        if 'FLAT' in flat_address:
            # print(flat_address)
            self.get_numbers_for_flat(the_flat_range, flat_address, list_address)
        self.get_entire_range(the_flat_range, flat_address, list_address)
        # print(flat_address)
        return flat_address

    def get_numbers_for_flat(self, the_flat_range, flat_address, list_address):
        """
        This function retrieve the range
        :param the_flat_range:
        :param flat_address:
        :param list_address:
        :return:
        """
        for i in range(0, len(flat_address)):  # retrieve numbers and if inclusive or odd
            if flat_address[i] == 'FLAT':
                the_flat_range.append(flat_address[i + 1])
                flat_address[i] = ''
                flat_address[i + 1] = ''
            if flat_address[i] == '(INCLUSIVE)' or flat_address[i] == '(ODD)':
                the_flat_range.append(flat_address[i])
                flat_address[i] = ''
                flat_address[i + 1] = ''
            if flat_address[i] == 'TO':
                flat_address[i] = ''

    def get_entire_range(self, the_flat_range, flat_address, list_address):
        """
        This function get the full number from inclusive or odd numbers
        :param the_flat_range:
        :param flat_address:
        :param list_address:
        :return:
        """
        the_entire_flat_range = []
        idx_start_list = []
        full_flat_address_list = []
        # print(the_flat_range, colored(flat_address, 'blue'))
        try:
            if float(the_flat_range[0]).is_integer() \
                    and the_flat_range[2] == '(INCLUSIVE)':  # check if it is a numbers in the range
                # print(the_flat_range, colored(flat_address, 'blue'))
                for k in range(int(the_flat_range[0]), int(the_flat_range[1]) + 1):
                    the_entire_flat_range.append(k)
            if float(the_flat_range[0]).is_integer() \
                    and the_flat_range[2] == '(ODD)':  # check if it is a numbers in the range
                # print(the_flat_range, colored(flat_address, 'blue'))
                for k in range(int(the_flat_range[0]), int(the_flat_range[1]) + 1, 2):
                    the_entire_flat_range.append(k)
        except:
            self.deal_with_letter(the_entire_flat_range, the_flat_range, flat_address, list_address)
        self.group_street_name(full_flat_address_list, idx_start_list, the_entire_flat_range, flat_address,
                               list_address)
        # print(flat_address, colored(full_flat_address_list, 'red'), list_address[self.pa])

    def deal_with_letter(self, the_entire_flat_range, the_flat_range, flat_address, list_address):
        """
        This function deal with the letter when this is not numbers
        :param the_entire_flat_range:
        :param the_flat_range:
        :param flat_address:
        :param list_address:
        :return:
        """
        if isinstance(the_flat_range[0], str):  # check if it is a character
            for k in range(string.ascii_lowercase.index(the_flat_range[0].lower()),
                           string.ascii_lowercase.index(the_flat_range[1].lower()) + 1):
                the_entire_flat_range.append(self.alphabet_dict[k])

    def group_street_name(self, full_flat_address_list, idx_start_list, the_entire_flat_range, flat_address,
                          list_address):
        """
        This function group the street name for flat when there is an 'AND' word
        :param full_flat_address_list:
        :param idx_start_list:
        :param the_entire_flat_range:
        :param flat_address:
        :param list_address:
        :return:
        """
        if not 'AND' in flat_address:
            for k in range(0, len(flat_address)):
                if self.capital_letter.findall(flat_address[k]) and flat_address[k - 1] == '':
                    idx_start_list.append(k)
            flat_address[idx_start_list[0]:len(flat_address)] = \
                [' '.join(flat_address[idx_start_list[0]:len(flat_address)])]
            self.join_number_to_street_name_with_and(full_flat_address_list, the_entire_flat_range, flat_address,
                                                     list_address)

        if 'AND' in flat_address:
            self.normalize_street_name_with_no_and(flat_address, the_entire_flat_range, list_address)

    def normalize_street_name_with_no_and(self, flat_address, the_entire_flat_range, list_address):
        flat_address_join = ' '.join(flat_address).strip()  # normalize extremite white space
        flat_address_join = self.multiple_space.sub(' ', flat_address_join)  # normalize white space
        flat_address_join = flat_address_join.split('AND')
        flat_address_join = [x.strip() for x in flat_address_join]
        # print(list_address[self.ow.Title_Number], flat_address_join, colored(the_entire_flat_range, 'red'))
        self.join_number_to_street_name_with_no_and(flat_address_join, the_entire_flat_range, list_address)

    def join_number_to_street_name_with_no_and(self, flat_address_join, the_entire_flat_range, list_address):
        """
        This function join all the number with the right street name
        :param flat_address_join:
        :param the_entire_flat_range:
        :param list_address:
        :return:
        """
        full_specific_flat_address = []
        if 'UNIT' in flat_address_join[1]:  # specific case
            flat_address_join[1] = ''.join(flat_address_join[1].split('UNIT 2')).strip()
            flat_address_join.insert(1, 'UNIT 2')
            # print(flat_address_join)
            self.get_full_numbers(full_specific_flat_address, flat_address_join, the_entire_flat_range, list_address)

    def get_full_numbers(self, full_specific_flat_address, flat_address_join, the_entire_flat_range, list_address):
        """
        This function:
        - Deal one specific case when there is the wor 'UNIT'
        - Join the full numbers with street name
        :param full_specific_flat_address:
        :param flat_address_join:
        :param the_entire_flat_range:
        :param list_address:
        :return:
        """
        for k in range(0, 2):  # create for 'UNIT 1' and 'UNIT 2' case
            join_number_street = flat_address_join[k] + ' ' + flat_address_join[2]
            full_specific_flat_address.append(join_number_street)
        for k in range(0, len(the_entire_flat_range)):
            join_number_street = 'FLAT ' + str(the_entire_flat_range[k]) + ' ' + flat_address_join[2]
            full_specific_flat_address.append(join_number_street)
        self.all_odd_address_list[list_address[self.ow.Title_Number]] = full_specific_flat_address

    def join_number_to_street_name_with_and(self, full_flat_address_list, the_entire_flat_range, flat_address,
                                            list_address):
        """
        This function join numbers with street name
        :param full_flat_address_list:
        :param the_entire_flat_range:
        :param flat_address:
        :param list_address:
        :return:
        """
        flat_address = [x for x in flat_address if x]  # remove empty element
        # print(the_entire_flat_range, flat_address)

        for k in range(0, len(the_entire_flat_range)):
            # print(the_entire_flat_range[k], flat_address[0])
            full_flat_address = 'FLAT ' + str(the_entire_flat_range[k]) + ' ' + flat_address[0]
            full_flat_address_list.append(full_flat_address)
            # print(full_flat_address)
            self.all_odd_address_list[list_address[self.ow.Title_Number]] = full_flat_address_list

    def get_the_numbers_odd(self, original_string, list_address):
        """
        This function is split into sub function to get the range of the odd numbers
        :param original_string:
        :param list_address:
        :return: list
        """

        tm_unittest = []
        the_range = []
        tl = list_address[self.pa].split('(ODD)')

        for idx, item in enumerate(tl):
            index_list_next_to = []
            item = item.replace(',', ' ').replace('  ', ' ')
            tm = item.split(' ')
            tm_unittest.append(tm)

            self.retrieve_index_with_to(the_range, tm, index_list_next_to, list_address)
        self.flatten_list_of_element(the_range, original_string, list_address)

        return tm_unittest

    def retrieve_index_with_to(self, the_range, tm, index_list_next_to, list_address):
        """
        This function retrieve the index just after the word 'TO'
        :param the_range:
        :param tm:
        :param index_list_next_to:
        :return: list
        """

        for n in range(0, len(tm)):  # retrieve index of 'TO'
            if tm[n] == 'TO':
                index_list_next_to.append(n + 1)
        self.retrieve_index_with_dash(the_range, tm, index_list_next_to, list_address)

        return index_list_next_to

    def retrieve_index_with_dash(self, the_range, tm, index_list_next_to, list_address):
        """
        This function retrieve the index of number for dash numbers
        :param the_range:
        :param tm:
        :param index_list_next_to:
        :return: integer
        """

        temporary_list_single_odd = []
        street_name_list = []
        dash_exception_index = ''

        for n in range(0, len(tm)):  # retrieve index with dash
            if n == len(tm) - 2 and self.dash_numbers.findall(tm[n]):
                dash_exception_index = n
        self.retrieve_numbers_with_dash(temporary_list_single_odd, the_range, dash_exception_index, tm,
                                        index_list_next_to, street_name_list, list_address)

        return dash_exception_index

    def retrieve_numbers_with_dash(self, temporary_list_single_odd, the_range, dash_exception_index, tm,
                                   index_list_next_to, street_name_list, list_address):
        """
        This fuction retrieve the numbers for dash case with index numbers
        :param temporary_list_single_odd:
        :param the_range:
        :param dash_exception_index:
        :param tm:
        :param index_list_next_to:
        :param street_name_list:
        :return: list
        """
        dash_range = []

        for index, i in enumerate(tm[:-1]):  # retrieve odd/even number with 'to'
            if index == dash_exception_index:
                dash_range = i.split('-')
                dash_range.append('')
                for n in range(0, len(dash_range)):
                    the_range.append(dash_range)
                i = ''

            self.retrieve_numbers_with_to(temporary_list_single_odd, index, tm, the_range, i, index_list_next_to,
                                          street_name_list, list_address)
        return dash_range

    def retrieve_numbers_with_to(self, temporary_list_single_odd, index, tm, the_range, i, index_list_next_to,
                                 street_name_list, list_address):
        """
        This function retrieve all the number where there is a 'TO' clause and stock it in a list
        :param temporary_list_single_odd:
        :param index:
        :param tm:
        :param the_range:
        :param i:
        :param index_list_next_to:
        :param street_name_list:
        :param list_address:
        :return: list
        """

        if i == 'TO' and not self.capital_letter.findall(tm[index - 1]) and not \
                self.capital_letter_word.findall(tm[index + 1]):
            the_range.append([tm[index - 1], tm[index + 1], ''])
            # if list_address[self.ow.Title_Number] == 'WA79324':
            #     print(the_range)
            tm[index - 1] = ''
            tm[index] = ''
            tm[index + 1] = ''
            self.retrieve_if_odd_inclusive(temporary_list_single_odd, index, tm, the_range, list_address)
        self.skip_some_element(temporary_list_single_odd, index, tm, the_range, i, index_list_next_to,
                               street_name_list, list_address)
        # if list_address[self.ow.Title_Number] == 'CYM195243':
        #     # print(list_address[self.ow.Property_Address])
        #     print(the_range)

        # if list_address[self.ow.Title_Number] == 'WA97011':
        #     print(colored(the_range, 'blue'))

        return the_range

    def retrieve_if_odd_inclusive(self, temporary_list_single_odd, index, tm, the_range, list_address):
        """
        This function retrieve the '(INCLUSIVE)' clause for inclusive number
        :param temporary_list_single_odd:
        :param index:
        :param tm:
        :param the_range:
        :param list_address:
        :return:
        """
        inclusive_unittest = []

        if index + 2 < len(tm):
            if tm[index + 2] == '(INCLUSIVE)' or tm[index + 2] == '(INC)' or \
                    tm[index + 2] == '(EVEN)' or tm[index + 2] == '(ODD)':
                the_range[-1][2] = tm[index + 2]
                inclusive_unittest.append(index + 2)
                inclusive_unittest.append(tm[index + 2])
                tm[index + 2] = ''
        temporary_list_single_odd = []

        return inclusive_unittest

    def skip_some_element(self, temporary_list_single_odd, index, tm, the_range, i, index_list_next_to,
                          street_name_list, list_address):
        """
        This function skip some element, the number before the 'TO' clause and 'TO' and 'AND'
        :param temporary_list_single_odd:
        :param index:
        :param tm:
        :param the_range:
        :param i:
        :param index_list_next_to:
        :param street_name_list:
        :param list_address:
        :return: list
        """

        if tm[index + 1] == 'TO' or i == 'TO':  # skip the first odd number, ex: '2' TO 6
            i = ''
        if i == 'TO' or i == 'AND':  # skip the 'TO' and 'AND' words
            pass
            i = ''
        self.check_index(temporary_list_single_odd, index, the_range, i, index_list_next_to, street_name_list,
                         list_address)
        return tm

    def check_index(self, temporary_list_single_odd, index, the_range, i, index_list_next_to, street_name_list,
                    list_address):
        """
        This function remove the index if it match in the list of index
        :param temporary_list_single_odd:
        :param index:
        :param the_range:
        :param i:
        :param index_list_next_to:
        :param street_name_list:
        :param list_address:
        :return:
        """
        if index in index_list_next_to:  # check if the index correspond to the list index
            i = ''
        self.reinitialize_temporary_list(temporary_list_single_odd, the_range, i, street_name_list, list_address)

    def reinitialize_temporary_list(self, temporary_list_single_odd, the_range, i, street_name_list, list_address):
        """
        This function reinitialize the temporary list to an empty list
        :param temporary_list_single_odd:
        :param the_range:
        :param i:
        :param street_name_list:
        :param list_address:
        :return: list
        """
        if self.capital_letter.findall(i):  # reinitialize the temporary list when match with street name
            # if list_address[self.ow.Title_Number] == 'WA79324':
            #     print(i)
            temporary_list_single_odd = []
        self.get_simple_numbers(temporary_list_single_odd, the_range, i, street_name_list, list_address)

    def get_simple_numbers(self, temporary_list_single_odd, the_range, i, street_name_list, list_address):
        """
        This function retrieve the single number and add all them to the range
        :param temporary_list_single_odd:
        :param the_range:
        :param i:
        :param street_name_list:
        :param list_address:
        :return:
        """
        if self.numbers.findall(i) and not i.startswith('(') and not i.endswith(')'):
            temporary_list_single_odd = []
            temporary_list_single_odd.append(i)
            the_range.append(temporary_list_single_odd)
            # if list_address[self.ow.Title_Number] == 'WA79324':
            #     print(colored(temporary_list_single_odd, 'blue'))
            #     print(the_range)

            i = ''
        self.skip_some_element_2(the_range, i, street_name_list, list_address)

    def skip_some_element_2(self, the_range, i, street_name_list, list_address):
        """
        This function remove some word, '(INCLUSIVE)', '(ODD)', '(INC)'
        :param the_range:
        :param i:
        :param street_name_list:
        :return: list
        """
        if i == '(INCLUSIVE)' or i == '(ODD)' or i == '(INC)':  # skip some words
            i = ''

        self.add_element(the_range, i, street_name_list, list_address)

    # @staticmethod
    def add_element(self, the_range, i, street_name_list, list_address):
        """
        This function retrieve the street_name_list
        :param the_range:
        :param i:
        :param street_name_list:
        :return:
        """
        if i != '':
            the_range.append([i])
            street_name_list.append(i)
        # if list_address[self.ow.Title_Number] == 'WA40846':
        #     print(the_range)

    def flatten_list_of_element(self, the_range, original_string, list_address):
        """
        This function flattend the range because there are some redundant
        :param the_range:
        :param original_string:
        :param list_address:
        :return:
        """

        the_range = list(the_range for the_range, _ in itertools.groupby(the_range))
        self.get_the_full_numbers_odd(the_range, original_string, list_address)

        # if list_address[self.ow.Title_Number] == 'CYM24708':
        #     print(colored(the_range, 'blue'))

        return the_range

    def get_the_full_numbers_odd(self, the_range, original_string, list_address):
        """
        This function retrieve all the numbers between the odd range
        :param the_range:
        :param original_string:
        :param list_address:
        :return:
        """
        the_entire_range = []
        for elem_list in the_range:
            if elem_list[-1] == '':
                try:
                    if self.number_capital_letter.findall(elem_list[1]):  # deal when there is letter in the range
                        self.retrieve_when_letter_in_range_odd(elem_list, the_entire_range)
                    else:
                        for j in range(int(elem_list[0]), int(elem_list[1]) + 2, 2): # when only numbers in the range
                            the_entire_range.append(str(j))
                except:
                    print(colored('Exception: ', 'red'), list_address[self.ow.Title_Number], the_range)
            self.get_the_full_numbers_inclusive(elem_list, the_entire_range, list_address)
        self.add_last_element(the_entire_range, original_string, list_address)

    @staticmethod
    def retrieve_when_letter_in_range_odd(elem_list, the_entire_range):
        for j in range(int(elem_list[0]), int(elem_list[1][0:len(elem_list[1]) - 1]) + 2, 2):
            the_entire_range.append(str(j))
            if j == int(elem_list[1][0:len(elem_list[1]) - 1]):
                last = str(j) + elem_list[1][-1]
                the_entire_range.append(last)
        # print(colored(the_entire_range, 'green'))

    def get_the_full_numbers_inclusive(self, elem_list, the_entire_range, list_address):
        """
        This function retrieve all the numbers between the inclusive numbers
        :param elem_list:
        :param the_entire_range:
        :return:
        """
        # if list_address[self.ow.Title_Number] == 'CYM24708':
        #     print(the_entire_range)
        if elem_list[-1] == '(INCLUSIVE)':
            try:
                if self.number_capital_letter.findall(elem_list[1]):  # deal when there is letter in the range
                    self.retrieve_when_letter_in_range_inclusive( elem_list, the_entire_range)
                else:
                    for j in range(int(elem_list[0]), int(elem_list[1]) + 1):  # when only numbers in the range
                        the_entire_range.append(str(j))
            except:
                print(colored('Exception: ', 'red'), list_address[self.ow.Title_Number], the_entire_range)
        self.add_2_entire_range(elem_list, the_entire_range)

    @staticmethod
    def retrieve_when_letter_in_range_inclusive(elem_list, the_entire_range):
        for j in range(int(elem_list[0]), int(elem_list[1][0:len(elem_list[1]) - 1]) + 1):
            the_entire_range.append(str(j))
            if j == int(elem_list[1][0:len(elem_list[1]) - 1]):
                last = str(j) + elem_list[1][-1]
                the_entire_range.append(last)

    @staticmethod
    def add_2_entire_range(elem_list, the_entire_range):
        """
        This function retrieve all the entire range
        :param elem_list:
        :param the_entire_range:
        :return:
        """
        if elem_list[-1] != '' and elem_list[-1] != '(INCLUSIVE)':
            for nb in elem_list:
                the_entire_range.append(str(nb))

    def add_last_element(self, the_entire_range, original_string, list_address):
        """
        This function add the last element because, before, we have remove the last element
        :param the_entire_range:
        :param original_string:
        :param list_address:
        :return:
        """
        the_entire_range.append(original_string.split(' ')[-1])  # add the last element
        entire_range_length = len(the_entire_range)

        self.standardise_range(the_entire_range, entire_range_length, list_address)

    def standardise_range(self, the_entire_range, entire_range_length, list_address):
        """
        This function return function from some condition about two list of index.
        index_start is the index number when it is the first word of the street name
        index_end si the index number whe it is the last word of the street name
        :param the_entire_range:
        :param entire_range_length:
        :param list_address:
        :return: list
        """
        index_start = []
        index_end = []
        minus_list = []
        start_word_list = ['FLAT', 'FLATS', 'UNIT', 'UNITS', 'APARTMENT']

        if the_entire_range[0] in start_word_list or 'FLAT' in the_entire_range:
            pass
            # index_start.append(0)
        if self.capital_letter_word.findall(the_entire_range[0]) \
                and the_entire_range[0] not in start_word_list:
            index_start.append(0)
            # print(list_address[self.ow.Title_Number], the_entire_range)
        else:
            for i in range(0, len(the_entire_range) - 1):  # retrieve index_start and index_end
                # self.retrieve_index_start(index_start, the_entire_range)

    # def retrieve_index_start(self, index_start, the_entire_range):
                if i == 0:
                    if self.only_letters.findall(the_entire_range[i]):
                        index_start.append(i)
                if self.word_index_start.findall(the_entire_range[i]) \
                        and self.numbers_index_start_end.findall(the_entire_range[i - 1]):
                    # print(self.data[i - 1], 'index start: ', the_entire_range[i], i)
                    index_start.append(i)
                    # print('index start: ', index_start)

                if self.word_index_end.findall(the_entire_range[i]) \
                        and self.numbers_index_start_end.findall(the_entire_range[i + 1]):
                    # print('index end: ', self.data[i], self.data.index(the_entire_range[i]))
                    index_end.append(i + 1)
                    # print('index end: ', index_end)
            index_start = list(dict.fromkeys(index_start))  # remove redundant
            index_end.append(len(the_entire_range))  # add the last index in index_end

            # print(colored(list_address[self.pa], 'blue'))
            # print(list_address[self.ow.Title_Number], colored(the_entire_range, 'red'))

            self.get_values_to_be_substracted(index_start, index_end, minus_list, the_entire_range, list_address)

    def get_values_to_be_substracted(self, index_start, index_end, minus_list, the_entire_range, list_address):
        """
        This function get the values to substract the value in index list
        :param index_start: 
        :param index_end: 
        :param minus_list: 
        :param the_entire_range: 
        :param list_address: 
        :return: 
        """
        # print(index_start, index_end)
        for i in range(0, len(index_start)):  # get the values to be subtracted
            minus = (index_end[i] - index_start[i]) - 1
            minus_list.append(minus)
        # print(colored(minus_list, 'blue'))

        self.update_index_list(index_start, index_end, minus_list, the_entire_range, list_address)

    def update_index_list(self, index_start, index_end, minus_list, the_entire_range, list_address):
        """
        This function serve to update the index list
        :param index_start:
        :param index_end:
        :param minus_list:
        :param the_entire_range:
        :param list_address:
        :return:
        """
        for j in range(1, len(index_start)):  # update the index list to get the right value
            for i in range(j, len(index_start)):
                index_start[i] = index_start[i] - minus_list[j - 1]
                index_end[i] = index_end[i] - minus_list[j - 1]

        # print(index_start, index_end)
        # print(list_address[self.ow.Title_Number], the_entire_range)
        self.join_the_entire_range(index_start, index_end, the_entire_range, list_address)

    def join_the_entire_range(self, index_start, index_end, the_entire_range, list_address):
        """
        This function join the street name inside the entire_range
        :param index_start:
        :param index_end:
        :param the_entire_range:
        :param list_address:
        :return:
        """
        for i in range(0, len(index_start)):
            # print(index_start[i], index_end[i])
            # if list_address[self.ow.Title_Number] == 'CYM323481':
            #     print(colored(index_start, 'blue'), colored(index_end, 'blue'), the_entire_range)
            the_entire_range[index_start[i]:index_end[i]] = [' '.join(the_entire_range[index_start[i]:index_end[i]])]

        # if list_address[self.ow.Title_Number] == 'CYM71611':
        #     print(colored(the_entire_range, 'green'))
        self.group_by_street_name(the_entire_range, list_address)

    def group_by_street_name(self, the_entire_range, list_address):
        """
        This function group the street name
        :param the_entire_range:
        :param list_address:
        :return:
        """
        group_street_name = []
        temporary_list = []
        # print(colored(the_entire_range, 'yellow'))
        for elem in the_entire_range:
            temporary_list.append(elem)
            if self.capital_letter_word.findall(elem):
                group_street_name.append(temporary_list)
                temporary_list = []
        # print(list_address[self.ow.Title_Number], colored(group_street_name, 'yellow'))
        self.join_street_name_with_numbers(group_street_name, list_address)

        # if list_address[self.ow.Title_Number] == 'YY21742':  # WA79324, WA40846, CYM71611, YY21742
        #     print(colored(group_street_name, 'blue'))
        # print(list_address[self.ow.Title_Number], colored(group_street_name, 'blue'))  # P170170

        return temporary_list

    def join_street_name_with_numbers(self, group_street_name, list_address):
        """
        This function join the street name with numbers
        :param group_street_name:
        :param list_address:
        :return:
        """
        address_list = []
        for elem_list in group_street_name:
            # address_list.append(list_address[self.ow.Title_Number])
            for n in range(0, len(elem_list) - 1):
                # print(elem_list[n], elem_list[len(elem_list) - 1])
                join = elem_list[n] + ' ' + elem_list[len(elem_list) - 1]
                address_list.append(join)

        # if list_address[self.ow.Title_Number] == 'WA79324':
        #     print(colored(address_list, 'blue'))
        self.all_odd_address_list[list_address[self.ow.Title_Number]] = address_list

        # self.all_odd_address_list.append(address_list)

        return self.all_odd_address_list

    def load_data(self, the_file):
        """
        Load the data into a list
        :param the_file:
        :return: list
        """
        with open(the_file, 'r') as f:
            f.readline()
            for line in f:
                tl = line.replace('\n', '').upper().split('\t')
                # if tl[self.ow.Title_Number] == 'WA79324':
                #     print(tl[self.pa])
                self.data.append(tl)

        return self.data

    def standardise_data(self, data):
        """
        This function standardizes the data, replaces 'EVEN' etc.. by 'ODD'
        :param data:
        :return: list
        """

        for idx, list_address in enumerate(data):

            list_address[self.pa] = list_address[self.pa].replace('(EVEN)', '(ODD)').replace('(EVENS)', '(ODD)').\
                replace('(EVEN NUMBERS)', '(ODD)').replace('(EVENS ONLY)', '(ODD)').\
                replace(' EVENS,', '(ODD),').replace(' EVENS ', ' (ODD) ')
            list_address[self.pa] = list_address[self.pa].replace('INCLUSIVE (ODD)', '(ODD)').\
                replace('INCLUSIVE (ODD NUMBERS)', '(ODD)')  # WYK507353
            list_address[self.pa] = list_address[self.pa].replace('(EVEN NUMBERS ONLY)', '(ODD)').\
                replace('EVEN NUMBERS', '(ODD)').replace('(ODD NUMBERS)', '(ODD)').replace('(ODDS)', '(ODD)')
            list_address[self.pa] = list_address[self.pa].replace('(EVEN ONLY)', '(ODD)').\
                replace('(ODD ONLY)', '(ODD)').replace('(ODD) ONLY', '(ODD)')  # WA631894, DN602002
            list_address[self.pa] = list_address[self.pa].replace('ODDS ONLY', 'ODD').\
                replace('(EVEN) INCLUSIVE', '(ODD)').replace('(ODD) INCLUSIVE', '(ODD)')
            list_address[self.pa] = self.tight_dash_odd.sub(r'\1 (ODD)', list_address[self.pa])
            list_address[self.pa] = self.tight_dash_right_odd.sub(r'\1-\2 (ODD)', list_address[self.pa])
            list_address[self.pa] = self.space_dash_odd.sub(r'\1-\2 (ODD)', list_address[self.pa])  # P170170
            list_address[self.pa] = re.sub(r'(\d+ TO \d+ ODD NUMBERS)', r'\1 (ODD))', list_address[self.pa])

        return list_address[self.pa]

    def standardise_data2(self, data):
        """
        This function standardizes the data, replaces 'INC' etc.. by 'INCLUSIVE'
        :param data:
        :return: list
        """

        for idx, list_address in enumerate(data):

            list_address[self.pa] = re.sub('\(INC 32A\)', ' (INCLUSIVE), 32A', list_address[self.pa])
            list_address[self.pa] = list_address[self.pa].replace('(EVENS INCLUSIVE)', '(ODD)').\
                replace('(ODD INCLUSIVE)', '(ODD)')
            list_address[self.pa] = list_address[self.pa].replace('(CONSECUTIVE NUMBERS)', '(INCLUSIVE)').\
                replace('CONSECUTIVE NUMBERS)', '(INCLUSIVE)').replace('(INC)', '(INCLUSIVE)').\
                replace('(INCL)', '(INCLUSIVE)').replace('(INCL )', '(INCLUSIVE)').replace('CONSECUTIVE', 'INCLUSIVE')
            list_address[self.pa] = re.sub(' INC ', '(INCLUSIVE)', list_address[self.pa])
            list_address[self.pa] = re.sub(' INC,', '(INCLUSIVE)', list_address[self.pa])
            list_address[self.pa] = self.tight_dash_inclusive_bracket.sub(r'\1 (INCLUSIVE)', list_address[self.pa])
            list_address[self.pa] = self.tight_nb_inclusive.sub(r'\1 (INCLUSIVE)', list_address[self.pa])  # WA92444
            list_address[self.pa] = self.flat_inclusive_normalized.sub(r'FLATS \1 TO FLATS \2 (INCLUSIVE)',
                                                                       list_address[self.pa])  # WA382857
            list_address[self.pa] = self.inclusive_letter.sub(r'(INCLUSIVE) \1', list_address[self.pa])  # CYM611888
            list_address[self.pa] = re.sub(r'(?<=\s)INCLUSIVE(?=\s|\,)', r'(INCLUSIVE)', list_address[self.pa])
            list_address[self.pa] = re.sub(r'(UNITS \d+ TO \d+)', r'\1 (INCLUSIVE)', list_address[self.pa])
            # if list_address[self.ow.Title_Number] == 'CYM122353':
            #     print(list_address[self.ow.Title_Number], list_address[self.pa])

        return list_address[self.pa]

    def standardise_data3(self, data):
        """
        This function standardizes the data:
        - Add a space between parenthese and 'AND'
        - Add space between the postcode and a numbers
        - Rework the brackets
        - Remove the '&' character
        - Remove space when dash for inclusive, i.e: 1 - 5 (INCLUSIVE) -> 1-5 (INCLUSIVE)
        - Remove space when simple dash, i.e: 1 - 5 -> 1-5
        - Remove the word 'PART OF'
        :param data:
        :return: list
        """

        for idx, list_address in enumerate(data):

            list_address[self.pa] = re.sub('\)AND', ') AND', list_address[self.pa])
            list_address[self.pa] = self.postcode_digit.sub(r'\1 \2', list_address[self.pa])
            list_address[self.pa] = self.parenthese_postcode.sub(r'\2', list_address[self.pa])
            list_address[self.pa] = self.inv_parenthese_postcode.sub(r'(\2', list_address[self.pa])  # WYK707867
            list_address[self.pa] = list_address[self.pa].replace('& ', '').replace('&', '')
            list_address[self.pa] = self.tight_dash_inclusive.sub(r'\1 TO \2 (INCLUSIVE)',
                                                                  list_address[self.pa])  # CL160664
            list_address[self.pa] = self.space_dash_inclusive.sub(r'\1 TO \2 (INCLUSIVE)',
                                                                  list_address[self.pa])  # CYM291170
            list_address[self.pa] = self.space_dash.sub(r'\1-\2', list_address[self.pa])  # P170170
            list_address[self.pa] = re.sub(r'PART OF', '', list_address[self.pa])  # WA102377
            list_address[self.pa] = re.sub(r'PLOTS', '', list_address[self.pa])  # YY112215
            list_address[self.pa] = self.tight_dash_right_inclusive.sub(r'\1 TO \2 (INCLUSIVE)',
                                                                        list_address[self.pa])  # CYM412410
            list_address[self.pa] = self.tight_dash_left.sub(r'\1-\2', list_address[self.pa])  # DN503661
            # list_address[self.pa] = self.tight_dash_right.sub(r'\1-\2', list_address[self.pa])  # CYM90573
            list_address[self.pa] = re.sub(r'(\d+) -(\d+)', r'\1-\2', list_address[self.pa])  # CYM90573
            # if list_address[self.ow.Title_Number] == 'CYM90573':
            #     print(list_address[self.pa])

        return list_address[self.pa]

    def standardise_data4(self, data):

        for idx, list_address in enumerate(data):

            list_address[self.pa] = self.remove_formerly.sub(r'', list_address[self.pa])  # WA44915
            list_address[self.pa] = self.remove_land_side_of.sub(r'', list_address[self.pa])  # WA25817
            list_address[self.pa] = self.remove_plot.sub(r'', list_address[self.pa])  # WA830325
            list_address[self.pa] = self.remove_site.sub(r'', list_address[self.pa])  # WA878817
            # list_address[self.pa] = re.sub(r'', r'', list_address[self.pa])

            # if list_address[self.ow.Title_Number] == 'CYM556948':
            #     print(list_address[self.pa])

    def extract_land_and_other_items(self):
        """
        This function extract all item we don't want in our data
        :return: list
        """
        tmp = []
        for address in self.data:
            if self.confirm_not_land_or_other(address):
                tmp.append(address)
        self.data[:] = tmp

    def confirm_not_land_or_other(self, address):
        """
        Confirm if there are not data we don't want
        :param address:
        :return: Boolean
        """
        for items in self.list_not_interested:
            if address[self.ow.Property_Address].startswith(items):
                return False
        return True

    def odd_even_inclusive_numbers2csv(self):
        """
        Write all odd and inclusive number in a csv file
        :return: csv file
        """
        lt = self.data

        # for address in self.all_odd_address_list:
        #     print(address)

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

            # test with dictionary
            for list_address in lt:
                if list_address[self.ow.Title_Number] in self.all_odd_address_list:
                    for address in self.all_odd_address_list[list_address[self.ow.Title_Number]]:
                        list_address[self.ow.Property_Address] = address
                        try:
                            output_writer.writerow(list_address)
                        except:
                            print(colored('Exception: ', 'red'), list_address)

    def multiple_numbers2csv(self):
        lt = self.data

        # for key, address in self.multiplicate_list.items():
        #     print(key, address)

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

            # test with dictionary
            for list_address in lt:
                if list_address[self.ow.Title_Number] in self.multiplicate_list:
                    for address in self.multiplicate_list[list_address[self.ow.Title_Number]]:
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

    def main(self, address_list):
        # Results = list of address after it has been split
        # print(address_list)
        results = self.start_commercial_ownership(address_list)
        return results


if __name__ == '__main__':
    fg = Main()

    start_time = time.time()

    fg.start_commercial_ownership('/media/pc2/Backup/Stage_doorda/property_product/address/data/0_raw/'
                                  'all_1_CCOD_FULL_2019_05.tsv')

    fg.odd_even_inclusive_numbers2csv()
    fg.multiple_numbers2csv()

    fg.remove_redundant('/media/pc2/Backup/Stage_doorda/property_product/address/data/output/simple_numbers/',
                        '1_CCOD_FULL_2019_05.csv')
    fg.remove_redundant('/media/pc2/Backup/Stage_doorda/property_product/address/data/output/odd_numbers/',
                       '1_CCOD_FULL_2019_05.csv')

    # file = '/media/pc2/Backup/Stage_doorda/property_product/address/data/0_raw/all_1_CCOD_FULL_2019_05.tsv'
    # with open(file, "r") as f:
    #     for line in f:
    #         tl = line.replace('\n', '').upper().split('\t')
    #         # address_list = tl
    #         new_address_list = fg.main(tl)

    end_time = time.time()

    print('Execution time: ', end_time - start_time)
