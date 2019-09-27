class Pagination
{
    constructor(element, offset, onclick)
    {
        this.element = element;
        this.selector = { offset: offset };
        this.limit = { left: false, right: false };
        this.onclick = (onclick !== undefined && typeof onclick === "function") ? onclick : () => {};
    }

    navigate(page, count)
    {
        return this.set_page(page).set_count(count).set_selector().display();
    }

    set_page(page)
    {
        this.page = page;
        return this;
    }

    set_count(count)
    {
        this.count = count;
        return this;
    }

    set_selector()
    {
        this.set_center(this.page, this.selector.offset);

        if(this.selector.min <= 3)
        {
            this.set_center(2 + this.selector.offset + 1, this.selector.offset);
            this.limit.left = true;
        }
        else
        {
            this.limit.left = false;
        }

        if(this.selector.max > this.count - 3)
        {
            this.set_center(this.count - 1 - this.selector.offset - 1, this.selector.offset);
            this.limit.right = true;
        }
        else
        {
            this.limit.right = false;
        }

        return this;
    }

    set_center(value)
    {
        this.selector.center = value;
        this.selector.min = value - this.selector.offset;
        this.selector.max = value + this.selector.offset;

        return this;
    }

    display()
    {
        var pagination = this.element.empty();
        if(this.count > (this.selector.offset + 2) * 2 + 1)
        {
            var items = [];
            for(var i = this.selector.min; i <= this.selector.max; ++i)
            {
                items.push(this.display_element(i));
            }

            pagination.append(
            [
                this.display_element(this.page > 1 ? this.page - 1 : undefined, "<i class='fas fa-angle-left'></i>", true),
                this.display_element(1),
                this.limit.left ? this.display_element(2) : this.display_element(undefined, "..."),
                ...items,
                this.limit.right ? this.display_element(this.count - 1) : this.display_element(undefined, "..."),
                this.display_element(this.count),
                this.display_element(this.page < this.count ? this.page + 1 : undefined, "<i class='fas fa-angle-right'></i>", true)
            ]);
        }
        else
        {
            var items = [];
            for(var i = 1; i <= this.count; ++i)
            {
                items.push(this.display_element(i));
            }

            pagination.append(
            [
                this.display_element(this.page > 1 ? this.page - 1 : undefined, "<i class='fas fa-angle-left'></i>", true),
                ...items,
                this.display_element(this.page < this.count ? this.page + 1 : undefined, "<i class='fas fa-angle-right'></i>", true)
            ]);
        }

        return this;
    }

    display_element(value, text, is_arrow)
    {
        var element = $("<li></li>");
        text = (text !== undefined) ? text : value;

        if(value !== undefined && value !== this.page)
        {
            element.addClass("page-item").append($("<span></span>").addClass("page-link").attr("data-page", value).html(text)).on("click", () =>
            {
                this.onclick(value);
            });
        }
        else
        {
            element.addClass("page-item disabled {0}".format(is_arrow ? "pagination-arrow" : "")).append($("<span></span>").addClass("page-link").html(text));
        }

        return element;
    }
}