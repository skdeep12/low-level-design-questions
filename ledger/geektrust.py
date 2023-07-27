
import sys

# LOAN BANK_NAME BORROWER_NAME PRINCIPAL NO_OF_YEARS RATE_OF_INTEREST
# PAYMENT BANK_NAME BORROWER_NAME LUMP_SUM_AMOUNT EMI_NO


# BALANCE BANK_NAME BORROWER_NAME EMI_NO
# bank, loan, borrower, payment, balance
class LumpsumPaymet:
    amount_in_rupees: int = None
    after_emi_no: int = None

    def __init__(self, amount, after_emi_no):
        self.amount_in_rupees = amount
        self.after_emi_no = after_emi_no


class Loan:
    id: int = 0
    tenure_in_years: int = 0
    rate_of_interest: float = 0
    principal_amount: int = 0
    total_amount: int = 0
    emi_amount: int = 0
    lumpSumPayments: []

    def __init__(self, principal_amount, tenure_in_years, rate_of_interest):
        self.tenure_in_years = tenure_in_years
        self.rate_of_interest = rate_of_interest
        self.principal_amount = principal_amount
        self.total_amount = self.principal_amount + (principal_amount * tenure_in_years * rate_of_interest) / 100
        emi_amount = self.total_amount / (12 * tenure_in_years)
        if int(emi_amount) == emi_amount:
            self.emi_amount = emi_amount
        else:
            self.emi_amount = int(emi_amount) + 1
        self.lumpSumPayments = list()

    def get_remaining_amount_after_nth_emi(self, n, lump_sum_amount):
        amount_paid = self.emi_amount * n + lump_sum_amount
        remaining_amount = self.total_amount - amount_paid
        return amount_paid, remaining_amount

    def record_payment(self, payment: LumpsumPaymet):
        self.lumpSumPayments.append(payment)
        self.lumpSumPayments.sort(key=lambda x: x.after_emi_no)

    def get_balance_paid_till(self, emi_no):
        return int(emi_no * self.emi_amount + self.__get_lumpsum_amount_till(emi_no))

    def __get_lumpsum_amount_till(self, emi_no):
        amount = 0
        for payment in self.lumpSumPayments:
            if payment.after_emi_no > emi_no:
                break
            else:
                amount += payment.amount_in_rupees
        return amount

    def get_remaining_number_of_emis_after(self, emi_no):
        remaining_amount = self.total_amount - self.get_balance_paid_till(emi_no)
        remaining_emis = remaining_amount/self.emi_amount
        if remaining_emis == int(remaining_emis):
            return int(remaining_emis)
        return int(remaining_emis)+1


class Bank:
    name: str = None
    borrowers = dict()

    def __init__(self, name):
        self.name = name

    def add_borrower(self, customer_name, loan: Loan):
        if customer_name not in self.borrowers:
            self.borrowers[customer_name] = Borrower(customer_name)
            self.borrowers[customer_name].add_loan(loan)
        else:
            print("already a loan present for the borrower")

    def record_payment(self, customer_name, payment: LumpsumPaymet):
        if customer_name not in self.borrowers:
            print("invalid payment")
            return
        self.borrowers[customer_name].record_payment_for_loan(payment)

    def get_balance_for_customer(self, customer_name, emi_no):
        return self.borrowers[customer_name].get_balance_and_remaining_emis_till_emi_number(emi_no)


class Borrower:
    id: int = 0
    name: str = None
    loan: Loan = None

    def __init__(self, name):
        self.name = name

    def add_loan(self, loan):
        self.loan = loan

    def get_balance_and_remaining_emis_till_emi_number(self, emi_no):
        amount_paid = self.loan.get_balance_paid_till(emi_no)
        remaining_emis = self.loan.get_remaining_number_of_emis_after(emi_no)
        return amount_paid, remaining_emis

    def record_payment_for_loan(self, payment):
        self.loan.record_payment(payment)

class Driver:
    banks = dict()

    def add_borrower(self, command: list):
        bank_name = command[0]
        borrower_name = command[1]
        principal_amount = int(command[2])
        tenure_in_years = int(command[3])
        rate_of_interest = float(command[4])
        loan = Loan(principal_amount, tenure_in_years, rate_of_interest)
        if bank_name not in self.banks:
            self.banks[bank_name] = Bank(bank_name)
        self.banks[bank_name].add_borrower(borrower_name, loan)

    def record_payment(self, command: list):
        bank_name = command[0]
        borrower_name = command[1]
        amount = int(command[2])
        after_emi_no = int(command[3])
        lumpsum_paymet = LumpsumPaymet(amount, after_emi_no)
        self.banks[bank_name].record_payment(borrower_name, lumpsum_paymet)

    def get_balance(self, command: list):
        bank_name = command[0]
        borrower_name = command[1]
        emi_no = int(command[2])
        amount_paid, remaining_emis = self.banks[bank_name].get_balance_for_customer(borrower_name, emi_no)
        print(f"{bank_name} {borrower_name} {amount_paid} {remaining_emis}")

    def process_command(self, command):
        command = command.split()
        if command[0] == "LOAN":
            self.add_borrower(command[1:])
        elif command[0] == "BALANCE":
            self.get_balance(command[1:])
        elif command[0] == "PAYMENT":
            self.record_payment(command[1:])
        else:
            print("invalid command")


def main():
    driver = Driver()
    input_file = sys.argv[1]
    # sys.argv[1] should give the absolute path to the input file
    # parse the file and process the command
    # print the output
    with open(input_file) as f:
        commands = f.read().split("\n")
        for command in commands:
            driver.process_command(command)


if __name__ == "__main__":
    main()
