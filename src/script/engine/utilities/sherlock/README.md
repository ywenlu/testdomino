### Installation

python setup.py install

### Example

Check the examples folder for more detail.
    
    import sherlock
    
    input_schema = "./schema/schema.xlsx"
    input_data = "./input/input.xlsX"
    
    validation_report = sherlock.validate(input_data, "CONTRACT", input_schema)
    validation_report.to_excel("./out.xlsx")
