class ArticleUploaded extends Article
{
    constructor(selector, store)
    {
        super(selector, store);
    }

    display_element(name)
    {
        var label = $("<div></div>")
        .addClass("panel-list-section-element dna-navigator")
        .attr("data-target", "rulebased")
        .append($("<i></i>").addClass("fas fa-file"))
        .append($("<span></span>").addClass("panel-list-section-element-text")
        .attr("value", name).text(name))
        .on("click", () =>
        {
            this.select = this.self.find("select#form-select-file");
            this.file = this.store.get_file(name);
            console.log("NAMEEEEE: ", this.file);
            this.select.trigger('change');
        });

        var button_delete = $("<div></div>")
        .addClass("panel-list-section-button panel-list-section-button-danger")
        .append($("<i></i>").addClass("fas fa-times"))
        .on("click", () =>
        {
            this.store.remove_file(name);

            this.refresh();
        });

        this.self.append($("<div></div>").addClass("panel-list-section-group").append(label).append(button_delete));
    }

    display_list()
    {
        return this.fade_out().then(() =>
        {
            this.self.empty();

            for(var name in this.store.files)
            {
                var file = this.store.files[name];
                if(!file.hidden)
                {
                    this.display_element(name);
                }
            }

            return this.fade_in();
        });
    }

    refresh()
    {
        return this.update(() =>
        {
            this.display_list();
        });
    }
}