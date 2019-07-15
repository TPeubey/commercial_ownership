from python_script import main3
import unittest
from library import file_handling as fh


class TestMain3(unittest.TestCase):

    def setUp(self):
        test_file = "/media/pc2/Backup/Stage_doorda/property_product/address/data/0_raw/test_main.tsv"

        fg = main3.Main()

        fg.start_commercial_ownership(test_file)

        fg.odd_even_inclusive_numbers2csv()
        fg.multiple_numbers2csv()

        multiple_numbers = "/media/pc2/Backup/Stage_doorda/property_product/address/data/output/simple_numbers/" \
                           "1_CCOD_FULL_2019_05.csv"
        odd_numbers = "/media/pc2/Backup/Stage_doorda/property_product/address/data/output/odd_numbers/" \
                      "1_CCOD_FULL_2019_05.csv"

        self.data_multiple = fh.load_data_into_dict_by_group(multiple_numbers, 0)
        self.data_odd = fh.load_data_into_dict_by_group(odd_numbers, 0)

    def test_multiple(self):

        # Test 1
        addresses = self.data_multiple["WA9399"]
        # print(addresses)
        assert len(addresses) == 4
        address = self.get_address(self.data_multiple, '38A')
        # print(address)
        assert len(address) == 1
        assert address[0][4] == '38A COUNTISBURY AVENUE CARDIFF'

        # Test 2
        # addresses = self.data_multiple['CYM74862']
        # print(addresses)
        # assert len(addresses) == 2
        #address = self.get_address(self.data_multiple, 'UNIT 2')
        # print(address)
        #assert len(address) == 1
        #assert address[0][2] == 'UNITS 2 THE PODIUM CAPITAL TOWER CARDIFF TOGETHER WITH THE EXCLUSIVE RIGHT TO USE ' \
        #                        'THE PLANT MACHINERY IN THE FIRST FLOOR OF THE THE LAND TINTED YELLOW ON THE FILED ' \
         #                       'PLAN THE FLUES VENTS SERVING THE LAND IN THIS TITLE GRANTED BY THE LEASE DATED ' \
          #                      '29 JUNE 2001 REFERRED TO BELOW'

        # Test 3
        #addresses = self.data_multiple['CYM74862']
        #assert len(address) == 2
        #address = self.get_address(self.data_multiple, 'UNITS 1B')
        #assert address[0][2] == 'UNITS 1B DRAKE WALK CARDIFF BAY CAR PARKING SPACES (CF10 4AN)'

    @staticmethod
    def get_address(the_dic, the_number):
        temp = list()
        for title in the_dic:
            for address in the_dic[title]:
                if address[4].startswith(the_number):
                    temp.append(address)
        return temp
