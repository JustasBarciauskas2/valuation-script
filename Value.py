from PyPDF2 import PdfReader, PdfWriter 
import PyPDF2
import os
import re

Path = "10-K"

String_Sing = r"SIGNATURES.*"

String_Rev = r"Total Revenues, net.*|Net Sales.*"
#String_EBIT = r"Operating (?:Loss|Profit).(?! \d+%)[^.]*(?=.)"
String_EBIT = r"Operating Loss.*|Operating loss.*|Operating \(Loss\).*"

signaturesList = []
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

            signaturesList.append(page_number)
            break
    
    for i in range(page_number, NumPages):

        PageObj = object.pages[i]
        Text = PageObj.extract_text() 
        
        Search_Rev = re.findall(String_Rev,Text,re.IGNORECASE)

        if len(Search_Rev) != 0:

            Rev_string = Search_Rev[0]

            Revenue = re.findall(r'\b\d{1,3}(?:,\d{3})*\b', Rev_string)
            
            if len(Revenue) == 2:
                Save_page = i
                revenue1 = Revenue[0]
                revenue2 = Revenue[1]

                print(filename)
            
                print("Revenue:", revenue1 +' '+revenue2)

                PageObj = object.pages[Save_page]
                Text = PageObj.extract_text() 
                
                Search_EBIT = re.findall(String_EBIT,Text)
                
                if len(Search_EBIT) != 0:

                    EBIT_string = Search_EBIT[0]

                    EBIT = re.findall(r'\b\d{1,3}(?:,\d{3})*\b', EBIT_string)

                    if len(EBIT) == 2:
                        EBIT1 = EBIT[0]
                        EBIT2 = EBIT[1]

                    print("EBIT:", EBIT1 +' '+EBIT2)

                    break






        
       
    