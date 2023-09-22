from PyPDF2 import PdfReader, PdfWriter 
import PyPDF2
import os
import re

Path = "10-K"

String_Sing = r"SIGNATURES.*"
Financial_Statements_Index = r"(?s)Financial Statements and Supplementary Data.*?(\d+)" 

String_Rev = r"Total Revenues, net.*|Net Sales.*|Total revenue\s*([\d,]+)\s*([\d,]+)\s*([\d,]+)"
String_EBIT = r"Operating Loss.*|Operating loss.*|Operating \(Loss\).*"
String_Deveopment_Costs = r"Development Costs.*"

signaturesList = []
financial_page_numbers = []
def get_development_costs(Development_Costs):
    Development_Costs_String = Development_Costs[0]

    dev_costs_filtered = re.findall(r'\b\d{1,3}(?:,\d{3})*\b', Development_Costs_String)

    if len(dev_costs_filtered) == 2:
        dev_costs_filtered1 = dev_costs_filtered[0]
        dev_costs_filtered2 = dev_costs_filtered[1]
        print("Development Costs:", dev_costs_filtered1 +' '+ dev_costs_filtered2)

def get_EBIT():
    EBIT_string = Search_EBIT[0]
    EBIT = re.findall(r'\b\d{1,3}(?:,\d{3})*\b', EBIT_string)

    if len(EBIT) == 2:
        EBIT1 = EBIT[0]
        EBIT2 = EBIT[1]

        print("EBIT:", EBIT1 +' '+EBIT2)
        print(filename)

def get_revenue(i, Revenue):
    income_statement_page_number = i
    revenue1 = Revenue[0]
    revenue2 = Revenue[1]
            
    print("Revenue:", revenue1 +' '+revenue2)
    return income_statement_page_number

for filename in os.listdir(Path):
    file_pdf = os.path.join(Path,filename)

    pdf = PdfReader(file_pdf)
    object = PyPDF2.PdfReader(file_pdf)

    total_number_of_pages = len(object.pages)

    for i in range(0, 3):

        current_page = object.pages[i]

        Text = current_page.extract_text() 

        financial_page = re.findall(Financial_Statements_Index,Text)
        ResSearch = re.findall(String_Sing,Text)


        if len(financial_page) != 0:
            financial_page_number = financial_page[0]
            financial_page_number = int(financial_page_number)
            financial_page_numbers.append(financial_page_number)
            break

        if len(ResSearch) != 0:
            string = ResSearch[0]
            lst_string = string.split(' ')
            signatures_page_number = lst_string[1]
            signatures_page_number = int(signatures_page_number)

            signaturesList.append(signatures_page_number)
            break

    revenue_page_number = 0
    for i in range(financial_page_number-1, financial_page_number + 8):
        current_page = object.pages[i]
        text = current_page.extract_text()
        newtext = text.replace(',','')

        revenue_string = re.findall(String_Rev,newtext, re.IGNORECASE)
        
        if len(revenue_string) != 0:
            revenue_page_number = current_page
            break

    if(revenue_page_number == 0):
        for i in range(signatures_page_number, financial_page_number + 8):
            current_page = object.pages[i]
            Text = current_page.extract_text() 
        
            revenue_string = re.findall(String_Rev,Text,re.IGNORECASE)

            if len(revenue_string) != 0:
                revenue_page_number = current_page
                break

    Rev_string = revenue_string[0]
    Revenue = re.findall(r'\b\d{1,3}(?:,\d{3})*\b', Rev_string)
    
    if len(Revenue) == 2:
        income_statement_page_number = get_revenue(revenue_page_number, Revenue)

        income_statment_page_number = object.pages[income_statement_page_number]
        IncomeStatement = income_statment_page_number.extract_text() 

        Search_EBIT = re.findall(String_EBIT,IncomeStatement)
        Development_Costs = re.findall(String_Deveopment_Costs,IncomeStatement, re.IGNORECASE)
        if len(Development_Costs) != 0:
            get_development_costs(Development_Costs)

        if len(Search_EBIT) != 0:
            get_EBIT()
            break