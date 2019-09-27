import os
import xlsxwriter
import pandas as pd
import dateparser
import datetime as dt
from random import *
from engine.config import config as cf
from engine.utilities.sherlock import sherlock_processor
from engine.utilities.sherlock.sherlock_processor import _extract_type_from_schema

def check_schema(schema_list, schema_name):
    with_schema = False
    if schema_name in schema_list:
        with_schema = True
    return with_schema


def extract_schema(schema_path):
    """
    :param schema_path: dir + schema name for one input file
    :return:
    """
    schema_sherlock, schema_required_if, = sherlock_processor.load_schemas(schema_path)
    schema_duplicates = pd.read_excel(schema_path, sheet_name=cf.ID)
    schema_address = pd.read_excel(schema_path, sheet_name=cf.ADDRESS)

    schemas = {
        'duplicates': schema_duplicates,
        'address': schema_address,
        'sherlock': schema_sherlock,
        'required_if': schema_required_if
    }
    
    return schemas

def schemaToExcel(dic, input_name, schema_dir):
    path = schema_dir + 'schema_' + input_name + '.xlsx'
    workbook = xlsxwriter.Workbook(path)
    for x in dic:
        worksheet = workbook.add_worksheet(x)
        j = 0
        for y in dic[x]:
            i = 1
            worksheet.write(0, j, y)
            for text in dic[x][y]:
                worksheet.write(i, j, text)
                i += 1
            j += 1

    workbook.close()
    return path

def forceDate(df, dtype):
    for x in dtype:
        if dtype[x] == dt.datetime or dtype[x] == dt.date:
            for i in range(len(df[x])):
                if dateparser.parse(df[x][i]):
                    df[x][i] = dateparser.parse(df[x][i])
            #df[x] = pd.to_datetime(df[x], errors='ignore')
    return df

def load_input(input_dict, schema_dict, schema_dir):
    
    inputs = {}
    n = randint(100000,1000000)
    schema = schemaToExcel(schema_dict, str(n), schema_dir)
    schemas = extract_schema(schema)
    dftype = _extract_type_from_schema(schemas['sherlock'])
    input_df = pd.DataFrame.from_dict(input_dict).astype(dftype, errors='ignore')

    forceDate(input_df, dftype)
    input_df = sherlock_processor.process_input(input_df)
    inputs[str(n)] = {'input': input_df, 'schemas':  schemas}
    return inputs


def load_cross_schema(schema_dir):
    schema_path = schema_dir + 'schema_cross_validation.xlsx'

    df_files = pd.ExcelFile(schema_path)

    df_files_mapping = df_files.parse("FILES_MAPPING")
    df_files_mapping.fillna("", inplace=True)

    df_files_mapping_dict_tmp = df_files_mapping.to_dict(orient="records")
    df_files_mapping_dict = {elt['SOURCE_ID']: elt['FILE_NAME'] for elt in df_files_mapping_dict_tmp if
                             len(elt['FILE_NAME']) > 0}

    df_fields_mapping = df_files.parse("FIELDS_MAPPING")
    df_fields_mapping.fillna("", inplace=True)
    df_fields_mapping = df_fields_mapping[df_fields_mapping["FIELD_MAPPING_ID"] != '']

    df_str_matching = df_files.parse("STR_MATCHING")
    df_str_matching.fillna("", inplace=True)

    df_row_matching = df_files.parse("ROW_MATCHING")
    df_row_matching.fillna("", inplace=True)

    return df_files_mapping_dict, df_fields_mapping, df_str_matching, df_row_matching
