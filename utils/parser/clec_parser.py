# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-03-22 Thursday
# @email: i@yanshengjia.com
# Copyright 2018 Shengjia Yan. All Rights Reserved.
# Extract ST3.txt and ST4.txt to JSON (each line is JSON format)

import re
import json
import xlrd
from codecs import open

class CLECParser:
    def __init__(self, parent=None):
        self.parent = parent
        self.st2_path = '../../data/corpus/clec/st2.xlsx'
        self.st2_preprocessed_path = '../../data/corpus/clec/st2_preprocessed.txt'
        self.st2_no_error_mark_path = '../../data/corpus/clec/st2_no_error_mark.txt'
        self.st3_path = '../../data/corpus/clec/st3.txt'
        self.st3_preprocessed_path = '../../data/corpus/clec/st3_preprocessed.txt'
        self.st3_no_error_mark_path = '../../data/corpus/clec/st3_no_error_mark.txt'
        self.st4_path = '../../data/corpus/clec/st4.txt'
        self.st4_preprocessed_path = '../../data/corpus/clec/st4_preprocessed.txt'
        self.st4_no_error_mark_path = '../../data/corpus/clec/st4_no_error_mark.txt'
    
    def find_between(self, s, first, last):
        try:
            start = s.index(first) + len(first)
            end = s.index(last, start)
            return s[start:end]
        except ValueError:
            return ""

    def squeeze_blankspace(self, essay):
        temp_essay = re.sub(' +', ' ', essay)
        new_essay = re.sub(r'\s+([?,.!"])', r'\1', temp_essay)
        return new_essay

    def extract_st2(self):
        with open(self.st2_preprocessed_path, mode='a', encoding='utf8') as st2_preprocessed:
            with open(self.st2_no_error_mark_path, mode='a', encoding='utf8') as st2_no_error_mark:
                workbook = xlrd.open_workbook(self.st2_path)
                worksheet = workbook.sheet_by_index(0)
                offset = 0  # change this depending on how many header rows are present
                counter = 0
                for i, row in enumerate(range(worksheet.nrows)):
                    if i <= offset:  # skip headers
                        continue
                    
                    essay_dict = {}
                    essay_dict['essay_id'] = counter
                    essay_dict['title']    = self.squeeze_blankspace(str(worksheet.cell_value(i, 0)).strip())
                    line                   = worksheet.cell_value(i, 1)

                    # remove <> tag
                    line = re.sub('<.*?>', '', line).strip()
                    essay_dict['essay'] = self.squeeze_blankspace(line)
                    newline = json.dumps(essay_dict)
                    st2_preprocessed.write(newline + '\n')

                    # remove [] tag
                    line = re.sub('\[.*?\]', '', line).strip()
                    essay_dict['essay'] = self.squeeze_blankspace(line)
                    newline = json.dumps(essay_dict)
                    st2_no_error_mark.write(newline + '\n')

                    counter += 1

    def extract_st3(self):
        with open(self.st3_path, mode='r', encoding="ISO-8859-1") as st3:
            with open(self.st3_preprocessed_path, mode='a', encoding='utf8') as st3_preprocessed:
                with open(self.st3_no_error_mark_path, mode='a', encoding='utf8') as st3_no_error_mark:
                    for line in st3:
                        line = line.strip()
                        essay_dict = {}

                        if "<ST 3>" in line:
                            essay_dict['st_id']    = self.find_between(line, '<ST ', '>')
                            essay_dict['sex']      = self.find_between(line, '<SEX ', '>')
                            essay_dict['y']        = self.find_between(line, '<Y ', '>')
                            essay_dict['way']      = self.find_between(line, '<WAY ', '>')
                            essay_dict['typ']      = self.find_between(line, '<TYP ', '>')
                            essay_dict['sch']      = self.find_between(line, '<SCH ', '>')
                            essay_dict['dic']      = self.find_between(line, '<DIC ', '>')
                            essay_dict['title']    = self.find_between(line, '<TITLE ', '>')
                            essay_dict['score']    = self.find_between(line, '<SCORE ', '>')
                            essay_dict['essay_id'] = self.find_between(line, '<ID ', '>')

                            # remove <> tag
                            line = re.sub('<.*?>', '', line).strip()
                            essay_dict['essay'] = self.squeeze_blankspace(line)
                            newline = json.dumps(essay_dict)
                            st3_preprocessed.write(newline + '\n')

                            # remove [] tag
                            line = re.sub('\[.*?\]', '', line).strip()
                            essay_dict['essay'] = self.squeeze_blankspace(line)
                            newline = json.dumps(essay_dict)
                            st3_no_error_mark.write(newline + '\n')

    def extract_st4(self):
        with open(self.st4_path, mode='r', encoding="ISO-8859-1") as st4:
            with open(self.st4_preprocessed_path, mode='a', encoding='utf8') as st4_preprocessed:
                with open(self.st4_no_error_mark_path, mode='a', encoding='utf8') as st4_no_error_mark:
                    lines = st4.read().splitlines()
                    max = len(lines) - 1

                    for index in range(len(lines)):
                        line = lines[index].strip()
                        essay_dict = {}

                        if "<ST 4>" in line and index + 1 <= max:
                            essay_dict['st_id']    = self.find_between(line, '<ST ', '>')
                            essay_dict['sex']      = self.find_between(line, '<SEX ', '>')
                            essay_dict['y']        = self.find_between(line, '<Y ', '>')
                            essay_dict['age']      = self.find_between(line, '<AGE ', '>')
                            essay_dict['way']      = self.find_between(line, '<WAY ', '>')
                            essay_dict['typ']      = self.find_between(line, '<TYP ', '>')
                            essay_dict['sch']      = self.find_between(line, '<SCH ', '>')
                            essay_dict['dic']      = self.find_between(line, '<DIC ', '>')
                            essay_dict['title']    = self.find_between(line, '<TITLE ', '>')
                            essay_dict['score']    = self.find_between(line, '<SCORE ', '>')
                            essay_dict['essay_id'] = self.find_between(line, '<ID ', '>')
                            essay_dict['essay']    = self.squeeze_blankspace(lines[index + 1].strip())

                            newline = json.dumps(essay_dict)
                            st4_preprocessed.write(newline + '\n')

                            # remove [] tag
                            temp_essay = re.sub('\[.*?\]', '', lines[index + 1]).strip()
                            essay_dict['essay'] = self.squeeze_blankspace(temp_essay)
                            newline = json.dumps(essay_dict)
                            st4_no_error_mark.write(newline + '\n')


def main():
    parser = CLECParser()
    parser.extract_st2()
    # parser.extract_st3()
    # parser.extract_st4()

if __name__ == "__main__":
    main()