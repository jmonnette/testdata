import json
import random
import datetime
import sys
from faker import Faker
import metro2

def generate_json(numObjects):
    fake = Faker()
    all_data = []

    for i in range(int(numObjects)):
        account_list = []
        for i in range(random.randint(0,20)):
            portfolio_type = random.choice(['R','I','O','M','C'])
            account_type = metro2.portfolio_type_to_account_type(portfolio_type)

            account = {
                "ProcessingIndicator":1,
                "TimeStamp":fake.date_time_between(start_date='-90d', end_date='now').isoformat(),
                "CorrectionIndicator":random.randint(0,1),
                "IdentificationNumber":fake.pystr_format(string_format='??????????????????'),
                "CycleIdentifier":fake.pystr_format(string_format='??'),
                "ConsumerAccountNumber":fake.pystr_format(string_format='??????????????????????????????'),
                "PortfolioType":portfolio_type,
                "AccountType":account_type,
                "DateOpened":fake.date_between(start_date='-30y', end_date='now').isoformat(),
                "CreditLimit":random.uniform(0, 1000),
                "HighestCreditorOriginalLoanAmount":random.uniform(0, 2000),
                "TermsDuration":"12",
                "TermsFrequency":random.choice(['D','P','W','B','E','M','L','Q','T','S','Y']),
                "ScheduledMonthlyPaymentAmount":random.uniform(0, 100),
                "ActualPaymentAmount":random.uniform(0, 100),
                "PaymentHistoryProfile":metro2.generate_payment_history_profile(),
                "SpecialComment":random.choice(['M','AP','BL','CI','AM','']),
                "ComplianceConditionCode":random.choice(['XB','XC','XF','XG','XH','XR']),
                "CurrentBalance":random.uniform(0, 10000),
                "AmountPastDue":random.uniform(0, 10),
                "OriginalCharge-offAmount":random.uniform(0, 20),
                "DateofAccountInformation":fake.date_between(start_date='-30y', end_date='now').isoformat(),
                "FCRACompliance-DateofFirstDelinquency":fake.date_between(start_date='-30y', end_date='now').isoformat(),
                "DateClosed":fake.date_between(start_date='-30y', end_date='now').isoformat(),
                "DateofLastPayment":fake.date_between(start_date='-30y', end_date='now').isoformat(),
                "InterestTypeIndicator":random.choice(['F','V']),
                "ConsumerTransactionType":"A",
                "GenerationCode":"",
                "ConsumerInformationIndicator":random.choice(['T','U']),
                "CountryCode":fake.country_code(representation='alpha-2'),
                "City":fake.city(),
                "AddressIndicator":"A",
                "AccountStatus":random.choice(['11','13','61','62','63','64','71','78','80','82','83','84','93','95','96','97','DA','DF'])
            }
            account_list.append(account)

        person = {
            "DateofBirth":fake.date_of_birth(minimum_age=30,maximum_age=70).isoformat(),
            "ECOACode":random.choice(['1','2','3','5','7','T','X','W','Z']),
            "FirstLineofAddress":fake.street_address(),
            "FirstName":fake.first_name(),
            "MiddleName":fake.first_name(),
            "Postal-ZipCode":fake.zipcode(),
            "ResidenceCode":"1",
            "SecondLineofAddress":"",
            "SocialSecurityNumber":fake.unique.ssn(),
            "State":fake.state_abbr(include_freely_associated_states = False),
            "Surname":fake.last_name(),
            "TelephoneNumber":fake.pystr_format(string_format='###-###-####'),
            "Accounts":account_list
        }
        all_data.append(person)

    with open('data.json', 'w') as f:
        json.dump(all_data, f)

if __name__ == "__main__":
    numObjects = sys.argv[1]
    generate_json(numObjects)
