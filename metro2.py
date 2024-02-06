import random
from cerberus import Validator
from datetime import datetime, timedelta
import pycountry
import us
import re

portfolio_types = {
    'C': ['15', '43', '47', '89', '7A', '9B'],
    'I': ['00', '01', '02', '03', '04', '05', '06', '10', '11', '13', '17', '20', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '90', '91', '0F', '3A', '6A', '6D', '7B', '9A'],
    'M': ['08', '19', '25', '26', '2C', '5A', '5B', '6B'],
    'O': ['12', '18', '37', '43', '48', '50', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '77', '90', '4D', '8B'],
    'R': ['07', '18', '37', '43', '0G', '2A', '8A']
}

# Get 90 days ago date
timestamp_range_start = (datetime.today() - timedelta(days=90)).strftime("%Y-%m-%d")

schema = {
    "DateofBirth": {"type": "string", "regex": "^\d{4}-\d{2}-\d{2}$", "date_range":["1924-01-01",datetime.today().strftime("%Y-%m-%d")]},
    "ECOACode": {"type": "string", "allowed": ["1", "2", "3", "5", "7", "T", "X", "W", "Z"]},
    "FirstLineofAddress": {"type": "string"},
    "FirstName": {"type": "string"},
    "MiddleName": {"type": "string", "required": False},
    "Postal-ZipCode": {"type": "string", "regex": "^\d{5}$"},
    "ResidenceCode": {"type": "string", "regex": "^\d{1}$"},
    "SecondLineofAddress": {"type": "string"},
    "SocialSecurityNumber": {"type": "string", "regex": "^\d{3}-\d{2}-\d{4}$"},
    "State": {"type": "string", "us_state": True},
    "Surname": {"type": "string"},
    "TelephoneNumber": {"type": "string", "regex": "^\d{3}-\d{3}-\d{4}$"},
    "Accounts": {
        "type": "list",
        "minlength": 0,
        "maxlength": 20,
        "schema": {
            "type": "dict",
            "schema": {
                "ProcessingIndicator": {"type": "integer"},
                "TimeStamp": {"type": "string", "regex": "^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$", "date_range": [timestamp_range_start, datetime.today().strftime("%Y-%m-%d")]},
                "CorrectionIndicator": {"type": "integer", "allowed": [0, 1]},
                "IdentificationNumber": {"type": "string", "maxlength": 20},
                "CycleIdentifier": {"type": "string"},
                "ConsumerAccountNumber": {"type": "string", "maxlength": 30},
                "PortfolioType": {"type": "string", "allowed": ["R", "I", "O", "M", "C"]},
                "AccountType": {"type": "string", "depends_on":{"property_name":"PortfolioType", "mapping_func":"validate_account_type"}},
                "DateOpened": {"type": "string", "regex": "^\d{4}-\d{2}-\d{2}$"},
                "CreditLimit": {"type": "float", "min": 0},
                "HighestCreditorOriginalLoanAmount": {"type": "float", "min": 0},
                "TermsDuration": {"type": "string"},
                "TermsFrequency": {"type": "string", "allowed": ["D", "P", "W", "B", "E", "M", "L", "Q", "T", "S", "Y"]},
                "ScheduledMonthlyPaymentAmount": {"type": "float", "min": 0},
                "ActualPaymentAmount": {"type": "float", "min": 0},
                "PaymentHistoryProfile": {"type": "string"},
                "SpecialComment": {"type": "string", "allowed": ["", "M", "AP", "BL", "CI", "AM"]},
                "ComplianceConditionCode": {"type": "string", "allowed": ["XB", "XC", "XF", "XG", "XH", "XR"]},
                "CurrentBalance": {"type": "float", "min": 0},
                "AmountPastDue": {"type": "float", "min": 0},
                "OriginalCharge-offAmount": {"type": "float", "min": 0},
                "DateofAccountInformation": {"type": "string", "regex": "^\d{4}-\d{2}-\d{2}$"},
                "FCRACompliance-DateofFirstDelinquency": {"type": "string", "regex": "^\d{4}-\d{2}-\d{2}$"},
                "DateClosed": {"type": "string", "regex": "^\d{4}-\d{2}-\d{2}$", "required": False, "date_range": ["1950-01-01","2024-01-01"]},
                "DateofLastPayment": {"type": "string", "regex": "^\d{4}-\d{2}-\d{2}$"},
                "InterestTypeIndicator": {"type": "string", "allowed": ["F", "V"]},
                "ConsumerTransactionType": {"type": "string"},
                "GenerationCode": {"type": "string"},
                "ConsumerInformationIndicator": {"type": "string", "allowed": ["T", "U"]},
                "CountryCode": {"type": "string", "country": True},
                "City": {"type": "string"},
                "AddressIndicator": {"type": "string"},
                "AccountStatus": {"type": "string", "allowed": ["11", "13", "61", "62", "63", "64", "71", "78", "80", "82", "83", "84", "93", "95", "96", "97", "DA", "DF"]}
            }
        }
    }
}

def portfolio_type_to_account_type(portfolio_type):

    codes_for_account_type = portfolio_types.get(portfolio_type)

    if codes_for_account_type:
        return random.choice(codes_for_account_type)
    else:
        return None

def validate_account_type(portfolio_type, account_type):
    codes_for_account_type = portfolio_types.get(portfolio_type)

    if codes_for_account_type:
        return account_type in codes_for_account_type
    else:
        return False

class Metro2Validator(Validator):
    def _validate_date_range(self, date_range, field, value):
        ''' The rule's arguments are validated against this schema:
        {'type': 'list'} '''

        if not isinstance(value, str):
            self._error(field, f"Invalid data type for {field}. Expected string got {type(value).__name__}")

        if not re.match(r'^\d{4}-\d{2}-\d{2}$|^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$', value):
            self._error(field, f"Invalid date format for {field}. Expected YYYY-MM-DD")

        date_list = sorted([datetime.strptime(date, '%Y-%m-%d') for date in date_range])
        date_value = datetime.strptime(value.split("T")[0], '%Y-%m-%d')

        valid_start = date_list[0]
        valid_end = date_list[1]

        if date_value < valid_start or date_value > valid_end:
            self._error(field, f"The date {date_value} is out of range.  Must be between {valid_start} and {valid_end}.")

    def _validate_country(self, country, field, value):
        '''
            {'type': 'boolean'}
        '''
        if not pycountry.countries.get(alpha_2=value):
            self._error(field, f"{value} is not a valid ISO-3166-1 two-letter country code")

    def _validate_us_state(self, state, field, value):
        '''
            {'type': 'boolean'}
        '''
        if not us.states.lookup(value):
            self._error(field, f"{value} is not a valid two letter US postal abbreviation")

    def _validate_depends_on(self, mapping, field, value):
        """ { 'type': 'dict' } """

        property_name = mapping['property_name']
        mapping_func_name = mapping['mapping_func']

        property_value = self.document.get(property_name)

        # Assuming the mapping function is globally defined.
        mapping_func = globals()[mapping_func_name]

        # Assume mapping_func takes two arguments, first from the property that is dependent,
        # and second from the original field being validated.
        if not mapping_func(property_value, value):
            self._error(field, f"Failed 'depends_on' validation, referring to property: {property_name}")
