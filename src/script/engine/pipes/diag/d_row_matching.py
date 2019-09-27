# Do pandas inner join
import pandas as pd
import numpy as np

from engine.config import config as cf

from engine.pipes.diag.c_string_matching import get_source
from engine.pipes.diag.c_string_matching import get_fields


def group_by_func(table_source,fixed_fields_source,comparable_fields_source):

    nb_unique_values_source = pd.DataFrame()

    for column in comparable_fields_source:
        table_count = pd.DataFrame(table_source.groupby(fixed_fields_source.tolist())[column].nunique())

        nb_unique_values_source = pd.concat([nb_unique_values_source, table_count], axis=1)

    return (nb_unique_values_source)


def create_report_source(table_source,table_ID,fixed_fields_source,comparable_fields_source,nb_unique_values_source):

    nb_unique_values_source['SOURCE'] = table_ID.iloc[0]
    nb_unique_values_source['FIXED_FIELDS'] = str(fixed_fields_source.tolist())
    nb_unique_values_source['COMPARISON_FIELDS'] = str(comparable_fields_source.tolist())
    nb_unique_values_source['FIXED_VALUES'] = nb_unique_values_source.index.tolist()

    df_comparison = pd.DataFrame()

    df_comparison['FIXED_VALUES']= table_source[fixed_fields_source.tolist()]
    df_comparison['COMPARISON_VALUES'] = table_source[comparable_fields_source].apply(lambda x: '-'.join(map(str, x)), axis=1).values.tolist()

    df_result = pd.merge(nb_unique_values_source,df_comparison,on="FIXED_VALUES")
    return(df_result)

def row_matching(self,list_inputs_dict, df_files_mapping_dict, df_fields_mapping, df_row_matching):

    df_result = pd.DataFrame()
    my_ids_set = set(df_row_matching["ROW_MATCHING_ID"].tolist())

    for matching_id in my_ids_set:

        df_tmp = df_row_matching[df_row_matching.ROW_MATCHING_ID == matching_id]

        table_1_ID = df_tmp["SOURCE1_ID"]
        table_2_ID = df_tmp["SOURCE2_ID"]

        if (len(set(table_1_ID)) == len(set(table_2_ID)) == 1):

            table_source1, name_source1 = get_source(table_1_ID.iloc[0], df_files_mapping_dict, list_inputs_dict)
            table_source2, name_source2 = get_source(table_2_ID.iloc[0], df_files_mapping_dict, list_inputs_dict)

            df_fields = df_tmp[["TYPE", "FIELD_MAPPING_ID"]]

            list_fixed = df_fields[df_fields.TYPE == 'FIXED']["FIELD_MAPPING_ID"].tolist()
            list_to_compare = df_fields[df_fields.TYPE == 'TO COMPARE']["FIELD_MAPPING_ID"].tolist()
            fields_mapping = {'FIXED': list_fixed, 'TO COMPARE': list_to_compare}

            fixed_fields_source1, fixed_fields_source2 = get_fields(fields_mapping['FIXED'], df_fields_mapping,
                                                                    table_1_ID.iloc[0],
                                                                    table_2_ID.iloc[0])

            comparable_fields_source1, comparable_fields_source2 = get_fields(fields_mapping['TO COMPARE'],
                                                                              df_fields_mapping, table_1_ID.iloc[0],
                                                                              table_2_ID.iloc[0])

            nb_unique_values_source1 = group_by_func(table_source1,fixed_fields_source1,comparable_fields_source1)
            nb_unique_values_source2 = group_by_func(table_source2,fixed_fields_source2, comparable_fields_source2)

            if (len(nb_unique_values_source1) == len(nb_unique_values_source2) == 0):

                table_source1_tmp = table_source1
                table_source1_tmp['SOURCE'] = "SRC1"

                table_source2_tmp = table_source2
                table_source1_tmp['SOURCE'] = "SRC1"

                df_compare = pd.merge(table_source1[fixed_fields_source1.tolist() + comparable_fields_source1.tolist()],
                                      table_source2[fixed_fields_source2.tolist() + comparable_fields_source2.tolist()],
                                      how='inner', left_on = fixed_fields_source1.tolist(), right_on= fixed_fields_source2.tolist())

                df_result = df_compare[df_compare[comparable_fields_source1].values != df_compare[comparable_fields_source2].values]

                #result_merged_sources = create_report_source(df_result, fixed_fields_source2, comparable_fields_source2, nb_unique_values_source2)



            else :
                nb_unique_values_source1.columns = [list_to_compare]
                nb_unique_values_source2.columns = [list_to_compare]

                result_source1_tmp = create_report_source(table_source1,table_1_ID, fixed_fields_source1, comparable_fields_source1, nb_unique_values_source1)
                result_source2_tmp = create_report_source(table_source2,table_2_ID, fixed_fields_source2, comparable_fields_source2, nb_unique_values_source2)

                result_tmp = pd.concat([result_source1_tmp, result_source2_tmp])

                result_tmp['TMP']=result_tmp[list_to_compare].sum(axis=1)

                df_result = result_tmp[result_tmp['TMP'] >= 2]



    return ( df_result.drop('TMP', axis=1) )
