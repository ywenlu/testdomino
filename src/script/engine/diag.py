import contextlib
import json
from pandas import ExcelWriter
from engine.config import stringref as st
from engine.utilities.loader import *
from engine.utilities.sherlock import sherlock_processor

from engine.pipes.diag.a_duplicate_detector import duplicates
from engine.pipes.diag.b_geocoder import Geocoder
from engine.pipes.diag.c_string_matching import  str_matching
from engine.pipes.diag.d_row_matching import  row_matching

class Diagnosis:

    def __init__(self, input_dict, schema_dict, schema_dir, out_dir, result, cross_validation=False):
        self.input_dict = input_dict
        self.schema_dict = schema_dict
        self.schema_dir = schema_dir
        self.out_dir = out_dir
        self.result = result
        self.cross = cross_validation
        self.report_list = []


    def validate(self, input_df, schemas):
        #print(st.rule_based_msg)
        sherlock_report = sherlock_processor.validate_df(input_df, schemas['sherlock'], schemas['required_if'],
                                                         allow_unknown=True)
        sherlock_report = sherlock_processor.make_report(sherlock_report, input_df, detailed_report=True)
        #print(st.duplicates_msg)
        duplicates_report = duplicates(input_df, schemas['duplicates'])

        #print(st.address_msg)
        gc = Geocoder(input_df, schemas['address'])
        with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
            address_report = gc.geocode()

        reports = {
            'sherlock': sherlock_report,
            'duplicates': duplicates_report,
            'address': address_report
        }
        
        self.result["report"].append(json.loads(json.dumps(sherlock_report.to_dict('list'),  indent=4, sort_keys=True, default=str)))
        self.result["report"].append(json.loads(json.dumps(duplicates_report.to_dict('list'),  indent=4, sort_keys=True, default=str)))
        self.result["report"].append(json.loads(json.dumps(address_report.to_dict('list'),  indent=4, sort_keys=True, default=str)))

        return reports


    def cross_validate(self,files_mapping_dict, fields_mapping, str_matching_schema, row_matching_schema,input_dict):

        str_matching_report = str_matching(self,input_dict, files_mapping_dict, fields_mapping, str_matching_schema)
        row_matching_report= row_matching(self,input_dict, files_mapping_dict, fields_mapping, row_matching_schema)

        reports = {
            'str_matching': str_matching_report,
            'row_matching': row_matching_report,
        }

        self.result["cross_report"].append(reports)

        return reports


    def export_report(self, reports, file_name):

        with  ExcelWriter("{}/report_{}.xlsx".format(self.out_dir,os.path.splitext(file_name)[0])) as writer:
            reports['sherlock'].to_excel(writer, sheet_name='RE1_rules')
            reports['duplicates'].to_excel(writer, sheet_name='RE2_duplicates')
            reports['address'].to_excel(writer, sheet_name='RE3_address')

        self.result["diagnostic"] = "Exported"
        return 0

    def export_cross_report(self, reports):

        with  ExcelWriter("demo/output/cross_report.xlsx") as writer:
            reports['str_matching'].to_excel(writer, sheet_name='CRE1_str_matching')
            reports['row_matching'].to_excel(writer, sheet_name='CRE2_row_matching')
        
        return 0

    def launch_diag(self):

        #print(st.simple_msg)
        input_dict = load_input(self.input_dict, self.schema_dict, self.schema_dir)

        for file_name, dfs in input_dict.items():
            #print("--------- {} ---------".format(file_name))
            reports = self.validate(dfs['input'], dfs['schemas'])
            self.export_report(reports, file_name)

        if self.cross:
            #print(st.cross_msg)
            files_mapping_dict, fields_mapping, str_matching_schema, row_matching_schema = load_cross_schema(self.schema_dir)
            cross_reports = self.cross_validate(files_mapping_dict, fields_mapping, str_matching_schema, row_matching_schema,input_dict)
            self.export_cross_report(cross_reports)
