import os
import datetime
import csv
import sys
import zipfile
import hashlib
from w3lib.html import replace_entities
import subprocess
from tqdm import tqdm

temp_file = '/tmp/temp'


def is_file_search_term_in_file_list(list_of_folder_files: str, search_term: str) -> list:
    matching_files = []
    for i in list_of_folder_files:
        if search_term in i:
            matching_files.append(i)
    return matching_files


def get_list_files_in_folder(folder):
    return [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]


def move_file(full_file_name, destination_folder):
    if os.path.isdir(destination_folder):
        os.rename(full_file_name, destination_folder + os.remove(full_file_name))
        return True
    return False


def delete_file(full_file_name):
    os.remove(full_file_name)


def get_just_file_name(full_file_name):
    return os.path.basename(full_file_name)


def does_file_exist(full_file_name):
    return os.path.isfile(full_file_name)


def load_data_into_dict_by_group(full_file_name: str, group_column: int) -> dict:
    data = {}
    number_lines = number_lines_in_file(full_file_name)
    print('Importing into Dic :: ' + full_file_name)
    with open(full_file_name, 'r') as f:
        for line in tqdm(f, total=number_lines):
            the_list = line.replace('\n', '').upper().split('\t')
            if the_list:
                if the_list[group_column] not in data:
                    data[the_list[group_column]] = [the_list]
                elif the_list[group_column] in data:
                    tl = data[the_list[group_column]]
                    tl.append(the_list)
                    data[the_list[group_column]] = tl
    return data


def get_data_file_date_and_name(the_file):
    tl = the_file.split('/')
    p1 = len(tl)
    the_name = tl[p1 - 1]
    st1 = tl[p1 - 1]
    tm = st1.split('-')
    p1 = len(tm)
    tn = tm[p1 - 1].split('.')
    the_date = tm[p1 - 2] + '-' + tn[0] + '-01'
    return the_date, the_name


def csv2tsv(csv_file, tsv_file):
    if csv_file.endswith('.tsv'):
        return csv_file
    if tsv_file == csv_file:
        tsv_file = csv_file[:-4] + '.tsv'
    if os.path.isfile(tsv_file):
        return tsv_file
    csv.field_size_limit(sys.maxsize)
    try:
        csv.writer(open(tsv_file, 'w+'), delimiter="\t").writerows(csv.reader(open(csv_file)))
    except UnicodeDecodeError:
        return 'ERROR UNICODE'
    return tsv_file


def csv2tsv_all_files(file_list):
    for csv_file in file_list:
        if csv_file.endswith('.tsv'):
            continue
        tsv_file = csv_file[:-4] + '.tsv'
        csv.field_size_limit(sys.maxsize)
        try:
            csv.writer(open(tsv_file, 'w+'), delimiter="\t").writerows(csv.reader(open(csv_file)))
        except UnicodeDecodeError:
            return 'ERROR UNICODE'
    return 'Done'


def number_lines_in_file(the_file):
    st1 = subprocess.run(["wc", "-l", the_file], stdout=subprocess.PIPE)
    st2 = st1.stdout
    st3 = st2.decode('utf8')
    tl = st3.split(' ')
    return int(tl[0])


def remove_header_from_file(the_file):
    os.system("sed -i '1d' " + the_file)


def remove_lines_in_columns_csv(the_file):
    with open(the_file, "r") as the_input, open("/data/ramdisk/output.csv", "w") as output:
        w = csv.writer(output)
        for record in csv.reader(the_input):
            w.writerow(tuple(s.replace("\n", ' :: ') for s in record))
    os.system('mv /data/ramdisk/output.csv ' + the_file)


def move_file_get_new_name(the_file, destination_folder, cp_or_mv):
    os.system(cp_or_mv + ' ' + the_file + ' ' + destination_folder)
    tl = the_file.split('/')
    p1 = len(tl)
    the_file_name = tl[p1 - 1]
    if not destination_folder.endswith('/'):
        destination_folder += '/'
    return destination_folder + the_file_name


def unzip_place_in_folder_return_name(the_file, destination_folder):
    with zipfile.ZipFile(the_file, 'r') as z:
        file_names = z.namelist()
    if not os.path.exists(destination_folder):
        os.system('mkdir ' + destination_folder)
    os.system('unzip ' + the_file + ' -d ' + destination_folder)
    return file_names


def file_modified_date(the_file):
    file_details = os.path.getmtime(the_file)
    return str(datetime.date.fromtimestamp(file_details))


def file_hash(the_file_name):
    return hashlib.md5(open(the_file_name, 'rb').read()).hexdigest()


def replace_html_entities(the_file):
    o = open(temp_file, 'w')
    with open(the_file, 'r') as f:
        for lines in f:
            st1 = replace_entities(lines, remove_illegal=True, encoding='utf-8')
            # remove special characters
            st1 = st1.replace('\\', '')
            o.write(st1)
    o.close()
    os.system('mv ' + temp_file + ' ' + the_file)


def remove_special_characters_by_file(the_file):
    o = open(temp_file, 'w')
    with open(the_file, 'r') as f:
        for line in f:
            line = line.replace('\\', '')
            o.write(line)
    o.close()
    os.system('mv ' + temp_file + ' ' + the_file)


def unzip_the_file(the_file_name, folder_unzip_in_or_empty):
    if folder_unzip_in_or_empty:
        os.system('unzip -j ' + the_file_name + ' -d ' + folder_unzip_in_or_empty)
    else:
        directory = the_file_name.replace(os.path.basename(the_file_name), '')
        os.system('unzip -j ' + the_file_name + ' -d ' + directory)


def file_name(the_file):
    return os.path.basename(the_file)


def collation_latin_to_utf8(the_file):
    os.system('iconv -f ISO-8859-1 -t UTF-8 ' + the_file + ' > /data/ramdisk/temp')
    os.system('mv /data/ramdisk/temp ' + the_file)


def are_file_md5_same(file1, file2):
    result = subprocess.run(['md5sum', file1], stdout=subprocess.PIPE)
    st1 = str(result.stdout)
    tl = st1.split(' ')
    md5_file1 = (tl[0][2:])
    result = subprocess.run(['md5sum', file2], stdout=subprocess.PIPE)
    st1 = str(result.stdout)
    tl = st1.split(' ')
    md5_file2 = (tl[0][2:])
    if md5_file1 == md5_file2:
        return True
    return False
