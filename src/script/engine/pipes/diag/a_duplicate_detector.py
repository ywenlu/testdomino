# -*- coding: utf-8 -*-
import pandas as pd
from engine.config import stringref as st

def new_func(x, id_fields):
    res =''
    for f in id_fields :
        if len(res) > 0:
            res = res + " , " + str(x[f])
        else:
            res = res + str(x[f])
    return res

def duplicates(input_df, schema):
    columns = list(input_df.columns)
    df_duplicates = []
    df_result = pd.DataFrame()

    for index, row in schema.iterrows():
        ids_fields = []
        for col in schema.columns:
            if row[col] in columns:
                ids_fields.append(row[col])
            else:
                if row[col] == row[col]:
                    """
                    print (st.WARNING_START)
                    print ("Colonne [{}] non prise en compte dans la détéction des doublons. \nColonne non reconnue.".format(row[col]))
                    print ("Pour plus de détails, cf. ligne {}, colonne {} de la table des identifiants.".format(index+1, col))
                    print (st.WARNING_END)
                    """
                    pass

        if len(ids_fields)>0:
            df = input_df.copy()
            df[st.DUPLICATED] = df.duplicated(subset=ids_fields, keep=False)
            df[st.ID_FIELDS] = str(ids_fields)
            df = df[df.DUPLICATED == True]
            df.drop(st.DUPLICATED, axis=1, inplace = True)
            df[st.ID_COMBI] = df.apply(lambda x : new_func(x, ids_fields), axis =1)
            df = df[[st.ID_FIELDS, st.ID_COMBI] + columns]
            df_duplicates.append(df)

    if len(df_duplicates)>0:
        df_result = pd.concat(df_duplicates)




    return df_result