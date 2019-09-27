import datetime as dt

# INPUT SCHEMA RULES
ORDER = "ORDER"
RULES = "RULES"
NAME = "NAME"
REQUIRED = "REQUIRED"
TYPE = "TYPE"
MIN = "MIN"
MAX = "MAX"
ALLOWED_REF = "ALLOWED_REF"
DEPENDENCIES = "DEPENDENCIES"
RELATIVE_MIN = "RELATIVE_MIN"
RELATIVE_MAX = "RELATIVE_MAX"
REQUIRED_IF_NULL = "REQUIRED_IF_NULL"
REGEX = "REGEX"

#ALL SCHEMA SHEETS
ID = "ID"
ADDRESS = "ADDRESS"
AD_FIELD = "Adress_Fields"

# INPUT SCHEMA REF
REF = "REF"
GROUP = "GROUP"
VALUE = "VALUE"

# INPUT SCHEMA MATCHING
MATCHING = "MATCHING"
SOURCE1 = "SOURCE1"
SHEETNAME_SOURCE1 = "SHEETNAME_SOURCE1"
FIELD_SOURCE1= "FIELD_SOURCE1"
SOURCE2= "SOURCE2"
SHEETNAME_SOURCE2= "SHEETNAME_SOURCE2"
FIELD_SOURCE2= "FIELD_SOURCE2"


input_schema_type = {
    NAME: str,
    REQUIRED: bool,
    TYPE: str,
    DEPENDENCIES: str
}

matching_schema_type = {
    SOURCE1: str,
    SHEETNAME_SOURCE1: str,
    FIELD_SOURCE1: str,
    SOURCE2: str,
    SHEETNAME_SOURCE2: str,
    FIELD_SOURCE2: str,
}

mapping_cerberus_python_types = {
    'number': float,
    'string': str,
    'boolean': bool,
    'date': dt.date,
    'datetime': dt.datetime
}

err_msg_relativemin = "must be greater than '%s'"
err_msg_relativemax = "must be smaller than '%s'"
err_msg_requiredif = "required value if field '%s' not filled"
err_msg_matching = "the number of fields specified for the matching between '%s' and '%s' is different. Refer to line '%s' of the matching schema"
err_msg_strmatching= "One or multiple fields specified in '%s' are not strings"

""" err_msg_relativemin = {code: 0, generic: "Must be greater than relative min", details: "Must be greater than '%s'"}
err_msg_relativemax = {code: 1, generic: "Must be smaller than relative max", details: "Must be smaller than '%s'"}
err_msg_requiredif = {code: 2, generic: "Required value", details: "Required value if field '%s' not filled"}
err_msg_matching = {code: 3, generic: "Matching difference", details: "The number of fields specified for the matching between '%s' and '%s' is different. Refer to line '%s' of the matching schema"}
err_msg_strmatching= {code: 4, generic: "Not strings", details: "One or multiple fields specified in '%s' are not strings"}
 """
# VALIDATION REPORT
SHERLOCK_ID = "SHERLOCK_ID"
FIELD = "FIELD"
ERROR = "ERROR"
VALIDATION_REPORT_COLUMNS = [SHERLOCK_ID, FIELD, ERROR]
