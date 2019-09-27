const FADE_TIME_ZERO = 0;
const FADE_TIME_DEFAULT = 200;

class Article
{
    constructor(selector, store)
    {
        this.selector = selector;
        this.self = $(this.selector);
        this.body = $(this.selector + " .article-body");
        this.popup = $(this.selector + " .article-popup");
        this.popup.find(".article-popup-container .article-header .article-close").on("click", () => { this.fade_popup_out() });

        this.store = store;
        this.listeners = {};
    }

    on(event, callback)
    {
        if(callback !== undefined && typeof callback === "function")
        {
            if(this.listeners[event] === undefined)
            {
                this.listeners[event] = [];
            }

            this.listeners[event].push(callback);
        }
    }

    trigger(event)
    {
        var promises = [];
        if(this.listeners[event] !== undefined)
        {
            for(var listener of this.listeners[event])
            {
                promises.push(new Promise((resolve, reject) =>
                {
                    try
                    {
                        resolve(listener());
                    }
                    catch(error)
                    {
                        reject(error);
                    }
                }));
            }
        }

        return Promise.all(promises);
    }

    fade_in()
    {
        return this.self.fadeTo(FADE_TIME_DEFAULT, 1).promise();
    }

    fade_out()
    {
        return this.self.fadeTo(FADE_TIME_DEFAULT, 0).promise();
    }

    fade_body_in()
    {
        return this.body.fadeTo(FADE_TIME_DEFAULT, 1).promise();
    }

    fade_body_out()
    {
        return this.body.fadeTo(FADE_TIME_DEFAULT, 0).promise();
    }

    fade_popup_in()
    {
        return this.popup.css("display", "flex").fadeTo(FADE_TIME_DEFAULT, 1).promise();
    }

    fade_popup_out()
    {
        return this.popup.fadeTo(FADE_TIME_DEFAULT, 0).promise().then(() =>
        {
            this.popup.css("display", "none");
        });
    }

    display_select(select, keys, values, condition)
    {
        condition = (condition !== undefined && typeof condition === "function") ? condition : () => true;
    
        select.empty();
        select.removeAttr("disabled");

        for(var i = 0; i < keys.length; ++i)
        {
            var element = (i < values.length) ? values[i] : "";
            if(condition(keys[i], element))
            {
                select.append($("<option></option>").attr("value", keys[i]).text(element));
            }
        }

        if(keys.length === 0)
        {
            select.attr("disabled", "disabled");
        }

        return select;
    }
    
    display_table(table, pagination, headers, content, page, page_max, has_headers_changed, callback)
    {
        var row_headers = table.find("thead tr");
        var rows_content = table.find("tbody tr");
        rows_content.empty();

        if(has_headers_changed)
        {
            row_headers.css("display", (headers.length === 0) ? "none" : "table-row");
            row_headers.empty();
            for(var header of headers)
            {
                if(header !== undefined)
                {
                    row_headers.append($("<th></th>").text(header));
                }
            }
        }

        var start = page * page_max;
        for(var i = start; i < start + page_max; ++i)
        {
            var element = content[i];
            var row_content = $(rows_content[i - start]).empty();
            if(element !== undefined && callback !== undefined && typeof callback === "function")
            {
                callback(row_content, i, element);
                row_content.children().each((index, cell) =>
                {
                    var header = $($(row_headers.get(0)).get(index));
                    var cell = $(cell);
                    //INSPECTER HEADER
                    cell.addClass(header.hasClass("td-left") ? "td-left" : "");
                    cell.addClass(header.hasClass("td-center") ? "td-center" : "");
                    cell.addClass(header.hasClass("td-right") ? "td-right" : "");
                });
            }
        }

        pagination.navigate(page + 1, Math.ceil((content.length) / page_max));
    }
    
    alert(div, count, text_none, text_one, text_default)
    {
        var alert = div;
        switch(count)
        {
            case 0:
                alert.removeClass("alert-success").addClass("alert-danger");
                alert.children(".swp-count-value").text("");
                alert.children(".swp-count-label").text(text_none);
            break;
    
            case 1:
                alert.removeClass("alert-danger").addClass("alert-success");
                alert.children(".swp-count-value").text("");
                alert.children(".swp-count-label").text(text_one);
            break;
    
            default:
                alert.removeClass("alert-danger").addClass("alert-success");
                alert.children(".swp-count-value").text(count);
                alert.children(".swp-count-label").text(text_default);
            break;
        }
    }

    update(callback)
    {
        if(callback !== undefined && typeof callback === "function")
        {
            callback();
        }

        return this.trigger("update");
    }
}