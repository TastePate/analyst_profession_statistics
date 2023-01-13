import csv
import re


class Parser(object):

    def __init__(self, file_name: str):
        self.file_name = file_name

    def get_data_from_file(self):
        with open(self.file_name, 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            for line in reader:
                yield self.__parse_line(line)

    def __get_clean_line(self, string):
        string = re.sub(r'<[^>]*>', '', string)
        string = re.sub("\s+", " ", string)
        string = string.strip()
        return string

    def __parse_line(self, row: list[str]):
        parsed_row = []
        for row_element in row:
            if "\n" in row_element:
                parsed_row.append(row_element.replace("\n", ","))
            else:
                parsed_row.append(self.__get_clean_line(row_element))
        return parsed_row
