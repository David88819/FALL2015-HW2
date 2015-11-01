"""
File name: Homework 2 Question 2
Project name: Mortgage comparison
Author: Wei Dai, Yan Liu, Dong Niu, Yu Wen
Description: 1. Comparison of schedule monthly payments between a 30 years
                mortgage and the same mortgage but after we pay one point
             2. Comparison of schedule monthly payments between a 15 years
                mortgage and the same mortgage but after we pay one point
Date: Oct 31, 2015
"""


# Python imports
import sys
# 3rd party imports
import numpy as np
import pandas as pd


# Input command line arguments
argList = sys.argv
loanAmount = float(sys.argv[1])
interestRate = float(sys.argv[2]) / 100.
extraPmt = float(sys.argv[3])


def monthly_pmt(loan_amount, interest_rate_pmt, years, extra_pmt=0.):
    """
    Summary: It is calculating the monthly payment of mortgages
    :param loan_amount: the amount of the loan
    :param interest_rate_pmt: interest rate by month
    :param years: the number of years for the mortgage
    :param extra_pmt: extra payment to the principal (usually zero)
    :return: the amount of monthly payment of mortgages
    """
    # term is the number of month for 15 or 30 years
    global term
    if years == 15:
        term = 12 * 15
    elif years == 30:
        term = 12 * 30

    # pmt is the amount of monthly payment of 15 or 30 years
    pmt = loan_amount / float((1 - pow((1 + interest_rate_pmt / 12.), -term)) / (interest_rate_pmt / 12.)) + extra_pmt
    return pmt


def table_mortgage(years):
    """
    Summary: It is calculating a table including Beginning Balance, Monthly Payment, Interest, Principal, and
             Ending Balance
    :param years: the number of years for the mortgage
    :return: A table of 15 or 30 years mortgage
    """
    # set up a table named data, we will save result in this table
    global data
    if years == 15:
        data = np.zeros((180, 11))
    elif years == 30:
        data = np.zeros((360, 11))

    # change the interest rate
    global interest_rate
    if years == 15:
        interest_rate = interestRate / 1.2
    elif years == 30:
        interest_rate = interestRate

    # calculate the first series of the table (0 point)
    pmt = monthly_pmt(loanAmount, interest_rate, years, extraPmt)
    beginning_balance = loanAmount
    interest = beginning_balance * (interest_rate / 12.)
    principal = pmt - interest + extraPmt
    ending_balance = beginning_balance - principal

    # calculate the first series of the table (1 point)
    pmt_point = monthly_pmt(loanAmount, interest_rate - 0.0025, years, extraPmt)
    beginning_balance_point = loanAmount
    interest_point = beginning_balance_point * ((interest_rate - 0.0025) / 12.)
    principal_point = pmt_point - interest_point + extraPmt
    ending_balance_point = beginning_balance_point - principal_point

    # input results in the table named data
    data[0, 0] = beginning_balance
    data[0, 1] = pmt
    data[0, 2] = interest
    data[0, 3] = principal
    data[0, 4] = ending_balance

    # using 'None' to separate two sub-tables
    data[0, 5] = None

    data[0, 6] = beginning_balance_point
    data[0, 7] = pmt_point
    data[0, 8] = interest_point
    data[0, 9] = principal_point
    data[0, 10] = ending_balance_point

    # calculating the rest series of the table
    global index
    if years == 15:
        index = 180
    elif years == 30:
        index = 360

    for pmt_num in xrange(1, index, 1):
        # calculating the rest series of 0 point
        beginning_balance = ending_balance
        interest = beginning_balance * (interest_rate / 12.)
        principal = pmt - interest + extraPmt
        ending_balance = beginning_balance - principal

        # input results in the table named data
        data[pmt_num, 0] = beginning_balance
        data[pmt_num, 1] = pmt
        data[pmt_num, 2] = interest
        data[pmt_num, 3] = principal
        data[pmt_num, 4] = ending_balance

        # using 'None' to separate two sub-tables
        data[pmt_num, 5] = None

        # calculating the rest series of 1 point
        beginning_balance_point = ending_balance_point
        interest_point = beginning_balance_point * ((interest_rate - 0.0025) / 12.)
        principal_point = pmt_point - interest_point + extraPmt
        ending_balance_point = beginning_balance_point - principal_point

        # input results in the table named data
        data[pmt_num, 6] = beginning_balance_point
        data[pmt_num, 7] = pmt_point
        data[pmt_num, 8] = interest_point
        data[pmt_num, 9] = principal_point
        data[pmt_num, 10] = ending_balance_point

    result = pd.DataFrame(data)
    # save results to a text file
    if years == 15:
        np.savetxt("15 Years Mortgage.txt", result, delimiter='\t', fmt='{: ^10}'.format('%.2f'),
                   header="\t\tThe Monthly Payments of 15 Years Mortgage (0 point)"
                          "\t\t\t\t\t\tThe Monthly Payments of 15 Years Mortgage (1 point)",
                   comments="Comments:\tTwo sub-table are separated by 'nan'"
                            "\nThe 1st column is Beginning Balance (0 point)."
                            "\t\tThe 6th column is Beginning Balance (1 point)."
                            "\nThe 2nd column is Monthly Payment (0 point)."
                            "\t\tThe 7th column is Monthly Payment (1 point)"
                            "\nThe 3nd column is Interest (0 point)."
                            "\t\t\tThe 8nd column is Interest (1 point)."
                            "\nThe 4th column is Principal (0 point)."
                            "\t\t\tThe 9th column is Principal (1 point)."
                            "\nThe 5th column is ending Balance (0 point)."
                            "\t\tThe 10th column is ending Balance (1 point).\n\n\n")
    elif years == 30:
        np.savetxt("30 Years Mortgage.txt", result, delimiter='\t', fmt='{: ^10}'.format('%.2f'),
                   header="\t\tThe Monthly Payments of 30 Years Mortgage (0 point)"
                          "\t\t\t\t\t\tThe Monthly Payments of 30 Years Mortgage (1 point)",
                   comments="Comments:\tTwo sub-table are separated by 'nan'"
                            "\nThe 1st column is Beginning Balance (0 point)."
                            "\t\tThe 6th column is Beginning Balance (1 point)."
                            "\nThe 2nd column is Monthly Payment (0 point)."
                            "\t\tThe 7th column is Monthly Payment (1 point)"
                            "\nThe 3nd column is Interest (0 point)."
                            "\t\t\tThe 8nd column is Interest (1 point)."
                            "\nThe 4th column is Principal (0 point)."
                            "\t\t\tThe 9th column is Principal (1 point)."
                            "\nThe 5th column is ending Balance (0 point)."
                            "\t\tThe 10th column is ending Balance (1 point).\n\n\n")


if __name__ == "__main__":
    table_mortgage(30)
    table_mortgage(15)




