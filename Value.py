from PyPDF2 import PdfReader, PdfWriter 
import PyPDF2
import os
import re

Path = "10-K"

String_Sing = r"SIGNATURES.*"

for filename in os.listdir(Path):
    file_pdf = os.path.join(Path,filename)

    pdf = PdfReader(file_pdf)
    object = PyPDF2.PdfReader(file_pdf)
    
    NumPages = len(object.pages)

    for i in range(0, NumPages):

        PageObj = object.pages[i]
        
        Text = PageObj.extract_text() 

        ResSearch = re.findall(String_Sing,Text)
        
        if len(ResSearch) != 0:
            string = ResSearch[0]
            lst_string = string.split(' ')
            page_number = lst_string[1]
            page_number = int(page_number)

            print(page_number)
    break







        
       
    