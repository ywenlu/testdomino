$(document).ready(() =>
{
    $(".panel-list-section-progress").each(function()
    {
        var count = 0;

        var div_progress = $(this);
        div_progress.children(".panel-list-progress-stage").each(function()
        {
            var div_progress_stage = $(this);
            var div_progress_stage_index = $("<div></div>").addClass("panel-list-progress-stage-index").text(++count);
            var div_progress_stage_text = $("<div></div>").addClass("panel-list-progress-stage-name").text(div_progress_stage.text());
            var div_separator = (count > 1) ? $("<div></div>").addClass("panel-list-progress-separator") : undefined;

            div_progress_stage.empty()
            .append(div_progress_stage_index)
            .append(div_progress_stage_text)
            .before(div_separator);
        });
    });
});