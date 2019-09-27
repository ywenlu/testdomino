const FILE_SIZE_BASE = 1024;
const FILE_SIZE_UNIT = ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"];
const FILE_TYPES =
{
    undefined: { name: "{0}", icon: "file", color: "grey-dark", options: [ "form-option-icon" ], default: true },
    "csv": { name: "CSV data file", icon: "file-csv", color: "green-dark", options: [ "form-option-icon", "form-option-headers", "form-option-csv-separator" ] }
};
const FILE_SEPARATORS =
[
    { name: "Comma (,)", char: "," },
    { name: "Semicolon (;)", char: ";" },
    { name: "Tabulation (\\t)", char: "\t" },
    { name: "Space ( )", char: " " }
];
const FILE_COLUMN_TYPES =
[
    "Text",
    "Number",
    "Boolean",
    "Date",
    "Datetime"
];
const FILE_COLUMN_TYPES_CODE =
[
    "string",
    "number",
    "boolean",
    "date",
    "datetime"
];
const RULES =
[
    "Name",
    "Type",
    "Is ID",
    "Is required",
    "Min.",
    "Max.",
    "Rel. min.",
    "Rel. max.",
    "Allowed ref.",
    "Dependencies",
    "Required if null",
    "RegEx"
];
const TABLE_VIEW_MAX_ROWS = 17;
const TABLE_RULES_MAX_ROWS = 14;
const TABLE_RESULT_MAX_ROWS = 17;

class ArticleSherlock extends Article
{
    constructor(selector, store)
    {
        super(selector, store);

        this.set_component_icon();
        this.set_component_select();
        this.set_component_options();
        this.set_component_table();
        this.set_result_table();
        this.set_component_pagination();
        this.set_component_popup();
        this.set_component_analysis();
        this.set_component_tabs();
    }
    
    set_component_icon()
    {
        this.icon = this.self.find(".form-icon");
    }

    set_component_select()
    {
        this.select = this.self.find("select#form-select-file");
        this.select.on("change", () =>
        {
            this.file = this.store.get_file(this.select.prop("value"));
            this.type = (this.file !== undefined && FILE_TYPES[this.file.type] !== undefined) ? FILE_TYPES[this.file.type] : FILE_TYPES[undefined];
            
            if(this.file !== undefined && this.type !== undefined && this.type.options !== undefined)
            {
                this.options.find(".form-option").addClass("hidden");
                for(var option of this.type.options)
                {
                    this.options.find("#{0}".format(option)).removeClass("hidden");
                }

                if(this.file.has_headers)
                {
                    this.option_headers.addClass("active");
                }
                else
                {
                    this.option_headers.removeClass("active");
                }

                this.option_separator.prop("value", (this.file.separator !== undefined) ? FILE_SEPARATORS.indexOf(this.file.separator) : 0);

                if(this.file !== undefined)
                {
                    var icon = this.options.find(".form-icon");
                    icon.parent().css("flex", 1);
                    icon.empty()
                    .append($("<i></i>").addClass("fas fa-{0}".format(this.type.icon)).css("color", "var(--{0})".format(this.type.color)))
                    .append($("<span></span>").addClass("form-icon-label").text(this.type.default ? this.type.name.format(this.file.type) : this.type.name));
                }
                
                this.page_view = 0;
                this.page_rules = 0;
                this.page_result = 0;
                this.refresh_tabs();
                this.refresh_table(true);              
            }
        });
    }

    set_component_options()
    {
        this.options = this.self.find(".form-options");
        this.options.children(".form-option").addClass("hidden");

        this.option_headers = this.options.find("#form-option-headers .form-checkbox");
        $(document).on("click", "#form-option-headers .form-checkbox", () =>
        {
            this.refresh_table(true);
        });

        this.option_separator = this.options.find("#form-option-csv-separator select");
        this.option_separator.empty();
        for(var key in FILE_SEPARATORS)
        {
            this.option_separator.append($("<option></option>").attr("value", key).text(FILE_SEPARATORS[key].name))
        }
        this.option_separator.on("change", () =>
        {
            this.refresh_table(true);
        });
    }

    set_component_table()
    {
        this.table_view = this.self.find(".form-table table.table#view-table");

        this.table_view_head = $("<thead></thead>").appendTo(this.table_view);
        this.table_view_head.append($("<tr></tr>"));
        this.table_view_body = $("<tbody></tbody>").appendTo(this.table_view);
        if(this.table_view_body.children().length < TABLE_VIEW_MAX_ROWS - 1)
        {
            for(var i = this.table_view_body.children().length - 1; i < TABLE_VIEW_MAX_ROWS - 1; ++i)
            {
                this.table_view_body.append($("<tr></tr>"));
            }
        }

        this.table_rules = this.self.find(".form-table table.table#rules-table");
        
        this.table_rules_head = $("<thead></thead>").appendTo(this.table_rules);
        this.table_rules_head.append($("<tr></tr>"));
        this.table_rules_body = $("<tbody></tbody>").appendTo(this.table_rules);
        if(this.table_rules_body.children().length < TABLE_RULES_MAX_ROWS - 1)
        {
            for(var i = this.table_rules_body.children().length - 1; i < TABLE_RULES_MAX_ROWS - 1; ++i)
            {
                this.table_rules_body.append($("<tr></tr>"));
            }
        }
    }

    set_result_table()
    {
        this.table_result= this.self.find(".form-table table.table#result-table");

        this.table_result_head = $("<thead></thead>").appendTo(this.table_result);
        this.table_result_head.append($("<tr></tr>"));
        this.table_result_body = $("<tbody></tbody>").appendTo(this.table_result);
        if(this.table_result_body.children().length < TABLE_RESULT_MAX_ROWS - 1)
        {
            for(var i = this.table_result_body.children().length - 1; i < TABLE_RESULT_MAX_ROWS - 1; ++i)
            {
                this.table_result_body.append($("<tr></tr>"));
            }
        }
        
    }

    set_component_pagination()
    {
        this.page_view = 0;
        this.pagination_view = new Pagination(this.self.find("ul.pagination#view-pagination"), 1, value =>
        {
            this.page_view = value - 1;
            this.refresh_table(false);
        });
        this.pagination_view.display();

        this.page_rules = 0;
        this.pagination_rules = new Pagination(this.self.find("ul.pagination#rules-pagination"), 1, value =>
        {
            this.page_rules = value - 1;
            this.refresh_table(false);
        });
        this.pagination_rules.display();

        this.page_result = 0;
        this.pagination_result = new Pagination(this.self.find("ul.pagination#result-pagination"), 1, value =>
        {
            this.page_result = value - 1;
            this.refresh_table(false);
        });
        this.pagination_result.display();
    }

    set_component_popup()
    {
        this.popup.find(".btn-validate").on("click", () =>
        {
            var rule = this.popup.attr("data-rule");
            var key = parseInt(this.popup.attr("data-key"));
            if(!isNaN(key))
            {
                this.file.rules[rule][key] = this.popup_textarea.prop("value").trim();

                var selected = this.table_rules.find("tr td .btn.btn-popup[data-key={0}]".format(key));
                if(this.file.rules[rule][key] !== "")
                {
                    selected.addClass("btn-primary");
                    selected.removeClass("btn-secondary");
                }
                else
                {
                    selected.removeClass("btn-primary");
                    selected.addClass("btn-secondary");
                }
            }

            this.fade_popup_out();
        });
        this.popup_textarea = this.popup.find(".article-popup-info textarea.form-textarea");
    }

    set_component_analysis()
    {
        this.button_analyse = this.self.find(".article-header .article-action button.btn").on("click", () =>
        {
            if(!this.button_analyse.hasClass("disabled"))
            {
                this.button_analyse.addClass("disabled");

                var message_input = this.message_input();
                var message_rules = this.message_rules();
                this.tab_result = $("ul.nav-tabs li.nav-item span.nav-link[data-tab=result]").trigger("click");

                this.store.queryScript("main", [message_input, message_rules], response =>
                {
                    console.log(response);
                    this.result = true;
                    this.refresh_table(true, response);

                    this.button_analyse.removeClass("disabled");
                });
            }
        });
    }
    
    set_component_tabs()
    {
        this.tabs = this.self.find(".nav.nav-tabs");
        this.tabs.fadeTo(0, 0);
        this.table_view.parent().fadeTo(0, 0);
    }

    read_file()
    {
        var has_headers = this.option_headers.hasClass("active");
        var separator = FILE_SEPARATORS[parseInt(this.option_separator.prop("value"))];
        if(separator !== undefined && this.file !== undefined)
        {
            this.file.has_headers = has_headers;
            this.file.separator = separator;
            
            var reader = new CSVReader(this.file.data);
            reader.read(this.file.has_headers, this.file.separator.char);

            this.file.headers = reader.headers;
            this.file.content = reader.content;
            if(this.file.headers.length == 0 && this.file.content.length > 0)
            {
                for(var i = 0; i < reader.length; ++i)
                {
                    this.file.headers.push("Column {0}".format(i + 1))
                }
            }
        }
    }

    message_input()
    {
        var message = {};
        for(var key_row in this.file.content)
        {
            key_row = parseInt(key_row);
            for(var key_header in this.file.content[key_row])
            {
                key_header = parseInt(key_header);
                if(key_header < this.file.headers.length)
                {
                    var column = this.file.headers[key_header].replace(/^"+|"+$/g, "");
                    if(message[column] === undefined)
                    {
                        message[column] = [];
                    }

                    message[column].push(this.file.content[key_row][key_header]);
                }
            }
        }

        return message;
    }

    message_rules()
    {
        var message =
        {
            "RULES":
            {
                "ORDER": [],
                "NAME": [],
                "REQUIRED": [],
                "TYPE": [],
                "MIN": [],
                "RELATIVE_MIN": [],
                "MAX": [],
                "RELATIVE_MAX": [],
                "ALLOWED_REF": [],
                "DEPENDENCIES": [],
                "REQUIRED_IF_NULL": [],
                "REGEX": [],
            },
            "REF": { "GROUP": [], "VALUE": [] },
            "ID": {},
            "ADDRESS": { "Adress_Fields": [] }
        };
        
        var ids = [];
        for(var key in this.file.headers)
        {
            var name = this.file.headers[key];
            var type = (this.file.rules["type"][key] !== undefined) ? parseInt(this.file.rules["type"][key]) : 0;
            type = FILE_COLUMN_TYPES_CODE[type];
            var required = (this.file.rules["required"][key] !== undefined) ? this.file.rules["required"][key] : false;
            var min_relative = (this.file.rules["min_relative"][key] !== undefined && this.file.rules["min_relative"][key] > 0) ? "{0}".format(this.file.rules["min_relative"][key]) : "";
            var max_relative = (this.file.rules["max_relative"][key] !== undefined && this.file.rules["max_relative"][key] > 0) ? "{0}".format(this.file.rules["max_relative"][key]) : "";
            var key_reference = "";
            var references = (this.file.rules["allowed_references"][key] !== undefined) ? this.file.rules["allowed_references"][key].split("\n") : [];
            for(var reference of references)
            {
                if(reference.trim() !== "")
                {
                    key_reference = "REF{0}".format(key);
                    
                    message["REF"]["GROUP"].push(key_reference);
                    message["REF"]["VALUE"].push(reference);
                }
            }

            var dependencies = (this.file.rules["dependencies"][key] !== undefined && this.file.rules["dependencies"][key] > 0) ? "{0}".format(this.file.rules["dependencies"][key]) : "";
            var required_if_null = (this.file.rules["required_if_null"][key] !== undefined && this.file.rules["required_if_null"][key] > 0) ? "{0}".format(this.file.rules["required_if_null"][key]) : "";

            if(this.file.rules["id"][key])
            {
                ids.push(name);
            }

            message["RULES"]["ORDER"].push("{0}".format(parseInt(key) + 1));
            message["RULES"]["NAME"].push(name);
            message["RULES"]["REQUIRED"].push(required);
            message["RULES"]["TYPE"].push(type);
            message["RULES"]["MIN"].push((this.file.rules["min"][key] !== undefined) ? this.file.rules["min"][key] : "");
            message["RULES"]["MAX"].push((this.file.rules["max"][key] !== undefined) ? this.file.rules["max"][key] : "");
            message["RULES"]["RELATIVE_MIN"].push(min_relative);
            message["RULES"]["RELATIVE_MAX"].push(max_relative);
            message["RULES"]["ALLOWED_REF"].push(key_reference);
            message["RULES"]["DEPENDENCIES"].push(dependencies);
            message["RULES"]["REQUIRED_IF_NULL"].push(required_if_null);
            message["RULES"]["REGEX"].push((this.file.rules["regex"][key] !== undefined) ? this.file.rules["regex"][key] : "");
        }

        for(var key_id in ids)
        {
            message["ID"]["ID{0}".format(parseInt(key_id) + 1)] = [ids[key_id]];
        }

        return message;
    }

    sort_type(x)
    {
        var counts = {};
        var sort = 0;
        for (var i of x)
        {
            if(i !== undefined)
            {
                var gtype = 0;
                if(!isNaN(parseFloat(i)))
                {
                    gtype = 1;
                }
                else if(moment(new Date(i))._isValid)
                {
                    gtype = 3;
                }
                else if(i == "true" || i == "false")
                {
                    gtype = 2;
                }
                else
                {
                    gtype = 0;
                }

                counts[gtype] = 1 + (counts[gtype] || 0);
            }
        }

        for(var key in counts)
        {
            var value = counts[key];
            sort = value > sort ? key : sort;
        }
        
        return sort;
    }

    guess_type()
    {
        var row_num = this.file.content.length;
        var col_num = this.file.headers.length;
        var randRow;
        var temp_type;
        var final_type = [];

        for(let j = 0; j < col_num; j++)
        {
            temp_type = [];
            for (let i = 0; i < Math.sqrt(row_num); i++)
            {
                randRow = Math.floor(Math.random() * row_num);
                temp_type.push(this.file.content[randRow][j])
            }
            final_type.push(this.sort_type(temp_type));
        }
        
        return final_type;
    }
    
    display_select_files()
    {
        var keys = [];
        var values = [];
        for(var key in this.store.get_file_all())
        {
            var size = this.store.files[key].size;
            var size_approximated = size;
            var size_unit = 0;
            while(size_approximated >= FILE_SIZE_BASE)
            {
                size_approximated /= FILE_SIZE_BASE;
                size_unit++;
            }
            
            keys.push(key);
            values.push("{0} ({1} {2})".format(key, size_approximated.toFixed(2), FILE_SIZE_UNIT[size_unit]));
        }

        this.display_select(this.select, keys, values);
    }

    display_table_view(start, has_headers_changed)
    {
        return this.display_table(this.table_view, this.pagination_view, this.file.headers, this.file.content, start, TABLE_VIEW_MAX_ROWS, has_headers_changed,
        (row, key, element) =>
        {
            for(var cell of element)
            {
                row.append($("<td></td>").attr("data-key", key).text(cell));
            }
        });
    }

    display_table_rules(start, has_headers_changed)
    {
        this.types = this.guess_type();
        return this.display_table(this.table_rules, this.pagination_rules, RULES, this.file.headers, start, TABLE_RULES_MAX_ROWS, has_headers_changed,
        (row, key, element) =>
        {
            var columns = ["Aucune", ...this.file.headers];

            row.append($("<td></td>").text(element))
            .append(this.display_type_select(key, this.file.rules["type"], this.types, Object.keys(FILE_COLUMN_TYPES), Object.values(FILE_COLUMN_TYPES)))
            .append(this.display_rule_checkbox(key, this.file.rules["id"]).css("width", "60px"))
            .append(this.display_rule_checkbox(key, this.file.rules["required"]).css("width", "60px"))
            .append(this.display_rule_number(key, this.file.rules["min"]).css("width", "60px"))
            .append(this.display_rule_number(key, this.file.rules["max"]).css("width", "60px"))
            .append(this.display_rule_select(key, this.file.rules["min_relative"], Object.keys(columns), Object.values(columns)).css("width", "100px"))
            .append(this.display_rule_select(key, this.file.rules["max_relative"], Object.keys(columns), Object.values(columns)).css("width", "100px"))
            .append(this.display_rule_reference(key, this.file.rules["allowed_references"]))
            .append(this.display_rule_select(key, this.file.rules["dependencies"], Object.keys(columns), Object.values(columns)))
            .append(this.display_rule_select(key, this.file.rules["required_if_null"], Object.keys(columns), Object.values(columns)))
            .append(this.display_rule_text(key, this.file.rules["regex"]));
        });
    }

    display_table_result(start, has_headers_changed, response)
    {
        var ids = [];
        var fields = [];
        var counts = {};
        var errors = {};
        var error = [];
        var found = [];
        var tds = []
        var error_count = 0;
        var x = 0;
        var min_color = [215,238,200];
        var max_color = [59,128,13];
        
        if(response !== undefined && response.diagnostic === "Exported" && response.report !== undefined)
        {
            ids = response.report[0].SHERLOCK_ID;
            fields = response.report[0].FIELD;
            error = response.report[0].ERROR;
            var field = 0;
            for (var id of ids)
            {
                if(counts[id]){
                    counts[id].push(fields[field]);
                    errors[id].push(error[field]);
                }
                else{
                    counts[id] = [fields[field]];
                    errors[id] = [error[field]];
                }
                field ++;
            }
        }

        this.result_header = ["Audit"].concat(this.file.headers);

        return this.display_table(this.table_result, this.pagination_result, this.result_header, ids, start, TABLE_RESULT_MAX_ROWS, has_headers_changed,
        (row, key, element) =>
        {
            if (!found.includes(element))
            {
                x = 0;
                error_count = 0;
                tds = [];
                for (var cell of this.file.content[element])
                {
                    if(counts[element].includes(this.file.headers[x]))
                    {
                        var error_message = errors[element][error_count];
                        console.log(errors)
                        var td = $('<td></td>')
                        .attr("data-key", key)
                        .attr("data-toggle", "popover")
                        .attr("title", "Error")
                        .attr("data-content", error_message)
                        .attr("data-placement", "right");

                        td.popover({ trigger: "hover" })

                        td.append($('<div>').addClass("error").attr('border-radius', '50%').text(cell));
                        tds.push(td);

                        error_count ++;
                        
                    }else
                    {
                        tds.push($('<td></td>').attr("data-key", key).text(cell));
                    }
                    x ++;
                }

                var error_nbr = 100 - Math.round(error_count / this.file.headers.length * 100);
                var error_percent = error_nbr + "%";
                var t = Math.ease_in(error_nbr / 100);
                var r = Math.round(Math.lerp(min_color[0], max_color[0], t));
                var g = Math.round(Math.lerp(min_color[1], max_color[1], t));
                var b = Math.round(Math.lerp(min_color[2], max_color[2], t));

                var td_error = $('<td></td>').attr("data-key", key)
                .css("background-color", "rgb({0}, {1}, {2})".format(r,g,b))
                .css("color", "white")
                .css("font-weight", "bold")
                .css("text-align", "center").text(error_percent);
                
                row.append(td_error);
                tds.forEach(x =>
                {
                    row.append(x);
                });

                found.push(element) 
            }
        });
    }

    display_rule_text(key, data)
    {
        var input = $("<input/>")
        .attr("type", "text")
        .prop("value", (key < data.length) ? data[key] : "")
        .addClass("form-control form-control-compact")
        .on("change", () =>
        {
            data[key] = input.prop("value");
        });

        return $("<td></td>").addClass("td-center").append(input);
    }

    display_rule_number(key, data)
    {
        //METTRE SUR 0
        var input = $("<input/>")
        .attr("type", "text")
        .prop("value", (key < data.length) ? data[key] : undefined)
        .addClass("form-control form-control-compact")
        .on("change", () =>
        {
            var parsed = parseFloat(input.prop("value"));
            data[key] = !isNaN(parsed) ? parsed : undefined;
            input.prop("value", (data[key] !== undefined) ? data[key] : "");
        });

        return $("<td></td>").addClass("td-center").append(input);
    }

    display_rule_select(key, data, keys, values)
    {
        var select = this.display_select($("<select></select>"), keys, values)
        .attr("data-key", key)
        .prop("value", (key < data.length) ? data[key] : 0)
        .addClass("form-select form-control form-control-compact")
        .on("change", function()
        {
            data[key] = parseInt($(this).prop("value"));
        })
        .trigger("change");

        return $("<td></td>").addClass("td-center").append(select);
    }

    display_type_select(key, data, types, keys, values)
    {
        var select = this.display_select($("<select></select>"), keys, values)
        .attr("data-key", key)
        .prop("value", (key < types.length) ? types[key] : 0)
        .addClass("form-select form-control form-control-compact")
        .on("change", function()
        {
            data[key] = parseInt($(this).prop("value"));
        })
        .trigger("change");

        return $("<td></td>").addClass("td-center").append(select);
    }

    display_rule_checkbox(key, data)
    {
        var checkbox = $("<div></div>");
        checkbox.addClass("form-checkbox " + ((key < data.length && data[key]) ? "active" : ""));
        checkbox.on("click", () =>
        {
            data[key] = !data[key];
        });

        return $("<td></td>").addClass("td-center").append(checkbox);
    }

    display_rule_reference(key, data)
    {
        var button = $("<button></button>")
        .attr("data-key", key)
        .addClass("btn btn-compact btn-popup " + ((key < data.length && data[key] !== undefined && data[key].trim() !== "") ? "btn-primary" : "btn-secondary"))
        .on("click", () =>
        {
            this.popup.attr("data-rule", "allowed_references");
            this.popup.attr("data-key", key);
            this.popup_textarea.prop("value", (key < data.length && data[key] !== undefined && data[key].trim() !== "") ? data[key] : "");
            this.fade_popup_in();
        })
        .append($("<i></i>").addClass("fas fa-edit"));

        return $("<td></td>").addClass("td-center").append(button);
    }

    refresh()
    {
        return this.update(() =>
        {
            this.display_select_files();
            this.select.trigger("change");
        });
    }

    refresh_tabs()
    {
        if(this.file !== undefined)
        {
            this.tabs.fadeTo(FADE_TIME_DEFAULT, 1);
            this.table_view.parent().fadeTo(FADE_TIME_DEFAULT, 1);
        }
    }

    refresh_table(has_headers_changed, response=null)
    {
        return this.update(() =>
        {
            this.read_file();
            if(this.file !== undefined)
            {
                this.display_table_view(this.page_view, has_headers_changed);
                this.display_table_rules(this.page_rules, has_headers_changed);
                if(this.result)
                {
                    this.display_table_result(this.page_result, has_headers_changed, response);
                }
            }
        });
    }
}