import pandas as pd
import random

def get_fields_type(self,df_input):

    columns = df_input.columns

    column_names = []
    columns_type = []

    columns_type_prct = []

    columns_min = []
    columns_max = []

    columns_nunique = []
    columns_example = []

    none_values = []
    filled_values = []

    for column in columns:

        #print(column)

        nb_True = 0
        nb_False = 0

        df_types = pd.DataFrame()

        min_value = None
        max_value = None

        set_values = set()

        column_names.append(column)

        lst = df_input[column]

        cleanedList = [x for x in lst if str(x) != 'nan']

        none_values.append(len([x for x in lst if str(x) == 'nan']))
        filled_values.append(len(cleanedList))

        if (len(cleanedList) > 0):

            columns_example.append(random.choice(cleanedList))

            types_list = [type(x) for x in cleanedList]
            set_lst = set(types_list)

            df_types["Types"] = [x for x in set_lst]
            df_types["Count_Types"] = [types_list.count(x) for x in set_lst]

            dominant_type = df_types.Types[df_types.Count_Types == max(df_types.Count_Types)].tolist()
            dominant_type_prct = (df_types.Count_Types[df_types.Count_Types == max(df_types.Count_Types)] / len(lst)).tolist()

            if (dominant_type == [str]):
                set_values = set(lst)
            else:
                if (len(cleanedList) > 0):
                    cleaned_list_unique_type = []
                    for x in cleanedList:
                        if type(x) != str:
                            cleaned_list_unique_type.append(x)
                    min_value = min(cleaned_list_unique_type)
                    max_value = max(cleaned_list_unique_type)
        #           else:
        #              min_value = "Empty column found"
        #               max_value = "Empty column found"

        else:
            columns_example.append("Empty column found")
            dominant_type = ["Empty column found"]
            dominant_type_prct = [1]

        columns_type.append(dominant_type)
        columns_type_prct.append(dominant_type_prct)
        columns_nunique.append(len(set_values))

        columns_min.append(min_value)
        columns_max.append(max_value)

    columns_type = [str(type).replace('[<class', '') for type in columns_type]
    columns_type = [str(type).replace('>]', '') for type in columns_type]
    columns_type = [str(type).replace('numpy.', '') for type in columns_type]
    columns_type = [str(type).replace('pandas.tslib.', '') for type in columns_type]

    dict_test = { "Fields" : column_names , 'Type' : columns_type, 'Type_Prct' : columns_type_prct ,'Filled_Values' : filled_values, 'Missing_Values' : none_values,
                      "Unique_values":columns_nunique, "Minimum":columns_min, "Maximum":columns_max, "Example" : columns_example}

    file_result = pd.DataFrame(dict_test)

    return(file_result)