Search_EBIT = re.findall(String_EBIT,IncomeStatement)
    Development_Costs = re.findall(String_Deveopment_Costs,IncomeStatement, re.IGNORECASE)
    if len(Development_Costs) != 0:
        get_development_costs(Development_Costs)

    if len(Search_EBIT) != 0:
        get_EBIT()
        break