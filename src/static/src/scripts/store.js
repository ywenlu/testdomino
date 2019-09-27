class Store
{
    queryScript(id, args, callback)
    {
        console.log(id);
        console.log(args);
        return axios({method:'post', url: "/python_script", data:{ id: id, args: args }})
        .then(response =>
        {
            if(response && callback !== undefined && typeof callback === "function")
            {
                callback(response.data);
            }
        })
        .catch(error =>
        {
            console.error(error);
        });
    }

    constructor()
    {
        this.listeners = [];
        this.files = {};
    }

    get_file_all()
    {
        var files = {};
        for(var file in this.files)
        {
            if(!this.files[file].hidden)
            {
                files[file] = this.files[file];
            }
        }

        return files;
    }

    get_file(key)
    {
        return this.files[key];
    }

    insert_file(name, modified, size, data)
    {
        var name_replacer = name;

        var count = 0;
        while(this.files[name_replacer] !== undefined)
        {
            name_replacer = "{0} ({1})".format(name, ++count)
        }
        
        this.files[name_replacer] = { name: name_replacer, type: name.substr(name.lastIndexOf(".") + 1), modified: modified, size: size, data: data, separator: undefined, hidden: false };
        this.files[name_replacer].rules =
        {
            "type": [],
            "id": [],
            "required": [],
            "min": [],
            "max": [],
            "min_relative": [],
            "max_relative": [],
            "allowed_references": [],
            "dependencies": [],
            "required_if_null": [],
            "regex": []
        }

    }

    remove_file(name)
    {
        if(this.files[name] !== undefined)
        {
            this.files[name].data = undefined;
            this.files[name].hidden = true;
        }
    }
}
