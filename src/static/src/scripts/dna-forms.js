$(document).onFirst("click", ".form-checkbox", function()
{
    if($(this).hasClass("active"))
    {
        $(this).removeClass("active");
    }
    else
    {
        $(this).addClass("active");
    }
});