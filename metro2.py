import random

def portfolio_type_to_account_type(portfolio_type):
    portfolio_types = {
        'C': ['15', '43', '47', '89', '7A', '9B'],
        'I': ['00', '01', '02', '03', '04', '05', '06', '10', '11', '13', '17', '20', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '90', '91', '0F', '3A', '6A', '6D', '7B', '9A'],
        'M': ['08', '19', '25', '26', '2C', '5A', '5B', '6B'],
        'O': ['12', '18', '37', '43', '48', '50', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '77', '90', '4D', '8B'],
        'R': ['07', '18', '37', '43', '0G', '2A', '8A']
    }

    codes_for_account_type = portfolio_types.get(portfolio_type)

    if codes_for_account_type:
        return random.choice(codes_for_account_type)
    else:
        return None
