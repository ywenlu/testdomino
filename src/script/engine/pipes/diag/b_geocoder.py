import pandas as pd
from engine.config import stringref as st, config as cf
from engine.utilities.geocode.helpers import run_queries


class Geocoder:
    def __init__(self, input_df, schema_address):
        self.input_df = input_df
        self.schema_address = schema_address
        self.list_df_response = []
        self.df_response = pd.DataFrame()

    def make_queries(self, address_list,field):
        return address_list[field]

    def similarity_score(self, x):
        result = 0
        if x[st.NB_CAR_DIFF] != 999:
            result = (len(x[st.QUERY]) + len(x[st.RESPONSE]) - x[st.NB_CAR_DIFF]) / (len(x[st.QUERY]) + len(x[st.RESPONSE]))
        return result

    def responses_to_df(self, df_responses, field):

        responses = df_responses[st.QUERY_RES]
        df_responses[st.FIELD] = field
        df_responses[st.RESPONSE] = [r.get_resp_address() for r in responses]
        df_responses[st.NB_CAR_DIFF] = [r.score for r in responses]
        df_responses[st.SCORE] = df_responses.apply(lambda x : self.similarity_score(x), axis =1)
        df_responses = df_responses[(df_responses[st.NB_CAR_DIFF] == 999) | (df_responses[st.SCORE] < 0.7)]
        df_responses[st.RISK_LEVEL] = ["High" if (diff == 999) else "Medium" for diff in df_responses[st.NB_CAR_DIFF]]

        df_responses.drop(st.QUERY_RES, axis=1, inplace=True)

        return df_responses

    def geocode(self):
        fields_list = [fd for fd in self.schema_address[cf.AD_FIELD] if fd in self.input_df.columns]

        if len(fields_list) > 0:
            for field in fields_list:
                address_df = self.input_df[[cf.SHERLOCK_ID, field]].dropna().reset_index(drop=True)
                queries = self.make_queries(address_df,field)
                if len(address_df) > 0:
                    address_df[st.QUERY] = queries
                    address_df[st.QUERY_RES] = run_queries(queries)
                    self.list_df_response.append(self.responses_to_df(address_df, field))
                else:
                    #print(st.NO_VALID_ADDRESS.format(field))
                    pass

        else:
            #print(st.NO_ADRESS)
            pass

        if len(self.list_df_response) > 0:
            self.df_response = pd.concat(self.list_df_response)

        return self.df_response
