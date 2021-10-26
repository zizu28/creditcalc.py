import argparse
import math

parser = argparse.ArgumentParser(description='For calculation of both annuity and differentiated payments.')

parser.add_argument('--type', required=True, choices=["annuity", "diff"], help="Please select the type of "
                                                                               "payment: 'annuity' or 'diff' "
                                                                               "(annuity or differentiated).")
parser.add_argument('--principal', type=int, help="It is used for calculations of both types of payment. You can get "
                                                  "its value if you know the interest, annuity payment,"
                                                  "and number of months.")
parser.add_argument('--periods', type=int, help="It denotes the number of months needed to repay the loan. "
                                                "It's calculated based on the interest, "
                                                "annuity payment,and principal.")
parser.add_argument('--interest', type=float, help="It is specified without a percent sign. Note that it can accept a "
                                                   "floating-point value. Our loan calculator can't calculate the "
                                                   "interest, so it must always be provided.")
parser.add_argument('--payments', type=int, help="It denotes the monthly payment made")

args = parser.parse_args()

args_list = []

for arg in vars(args):
    if getattr(args, arg) is not None:
        args_list.append(getattr(args, arg))

differentiated_payment = 0
annuity_payment = 0

amounts_diff = []

amounts_annuity = []

if args.interest is None or args.type not in ("diff", "annuity") or len(args_list) != 4:
    print("Incorrect parameters")

if args.type == 'annuity' and (args.principal and args.periods and args.interest):
    nominal_interest_rate = (args.interest / 100) / 12
    exp = math.pow((1 + nominal_interest_rate), args.periods)
    mono = ((nominal_interest_rate * exp) / (exp - 1))
    annuity_payment = math.ceil(args.principal * mono)
    overpayment_annuity = (annuity_payment * args.periods) - args.principal
    print(f'Your annuity payment = {annuity_payment}!\nOverpayment = {overpayment_annuity}')

elif args.type == 'annuity' and (args.payments and args.periods and args.interest):
    nominal_interest_rate = (args.interest / 100) / 12
    exp = math.pow((1 + nominal_interest_rate), args.periods)
    mono = ((nominal_interest_rate * exp) / (exp - 1))
    loan_principal = math.ceil(args.payments / mono)
    overpayment = (args.payments * args.periods) - loan_principal
    print(f'Your loan principal = {loan_principal}!\nOverpayment = {overpayment}')

elif args.type == 'annuity' and (args.principal and args.payments and args.interest):
    nominal_interest_rate = (args.interest / 100) / 12
    number_of_payments = math.ceil((math.log(args.payments / (args.payments - (nominal_interest_rate * args.principal)),
                                             1 + nominal_interest_rate)))
    a_year = 12
    years = number_of_payments // a_year
    months = number_of_payments % a_year
    overpayment = (number_of_payments * args.payments) - args.principal
    if years == 0:
        if months > 1:
            print(f'It will take {months} months to repay this loan!\nOverpayment = {overpayment}')
        else:
            print(f'It will take {months} month to repay this loan!\nOverpayment = {overpayment}')
    else:
        if years == 1 and months > 1:
            print(f'It will take {years} year and {months} months to repay this loan!\nOverpayment = {overpayment}')
        elif years > 1 and months == 0:
            print(f'It will take {years} years to repay this loan!\nOverpayment = {overpayment}')
        else:
            print(f'It will take {years} years and {months} months to repay this loan!\nOverpayment = {overpayment}')

if args.type == 'diff' and (args.principal < 0 or args.periods < 0 or args.interest < 0):
    print('Incorrect parameters')

elif args.type == 'diff' and args.principal is not None and args.periods is not None and args.interest is not None:
    nominal_interest_rate = (args.interest / 100) / 12
    for i in range(1, args.periods + 1):
        z = args.principal * ((args.periods - i + 1) / args.periods)
        differentiated_payment = math.ceil((args.principal / args.periods) + (nominal_interest_rate * z))
        amounts_diff.append(differentiated_payment)
        print(f'Month {i}: payment is {round(differentiated_payment)}')
    overpayment_diff = sum(amounts_diff) - args.principal
    print(f'Overpayment = {round(overpayment_diff)}')
