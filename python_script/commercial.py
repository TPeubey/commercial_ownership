from library import file_handling as fh
# from library import address_reference
from library import structure
import re



class Commercial:

    def __init__(self):
        # self.st = address_reference.CommercialOwnership()
        self.st = structure.CommercialOwnership()
        self.data = []
        self.list_not_interested = ['LAND AND', 'LAND AT', 'SITES OF', 'PUMPING STATION', 'BEING LAND',
                                    'LAND TO', 'LAND IN', 'LAND LYING', 'PART OF ', 'PARTS OF',
                                    'LAND ADJOINING', 'THE AIRSPACE', 'LAND ON', 'LAND FORMING',
                                    'THE SITES', 'LAND FRONTING', 'ON THE', 'THE SITE', 'ALL THE',
                                    'PORTIONS ', 'LAND BEING']

    def start_commercial_ownership(self, the_file):
        # fh.collation_latin_to_utf8(the_file)
        # tsv = fh.csv2tsv(the_file, the_file)
        self.load_data(the_file)
        self.extract_land_and_other_items()
        # self.find_multiplication()

    def find_multiplication(self):
        for address in self.data:
            if "(ODD)" in address[self.st.full_address] or "(EVEN)" in address[self.st.full_address]:
                self.deal_with_odd_and_even(address)
            # if ' AND ' in address[self.st.full_address] and ' FLOOR ' not in address[self.st.full_address]:

    def deal_with_odd_and_even(self, address):
        s1 = address[self.st.full_address]
        s1.replace('(EVEN)', '(ODD)')
        self.get_the_numbers(s1.split('(ODD)'), s1)
        self.print_test_address(address, s1.split('(ODD)'))

    def get_the_numbers(self, tl, original_string):
        the_range = []
        single_numbers = []
        for item in tl:
            item = item.replace(',', ' ').replace('  ', ' ')
            tm = item.split(' ')
            for index, i in enumerate(tm[:-1]):
                if i == 'TO':
                    the_range.append([tm[index - 1], tm[index + 1], ''])
                    tm[index - 1] = ''
                    tm[index] = ''
                    tm[index + 1] = ''
                    if index + 2 < len(tm):
                        if tm[index + 2] == '(INCLUSIVE)' or tm[index + 2] == '(EVEN)' or tm[index + 2] == '(ODD)':
                            the_range[-1][2] = tm[index + 2]
                            tm[index + 2] = ''
                            print(the_range)


            # if the_range:
            #     print(single_numbers, the_range, tm)
            # self.find_the_road(tm, original_string)
        # print(the_range)

    def find_the_road(self, tm, s1):
        print(s1)

    def extract_land_and_other_items(self):
        tmp = []
        for address in self.data:
            if self.confirm_not_land_or_other(address):
                tmp.append(address)
        self.data[:] = tmp

    def confirm_not_land_or_other(self, address):
        for items in self.list_not_interested:
            if address[self.st.full_address].startswith(items):
                return False
        return True

    def load_data(self, the_file):
        with open(the_file, 'r') as f:
            f.readline()
            for line in f:
                tl = line.replace('\n', '').upper().split('\t')
                self.data.append(tl)

    def test_print_list(self, the_list):
        for i in the_list:
            print(i)

    def print_test_address(self, address, tl, title='SYK210490'):
        if address[self.st.title_number] == title:
            print(address[self.st.full_address])
            print(tl)


fg = Commercial()
fg.start_commercial_ownership('/media/pc2/Backup/Stage_doorda/property_product/address/data/sample.csv')