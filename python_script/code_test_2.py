import re
from termcolor import colored


class Code:

    def __init__(self):
        # self.data = ['1', '2', '7', '8', '10', 'BLACKBIRDS', 'WAY', 'ST', 'MELLONS', 'CARDIFF', '(CF3', '5RE)', '8',
        #              '9', '10', '14', '15', 'BLUEBELL', 'DRIVE', 'ST', 'MELLONS', 'CARDIFF', '(CF3', '5RA)', '2', '14',
        #              '16', 'DRAWLINGS', 'CLOSE', 'ST', 'MELLONS', 'CARDIFF', '(CF3', '5RB)', '1', '2', '4', '6', '8',
        #              '10', '11', '12', '13', '14', '16', '17', '18', '20', '22', '24', '25', '26', '27', 'ARCON',
        #              'HOUSE', 'BLACKBIRDS', 'WAY', 'ST', 'MELLONS', 'CARDIFF', '(CF3', '5RF)', '13', '15', '17', '19',
        #              '21', '23', '25', '27', '29', '31', '33', '35', '37', 'ST', 'MELLONS', 'HOUSE', 'BLACKBIRDS',
        #              'WAY', 'ST', 'MELLONS', 'CARDIFF', '(CF3', '5RE)', '36-45', 'AVENUE', 'HOUSE', 'BLUEBELL', 'DRIVE',
        #              'ST', 'MELLONS', 'CARDIFF', '(CF3', '5RA)', '20-35', 'MILL', 'HOUSE', 'BLUEBELL', 'DRIVE', 'ST',
        #              'MELLONS', 'CARDIFF', '(CF3', '5RA)', '1', '3', '5', '7', '9', '11', '13', '15', '17', '19', '21',
        #              '23', '25', '27', '29', '31', '33', '35', '37', '39', '41', '43', '45', '47', 'ELIZABETH', 'HOUSE',
        #              'DRAWLINGS', 'CLOSE', 'ST', 'MELLONS', 'CARDIFF', '(CF3', '5RB)', '1-10', 'PRINCE', 'OF', 'WALES',
        #              'HOUSE', 'EASTERN', 'CLOSE', 'ST', 'MELLONS', 'CARDIFF', '(CF3', '5RD)', '11-15', 'JUBILEE',
        #              'HOUSE', 'EASTERN', 'CLOSE', 'ST', 'MELLONS', 'CARDIFF', '(CF3', '5RD)', '16-25', "TY'R", 'WINCH',
        #              'HOUSE', 'EASTERN', 'CLOSE', 'ST', 'MELLONS', 'CARDIFF', '(CF3', '5RD)']

        # self.data = ['FLATS', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45',
        #              '46', '47', '48', '49', '50', '51', '52', '53', '54', 'BUTT-LEE', 'COURT', 'WILLIAMS', 'CRESCENT',
        #              'BARRY', '(CF62', '8EX)']

        # self.data = ['FLATS', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', 'YEW',
        #              'TREE', 'COURT', 'BRONWYDD', 'AVENUE', 'CARDIFF', 'CF23', '5JP', 'PARKING', 'SPACES', 'ASSOCIATED',
        #              'WITH', 'FLATS', '11', '15']

        # self.data = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '14', '15', '16', '17', '18', '19',
        #              '20', '21', '22', '23', 'CHENIES', 'CLOSE', '(LS14', '6UL);', '1-14', '16', '17', '18', '19', '20',
        #              '21', '22', '23', '24', '25', '26', '27', '28', '30', '31', '33', '35', '37', 'COLLIN', 'ROAD',
        #              '((LS14', 'RYE', 'PLACE', '(LS14', '6AG);', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11',
        #              '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '26', '28', 'STOREY',
        #              'PLACE', '(LS14', 'SUNNYDENE', ')LS14', '9', '10', '11', '12', '13', 'SUTTON', 'APPROACH', '(LS14',
        #              '6AH);', '1', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', 'SUTTON', 'CRESCENT', '(LS14',
        #              '6AJ);', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', 'WAKEFIELD', 'AVENUE', '(LS14',
        #              '6AN);', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17',
        #              '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34',
        #              '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '47', '49', '51', '53', '55', '57',
        #              '59', '61', '63', 'WATSON', 'ROAD', '(LS14', '6AE);', '576', '582', '584', '588', 'YORK', 'ROAD',
        #              '(LS14', '6AD)']

        # self.data = ['GROUND', 'FLOOR', 'COMMERCIAL', 'UNIT', 'FLAT', '6', '93-95', 'WHITCHURCH', 'ROAD', 'CARDIFF',
        #              '(CF14', '3JP)']  # WA25210
        self.data = ['THE', 'RAILWAY', 'HOTEL', '128', '130', '132', 'STATION', 'ROAD', 'LLANDAFF',
                     'NORTH', '(CF14', '2FH)']

        # self.data = ['GWLAD', 'DU', 'GWYRDD', 'GILFACH', 'FOCH', 'PORTH', '(CF39', '8YD)']  # WA92444

        self.data2 = ['3, 4, 5, 19 South William Street, 26, 28, 29, 30, 31 Louisa Street, 42 George Street, '
                                      '44 Dudley Street, 1, 7, 7A Eleanor Street, 1, 2, 3, 4, Penarth Terrace, 19 Margaret Street',
                                      '135A, 135B, 135C, 135D, 135E, 135F, 135G and 135H Clive Street, Cardiff (CF11 7HQ)',
                                      '7 Ambleside Avenue, 15 Lake Road West and land forming parts of the sites of or lying'
                                      ' adjacent to Allensbank Road, Eastern Avenue, Lake Road East, Lake Road West and North Road',
                                      '64 Sloper Road, (formerly 1A Sloper Road), Leckwith, Cardiff',
                                      '24 Orbit Street, 62 Longcross Street, 25 North Luton Place, 25 Adamsdown Square, '
                                      '7 Clyde Street, 20 Constellation Street, 7 Prince Leopold Street and 6 Moira Street',
                                      'Flat 102, Victoria House, 143-145 The Headrow, Leeds (LS1 5RL)',
                                      'Apartment 6, Citispace West, 2 Leylands Road, Leeds (LS2 7JS)',
                                      '56 and 58 Albion Street, Leeds, (LS1 6AD)',
                                      '2, 2A, 2B, 4, 4A, 4B, 6, 6A, 8, 8A, 10, 10A, 12, 12A, 14, 14A, 16 and 16A Bentley Lane,'
                                      ' Leeds (LS7 2QR)  36-70 (even numbers only) Stainbeck Avenue, Leeds (LS7 2QU)',
                                      '31A, 31B, 31C 31D SAPPHIRE STREET, CARDIFF CF24 1PY 22-32 (ODD) BROADWAY,'
                                      ' CARDIFF CF24 1NF',
                      '44, 44a, 46 and 46a Sanquhar Street and 1 to 22 (inclusive) Cwrt Sanquhar, Splott, Cardiff'
                      ]

    def standardise(self):
        self.data2 = self.data2[10].replace(',', '').split(' ')
        self.data2 = [x.upper() for x in self.data2 if x]
        self.data2 = [x.replace('AND', '') for x in self.data2 if x]  # remove the 'AND'
        self.data2 = [x for x in self.data2 if x]  # remove empty element
        return self.data2

    def conditional_with_index_list_second_case_1(self):

        index_start_list = [5, 17, 27, 53, 75, 129]
        index_end_list = [12, 24, 34, 62, 105, 170]
        minus = 0

        # self.data[5:12] = [' '.join(self.data[5:12])]
        # self.data[11:18] = [' '.join(self.data[11:18])]
        # self.data[15:22] = [' '.join(self.data[15:22])]
        # self.data[35:44] = [' '.join(self.data[35:44])]
        # self.data[49:59] = [' '.join(self.data[49:59])]
        # self.data[51:60] = [' '.join(self.data[51:60])]
        # self.data[53:62] = [' '.join(self.data[53:62])]
        # self.data[78:87] = [' '.join(self.data[78:87])]
        # self.data[80:91] = [' '.join(self.data[80:91])]
        # self.data[82:91] = [' '.join(self.data[82:91])]
        # self.data[84:94] = [' '.join(self.data[84:94])]

        index_start = []
        index_end = []
        minus_list = []

        self.data = self.standardise()
        print(self.data)

        start_word_list = ['FLAT', 'FLATS', 'APARTMENT']
        count_digit = 0

        for p in range(0, len(self.data)):  # check if there ar no number in the address
            if re.findall(r'(^\d+$)|($\d+[A-Z]$)|(^\d+[A-Z]?-\d+[A-Z]?$)', self.data[p]):
                count_digit += 1
        if count_digit == 0:
            self.data = ' '.join(self.data)

        if self.data[0] in start_word_list:
            index_start.append(0)

        for i in range(0, len(self.data) - 1):  # retrieve index_start
            if i == 0:
                if re.findall(r'^[A-Z]+$', self.data[i]):
                    index_start.append(i)
            if re.findall(r'(^[A-Z]+)|(^\()|(\)$)', self.data[i]) \
                    and re.findall(r'(^\d+$)|(^\d+-\d+$)|(^\d+[A-Z]$)', self.data[i - 1]):
                # print(self.data[i - 1], 'index start: ', self.data[i], i)
                index_start.append(i)
                print('index start: ', index_start)

            # retrieve index_end
            if re.findall(r'(^[A-Z]+)|(^\()|(\)$)|(^\d[A-Z]{2})', self.data[i]) \
                    and re.findall(r'(^\d+$)|(^\d+-\d+$)|(^\d+[A-Z]$)', self.data[i + 1]):
                # print('index end: ', self.data[i], self.data.index(self.data[i]))
                index_end.append(i + 1)
                print('index end: ', index_end)
        index_start = list(dict.fromkeys(index_start))  # remove redundant
        index_end.append(len(self.data))  # add the last index

        # print(index_start, index_end)

        for i in range(0, len(index_start)):  # get the values to be subtracted
            minus = (index_end[i] - index_start[i]) - 1
            minus_list.append(minus)
        print(colored(minus_list, 'blue'))

        for j in range(1, len(index_start)):  # update the index list to get the right value
            for i in range(j, len(index_start)):
                index_start[i] = index_start[i] - minus_list[j - 1]
                index_end[i] = index_end[i] - minus_list[j - 1]

                # print(minus_list[j], index_start[i], index_end[i])

        # print(sum(minus_list))

        for i in range(0, len(index_start)):
            # print(index_start[i], index_end[i])
            self.data[index_start[i]:index_end[i]] = [' '.join(self.data[index_start[i]:index_end[i]])]

        print(self.data)


if __name__ == '__main__':

    test = Code()
    # test.standardise()
    test.conditional_with_index_list_second_case_1()
