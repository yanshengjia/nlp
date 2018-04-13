# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2017-12-01 Friday
# @email: i@yanshengjia.com
# extract OCR results from A2iA

import xml.etree.ElementTree as ET
import json

class XMLParser:
    def __init__(self, parent=None):
        self.parent = parent
        self.xml_path= '../../data/corpus/17zuoye/ocr.xml'
        self.output_path= '../../data/corpus/17zuoye/ocr.txt'
        self.essay_counter = 0
        self.essays = []

    def parse(self):
        tree = ET.parse(self.xml_path)
        root = tree.getroot()

        for singlepage in root.findall('SinglePage'):
            self.essay_counter += 1
            essay_info = {}
            essay = ''
            filename = singlepage.get('FileName').replace("D:\A2iA\SunnyEdu\EnHomework\LocalResources\TestData\Images\\", "")

            for line in singlepage.iter('RecoLine'):
                str = line.attrib['Value']
                if str.startswith('-'):
                    str = str[2:]
                if str.endswith('-'):
                    str = str[:-1]
                essay += str + ' '
            
            essay_info['image_id'] = filename
            essay_info['essay'] = essay
            self.essays.append(essay_info)
            
    def saveEssay(self):
        with open(self.output_path, 'w') as output_file:
            json.dump(self.essays, output_file)
    
    def clear(self):
        with open(self.output_path, 'w') as file:
            file.seek(0)
            file.truncate()

def main():
    xml_parser = XMLParser()
    xml_parser.parse()
    xml_parser.saveEssay()

if __name__ == "__main__":
    main()


