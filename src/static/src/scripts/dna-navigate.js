class Navigator
{
    move(page)
    {
        var url = new URL(window.location.href);
        if(page !== undefined && page !== "")
        {
            url.searchParams.set("page", page);
        }
        else
        {
            url.searchParams.delete("page");
        }
    
        history.pushState("", document.head.title, url);
    }

    refresh()
    {
        var fragment = new URL(window.location.href).searchParams.get("page");
        if(fragment !== null && fragment !== undefined)
        {
            var div_content = $("#content");
            if(div_content.length > 0)
            {
                div_content.load("fragments/" + fragment + ".html", data =>
                {
                    //console.log(data);
                    var breadcrumb = $("#fragment").attr("data-breadcrumb");
                    if(breadcrumb !== undefined)
                    {
                        var div_breadcrumb = $(".breadcrumb");
                        div_breadcrumb.empty();
                        div_breadcrumb.append("<li class='breadcrumb-item'><i class='fas fa-users'></i></li>");
                        for(var child of breadcrumb.split(","))
                        {
                            div_breadcrumb.append("<li class='breadcrumb-item'>" + child + "</li>");
                        }
                        div_breadcrumb.children().last().addClass("active");
    
                    }
                    //console.log(breadcrumb);
                });
            }
        }
    }
}

$(document).ready(() =>
{
    var navigator = new Navigator();
    navigator.refresh();

    $(".dna-navigator").each((_, element) =>
    {
        $(element).on("click", () =>
        {
            var fragment = $(element).attr("data-target");
            navigator.move(fragment);
            navigator.refresh();
        });
    });
});