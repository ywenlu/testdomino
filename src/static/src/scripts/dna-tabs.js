const DURATION_FADE_DEFAULT = 200;

class Tabs
{
    constructor()
    {
        this.items = $("#app #content .article ul.nav.nav-tabs .nav-item .nav-link");
        this.items.on("click", e =>
        {
            this.activate($(e.target));
        });

        this.contents = $("#app #content .article .nav-content");
        this.contents.removeClass("active");
    }

    activate(tab)
    {
        var item = $("");
        switch(typeof tab)
        {
            case "number":
                item = $(this.items[tab]);
            break;

            case "string":
                item = this.items.filter(".nav-link[data-tab=" + tab + "]");
            break;

            default:
                item = $(tab);
            break;
        }

        if(!item.hasClass("active") && !item.hasClass("disabled"))
        {
            this.items.removeClass("active");
            item.addClass("active");

            this.contents.fadeOut(DURATION_FADE_DEFAULT).promise().then(() =>
            {
                this.contents.removeClass("active");

                var content = this.contents.filter((".nav-content[data-tab=" + item.attr("data-tab") + "]"));
                content.addClass("active");
                content.fadeIn(DURATION_FADE_DEFAULT);
            });
        }
    }
}

$(document).ready(() =>
{
    var tabs = new Tabs();
    tabs.activate(0);
});