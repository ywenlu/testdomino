class FileUpload
{
    constructor(selector, accept, callback)
    {
        this.input = $(selector).on("click", () =>
        {
            this.trigger.click();
            
        });

        this.trigger = $("<input></input>").attr("type", "file").attr("accept", accept).css("display", "none").on("change", function()
        {
            for(var file of this.files)
            {
                var reader = new FileReader();
                reader.onload = (e) =>
                {
                    if(callback !== undefined && typeof callback === "function")
                    {
                        callback(file.name, file.lastModified, file.size, e.target.result);
                    }
                };
                reader.readAsText(file);
            }
        });
    }
}