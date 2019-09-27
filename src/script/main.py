import sys
import os
import json
import pandas as pd

from engine.diag import Diagnosis

SCHEMA_DIR = os.getcwd() + "/src/script/demo/schema/"
OUT_DIR = os.getcwd() + "/src/script/demo/output/"

ARGS_DIR = os.getcwd() + "/src/data/"

result = { "diagnostic": None, "report": [], "cross_report": [] }

for file in os.listdir(ARGS_DIR):
    if file.endswith("0.json"):
        input_dict = json.loads(open(ARGS_DIR + file).read())
    if file.endswith("1.json"):
        schema_dict = json.loads(open(ARGS_DIR + file).read())

""" input_dict = json.loads(sys.argv[1])
schema_dict = json.loads(sys.argv[2]) """

dg = Diagnosis(input_dict, schema_dict, SCHEMA_DIR, OUT_DIR, result)

try:
    dg.launch_diag()
except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)
    print(e)

print(json.dumps(result))

sys.stdout.flush()
