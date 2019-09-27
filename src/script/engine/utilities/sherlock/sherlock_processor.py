import pandas as pd
from engine.config import config as cf
from engine.utilities.sherlock.sherlock_validator import SherlockValidator


def read_excel(input_path, sheetname, schema):
    dftype = _extract_type_from_schema(schema)
    df = pd.read_excel(input_path, sheet_name=sheetname, dtype=dftype)
    return df


def read_csv(input_path, schema, sep=",", encoding="utf8"):
    dftype = _extract_type_from_schema(schema)
    df = pd.read_csv(input_path, df_type=dftype, sep=sep, encoding=encoding)
    return df


def load_schemas(schema_path):
    df = pd.read_excel(schema_path, df_type=cf.input_schema_type, sheet_name=cf.RULES)
    df.fillna("", inplace=True)

    df_ref = pd.read_excel(schema_path, df_type=cf.input_schema_type, sheet_name=cf.REF)
    df_ref.fillna("", inplace=True)

    df_dict = df.to_dict(orient="records")
    schema = {}
    schema_required_if = {}
    for f in df_dict:
        schema.update(_dict_to_schema(f, df_ref))
        schema_required_if.update(_dict_to_schema_required_if(f, df))

    return schema, schema_required_if


def process_input(df):
    df.reset_index(inplace=True)
    df.rename(columns={"index": cf.SHERLOCK_ID}, inplace=True)
    return df


def _dict_to_schema_required_if(rule, df_schema):
    # init schema dict
    schema = {}

    requiredif_ids = [int(i) for i in rule[cf.REQUIRED_IF_NULL].split(',') if i != ""]
    requiredif_fields = df_schema[df_schema[cf.ORDER].isin(requiredif_ids)][cf.NAME].tolist()
    if len(requiredif_fields) > 0:
        schema[rule[cf.NAME]] = {}
        schema[rule[cf.NAME]]['requiredif'] = requiredif_fields
    return schema


def _dict_to_schema(rule, ref):
    # init schema dict
    schema = {rule[cf.NAME]: {}}

    # init processed rules
    dependencies = [i for i in rule[cf.DEPENDENCIES].split(',')]
    allowed_values = ref[ref[cf.GROUP] == rule[cf.ALLOWED_REF]][cf.VALUE].tolist()

    schema[rule[cf.NAME]]['type'] = rule[cf.TYPE]
    schema[rule[cf.NAME]]['required'] = rule[cf.REQUIRED]

    if rule[cf.RELATIVE_MIN] != "":
        schema[rule[cf.NAME]]['relativemin'] = rule[cf.RELATIVE_MIN]
    if rule[cf.RELATIVE_MAX] != "":
        schema[rule[cf.NAME]]['relativemax'] = rule[cf.RELATIVE_MAX]
    if rule[cf.MIN] != "":
        schema[rule[cf.NAME]]['min'] = rule[cf.MIN]
    if rule[cf.MAX] != "":
        schema[rule[cf.NAME]]['max'] = rule[cf.MAX]
    if rule[cf.REGEX] != "":
        schema[rule[cf.NAME]]['regex'] = rule[cf.REGEX]
    if rule[cf.DEPENDENCIES] != "":
        schema[rule[cf.NAME]]['dependencies'] = dependencies
    if len(allowed_values) > 0:
        schema[rule[cf.NAME]]['allowed'] = allowed_values
    return schema


def _extract_type_from_schema(schema):
    dftype = {}
    for i in schema:
        type_name = schema[i]['type']
        rtype = cf.mapping_cerberus_python_types[type_name]
        dftype[i] = rtype
    return dftype


def _replace_dict_nan_none(dico):
    for doc in dico:
        for el in doc:
                if (str(doc[el]) == "nan") | (str(doc[el]) == "NaT"):
                    doc[el] = None
    return dico


def validate_df(df, schema, schema_requiredif=None, allow_unknown=False):
    v_report = []
    df_dict = df.to_dict(orient="records")
    _replace_dict_nan_none(df_dict)
    v = SherlockValidator(schema)
    v.allow_unknown = allow_unknown

    for i, r in enumerate(df_dict):
        errors = {}
        r = {k: v for (k, v) in r.items() if v}
        val_res = v.validate(r)
        if not val_res:
            errors = v.errors
        if schema_requiredif:
            required_if_errors = _validate_required_if(r, schema_requiredif)
            errors.update(required_if_errors)

        if errors != {}:
            v_report.append([i, errors])
    return v_report


def _format_validation_report(v_report):
    final_report = []
    if len(v_report) > 0:
        for id in v_report:
            for key, value in iter(id[1].items()):
                final_report.append([id[0], key, ", ".join(value)])
    df_validation_report = pd.DataFrame(final_report, columns=cf.VALIDATION_REPORT_COLUMNS)
    return df_validation_report


def make_report(v_report, input_df, detailed_report):
    df_validation_report = _format_validation_report(v_report)
    if detailed_report:
        df_validation_report = pd.merge(df_validation_report, input_df, how="left", left_on=cf.SHERLOCK_ID,
                                        right_on=cf.SHERLOCK_ID)
    return df_validation_report


def _validate_required_if(document, schema):
    v_report = {}
    full_none = True
    for field in schema:
        required_fields = schema[field]["requiredif"]
        for j in document:
            if j in required_fields:
                full_none = False
        if full_none & (field not in document):
            v_report[field] = [cf.err_msg_requiredif % ",".join(required_fields)]
    return v_report


def validate(input,sheetname, schema, allow_unknown=True, detailed_report=True):
    # type: (str, str, str, bool, bool) -> object

    """
    Main function to validate doc

    :param input: Filepath of the input data excel file
    :param schema: Filepath of the schema excel file
    :param allow_unknown: Determine if unknown fields accepted (default True)
    :param detailed_report: Determine whether to add input full data in the error report
    :return: Dataframe with error report summary
    """

    schema, schema_required_if,  = load_schemas(schema)

    input_df = read_excel(input, schema, sheet_name=sheetname)
    input_df = process_input(input_df)

    v_report = validate_df(input_df, schema, schema_required_if, allow_unknown)
    v_report = make_report(v_report, input_df, detailed_report)


    return v_report