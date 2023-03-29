"""File parsing script
This script allows to generate .txt file with needed configuration from the input file.

This script accepts Excel (.xlsx) file

This script generates .txt file in the django directory and returns nothing

Main fucntion is file_parse()
"""

from math import isnan

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


# check if string input is float
def convert_to_float(n):
    if check_numeric(n):
        n = str(n)
        n = n.replace(',', '.')
        result = float(n)
    else:
        result = n
    return result


# check if string input is integer
def convert_to_int(n):
    if check_numeric(n):
        n = str(n)
        n = n.replace(',', '.')
        result = int(round(float(n)))
    else:
        result = n
    return result


def check_numeric(a_string):
    try:
        a_string = str(a_string)
        a_string = a_string.replace(',', '.')
        a_float = float(a_string)
        if isnan(a_float):
            raise ValueError
        return True
    except ValueError:
        return False


def check_empty_and_nan_member_id(df, column):
    error_indexes = df[column].index[df[column].apply(pd.isnull)]
    df_index = df.index.values.tolist()
    error_indexes_list = [df_index.index(i) + 2 for i in error_indexes]
    if error_indexes_list:
        raise ValueError(f'Empty {column} in the rows: {error_indexes_list}')


def file_parse(file):
    """
    Main fuction of this script
    :param file: accepts the Excel file
    :return: full string separated to the rows, ready to write to the file
    """
    df = pd.read_excel(file)
    #Check member_id column for empty cells
    check_empty_and_nan_member_id(df, 'member_id')
    check_empty_and_nan_member_id(df, 'fasting')
    # Mapping and creating first static part of the column output (header_str)
    HEADER_NAME = [
        'Record Type',
        'Sending Facility ID',
        'Sending Facility ID Type',
        'Receiving Facility ID',
        'Receiving Facility ID Type',
        'File Date Time',
        'Message Control ID',
        'Processing Details',
        'Date Period Begin',
        'Data Period End',
        'Record Count'
    ]
    time_now = datetime.now()
    delta = timedelta(days=1)
    file_date = time_now.strftime('%Y%m%d%H%M%S') + '0000'
    period_date = (time_now - delta).strftime('%Y%m%d')
    header_values = {
        'Record Type': 'HDR',
        'Sending Facility ID': '570769093',
        'Sending Facility ID Type': 'TAX',
        'Receiving Facility ID': '570287419',
        'Receiving Facility ID Type': 'TAX',
        'File Date Time': file_date,
        'Message Control ID': '20210603FRAMPTON',
        'Processing Details': 'PROD',
        'Date Period Begin': period_date,
        'Data Period End': period_date,
        'Record Count': str(df.shape[0] * 13)
    }
    header_str = ''
    for col_name in HEADER_NAME:
        if col_name in header_values.keys():
            header_str += header_values[col_name] + '|'
        else:
            header_str += '|'

    # Mapping and creating second static part of the column output (details_str)
    DETAILS_PRIMARY_NAME = [
        'Record Type',
        'Subscriber ID',
        'Subscriber ID Type',
        'Member ID',
        'Member ID Type',
        'Patient First Name',
        'Patient Middle Name',
        'Patient Last Name',
        'Patient Date of Birth',
        'Patient Sex',
        'Patient Consent Status',
        'Patient Address Type',
        'Patient Street Address 1',
        'Patient Street Address 2',
        'Patient City',
        'Patient State',
        'Patient ZIP',
        'Patient Country',
        'Patient Primary phone number',
        'Patient Secondary phone number',
        'Patient Marital Status',
        'Patient Race',
        'Patient Death Indicator',
        'Patient Death Date and Time',
        'Smoking Status',
        'Smoking Quit Date',
        'Placer Order Number',
        'Filler Order Number',
        'Universal Service ID',
        'Universal Service ID Type',
        'Universal Service Name',
        'Order Date',
        'Ordering Provider ID',
        'Ordering Provider ID Type',
        'Date - Time of Results or Status Change',
        'Procedure Code',
        'Procedure Code Modifiers',
        'Procedure Code type',
        'Diagnosis Code',
        'Diagnosis Code type',
        'Order Only Indicator'
    ]
    details_primary_values = {
        'Record Type': 'DTL',
        'Subscriber ID Type': 'MB',
        'Member ID Type': 'AC'
    }
    DETAILS_SECONDARY_NAME = [
        'Observation Value Type',
        'Observation ID',
        'Observation ID Type',
        'Observation Name',
        'Observation Sub-ID',
        'Observation Value Text',
        'Observation Value Numeric Integer',
        'Observation Value Numeric Decimal',
        'Observation Units',
        'Reference Range Low',
        'Reference Range High',
        'Abnormal Flags',
        'Observation Result Status',
        'Observation Date Time',
        'Analysis Date Time',
        'Performing Provider ID',
        'Performing Provider ID Type',
        'Performing Provider Location'
    ]
    details_secondary_values = {
        'Observation Value Type': 'NM',
        'Observation Result Status': 'F',
        'Performing Provider ID': '1154508265',
        'Performing Provider ID Type': 'NPI',
        'Performing Provider Location': 'Columbia 29201'
    }

    details_str = ''
    for index, row in df.iterrows():
        details_primary_values['Subscriber ID'] = convert_to_int(row.get('member_id'))
        details_primary_values['Patient First Name'] = row.get('first_name')
        details_primary_values['Patient Last Name'] = row.get('last_name')
        details_primary_values['Patient Sex'] = row.get('gender')
        details_primary_values['Patient Date of Birth'] = row.get('dob').strftime('%Y%m%d')
        row_primary_str = '\n' + create_str(DETAILS_PRIMARY_NAME, details_primary_values)
        details_secondary_values['Observation Date Time'] = \
            row.screening_date.strftime('%Y%m%d')
        details_dynamic_values = {
            1: ['BPSYSTOLIC', 'MMHG', convert_to_int(row.get('systolic_bp'))],
            2: ['BPDIASTOLIC', 'MMHG', convert_to_int(row.get('diastolic_bp'))],
            3: ['TOTALCHOL', 'MG/DL', convert_to_int(row.get('total_cholesterol'))],
            4: ['HDL', 'MG/DL', convert_to_int(row.get('hdl'))],
            5: ['LDL', 'MG/DL', convert_to_int(row.get('ldl'))],
            6: ['TRIGLYCERIDE', 'MG/DL', convert_to_int(row.get('triglyceride'))],
            7: ['CHOL/HDL', 'RATIO', convert_to_float(row.get('cholesterol_ratio'))],
            8: [(lambda x: 'GLUCOSFAST' if x.lower() == 'yes' else 'GLUCOSNOFAST')(row.fasting),
                'MG/DL', convert_to_int(row.get('glucose'))],
            9: ['HEIGHT', 'IN', convert_to_int(row.get('height_inches_total'))],
            10: ['WEIGHT', 'LBS', convert_to_int(row.get('weight'))],
            11: ['BMI', 'RATIO', convert_to_float(row.get('bmi'))],
            12: ['WAIST', 'IN', (lambda x: '' if x == 'N/A' else x)(row.waist)],
            13: ['A1C', 'PERCENT', convert_to_float(row.get('hba1c'))]
        }

        for i in range(1, 14):
            details_secondary_values['Observation Sub-ID'] = i
            details_secondary_values['Observation Name'] = details_dynamic_values[i][0]
            details_secondary_values['Observation Units'] = details_dynamic_values[i][1]
            if i not in (7, 11, 13):
                details_secondary_values['Observation Value Numeric Integer'] = \
                    details_dynamic_values[i][2]
            else:
                details_secondary_values['Observation Value Numeric Decimal'] = \
                    details_dynamic_values[i][2]
            row_secondary_str = create_str(DETAILS_SECONDARY_NAME, details_secondary_values)
            details_str += row_primary_str + row_secondary_str
            details_secondary_values['Observation Value Numeric Integer'] = ''
            details_secondary_values['Observation Value Numeric Decimal'] = ''

    full_str = header_str + details_str
    return str(full_str)


# create string from headers and values
def create_str(header: list, values: dict) -> str:
    my_str = ''
    for col_name in header:
        if col_name in values.keys():
            if not pd.isna(values[col_name]):
                my_str += str(values[col_name]) + '|'
            else:
                my_str += '|'
        else:
            my_str += '|'
    return my_str


# optional file encryption
def encrypt_file(filename):
    return filename
