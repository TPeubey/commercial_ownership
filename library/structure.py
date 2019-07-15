import sys
import os


class ProjectStructure:

    def __init__(self):

        self.working_directory = ''

        self.data_raw = ''
        self.data_tsv = ''
        self.data_fill_multiplicate_land_columns = ''
        self.data_multiplicate_land_file = ''
        self.final_result = ''

    @staticmethod
    def confirm_wworking_directory(project_name):
        working_directory = sys.path[0]
        the_list = working_directory.split('/')
        i = 0
        for i, name in enumerate(the_list):
            if project_name in name:
                break
        return '/'.join(the_list[:i + 1]) + '/'


class CommercialOwnership(ProjectStructure):

    def start_address(self):
        self.working_directory = self.confirm_wworking_directory('address')
        self.__create_folder_name()
        # self.__create_folders()

    def __create_folder_name(self):
        self.data_raw = self.working_directory + 'data/0_raw_data/'
        self.data_output = self.working_directory + 'data/output/'
        self.data_simple_numbers = self.working_directory + 'data/output/simple_numbers/'
        self.data_odd_numbers = self.working_directory + 'data/output/odd_numbers/'

    def __create_folders(self):
        require = [self.data_tsv]
        for i in require:
            try:
                if not os.path.isfile(i):
                    os.mkdir(i)
            except:
                pass


class CommercialOwnershipStructure:

    Title_Number, Tenure, multiplicate, land, Property_Address = 0, 1, 2, 3, 4
    District, County, Region, Postcode, Multiple_Address_Indicator = 5, 6, 7, 8, 9
    Price_Paid, Proprietor_Name_1, Company_Registration_No_1, Proprietorship_Category_1 = 10, 11, 12, 13
    Proprietor_1_Address_1, Proprietor_1_Address_2, Proprietor_1_Address_3, Proprietor_Name_2 = 14, 15, 16, 17
    Company_Registration_No_2, Proprietorship_Category_2, Proprietor_2_Address_1 = 18, 19, 20
    Proprietor_2_Address_2, Proprietor_2_Address_3, Proprietor_Name_3, Company_Registration_No_3 = 21, 22, 23, 24
    Proprietorship_Category_3, Proprietor_3_Address_1, Proprietor_3_Address_2, Proprietor_3_Address_3 = 25, 26, 27, 28
    Proprietor_Name_4, Company_Registration_No_4, Proprietorship_Category_4, Proprietor_4_Address_1 = 29, 30, 31, 32
    Proprietor_4_Address_2, Proprietor_4_Address_3, Date_Proprietor_Added = 33, 34, 35
    Additional_Proprietor_Indicator = 36
