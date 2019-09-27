# Do pandas inner join
import pandas as pd
import numpy as np
from engine.config import config as cf

def levenshtein_ratio_and_distance(s, t, ratio_calc):
    """ levenshtein_ratio_and_distance:
        Calculates levenshtein distance between two strings.
        If ratio_calc = True, the function computes the
        levenshtein distance ratio of similarity between two strings
        For all i and j, distance[i,j] will contain the Levenshtein
        distance between the first i characters of s and the
        first j characters of t
    """
    # Initialize matrix of zeros
    rows = len(s)+1
    cols = len(t)+1
    distance = np.zeros((rows,cols),dtype = int)

    # Populate matrix of zeros with the index of each character of both strings
    for i in range(1, rows):
        for k in range(1,cols):
            distance[i][0] = i
            distance[0][k] = k

    # Iterate over the matrix to compute the cost of deletions,insertions and/or substitutions
    for col in range(1, cols):
        for row in range(1, rows):
            if s[row-1] == t[col-1]:
                cost = 0 # If the characters are the same in the two strings in a given position [i,j] then the cost is 0
            else:
                # In order to align the results with those of the Python Levenshtein package, if we choose to calculate the ratio
                # the cost of a substitution is 2. If we calculate just distance, then the cost of a substitution is 1.
                if ratio_calc == True:
                    cost = 2
                else:
                    cost = 1
            distance[row][col] = min(distance[row-1][col] + 1,      # Cost of deletions
                                 distance[row][col-1] + 1,          # Cost of insertions
                                 distance[row-1][col-1] + cost)     # Cost of substitutions
    if ratio_calc == True:
        # Computation of the Levenshtein Distance Ratio
        Ratio = ((len(s)+len(t)) - distance[row][col]) / (len(s)+len(t))
        return Ratio
    else:
        # print(distance) # Uncomment if you want to see the matrix showing how the algorithm computes the cost of deletions,
        # insertions and/or substitutions
        # This is the minimum number of edits needed to convert string a to string b
        return "The strings are {} edits away".format(distance[row][col])


def merge_columns(df,columns_names):

    # Merge the content of the specified columns of a data frame

    for column in columns_names:
        if( isinstance(df[column],str) == False):
            df[column] = df[column].astype(str)

    return(df.apply(lambda x: " ".join(x), axis=1))


def get_source(id_source, files_mapping_schema, list_inputs_dict):

    file_name = files_mapping_schema[id_source]

    df_source = list_inputs_dict[file_name]["input"]

    return df_source,file_name

def get_fields(field_mapping_ids,fields_mapping_schema,id_source1,id_source2):

    row = fields_mapping_schema[fields_mapping_schema.FIELD_MAPPING_ID.isin(field_mapping_ids)]

    field_source1 = row[id_source1]
    field_source2 = row[id_source2]

    return field_source1,field_source2

def str_matching(self,list_inputs_dict, df_files_mapping_dict, df_fields_mapping, df_str_matching):

    df_result = pd.DataFrame()
    df_list = []
    my_ids_set = set(df_str_matching["MATCHING_ID"])

    # Get file names, and comparison fields from schema

    for matching_id in my_ids_set:

        df_tmp = df_str_matching[df_str_matching.MATCHING_ID == matching_id]
        table_1_ID = df_tmp["SOURCE1_ID"]
        table_2_ID = df_tmp["SOURCE2_ID"]

        if ( len(set(table_1_ID)) == len(set(table_2_ID)) == 1):

            table_source1,name_source1 = get_source(table_1_ID.iloc[0], df_files_mapping_dict, list_inputs_dict)
            table_source2,name_source2 = get_source(table_2_ID.iloc[0], df_files_mapping_dict, list_inputs_dict)

            fields_mapping_id = df_tmp["FIELD_MAPPING_ID"].tolist()

            fields_source1, fields_source2 = get_fields(fields_mapping_id, df_fields_mapping, table_1_ID.iloc[0],
                                                        table_2_ID.iloc[0])


            df1 = table_source1[fields_source1]
            df2 = table_source2[fields_source2]

            if ( (table_source1[fields_source1].iloc[0]).dtypes ==(table_source2[fields_source2].iloc[0]).dtypes == object ):

                df1['Merge_Source1'] = merge_columns(df1, fields_source1)
                df2['Merge_Source2'] = merge_columns(df2, fields_source2)

                list1 = df1['Merge_Source1'].tolist()
                list2 = df2['Merge_Source2'].tolist()

                list = [[x, y] for x in list1 for y in list2]

                df_matching = pd.DataFrame(list, columns={"source1", "source2"})

                list_distances = []

                for index, row in df_matching.iterrows():
                    list_distances.append(
                        levenshtein_ratio_and_distance(row['source2'].lower(), row['source1'].lower(), ratio_calc=True))

                df_matching['distance'] = list_distances
                df_matching['MATCHING_ID'] = matching_id
                df_matching['NAME_Source1'] = name_source1
                df_matching['NAME_Source2'] = name_source2
                df_matching['MATCHING_Fields_Source1'] = str(fields_source1.tolist())
                df_matching['MATCHING_Fields_Source2'] = str(fields_source2.tolist())

                df_list.append(df_matching)
            else:
                pass
                #print(matching_id,cf.err_msg_strmatching % df_tmp.FIELD_MAPPING_ID.values)


    if len(df_list) > 0:
        df_result = pd.concat(df_list)

    return df_result

