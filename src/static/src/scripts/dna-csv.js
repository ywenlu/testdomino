class CSVReader
{
    constructor(data)
    {
        this.data = data;
        this.headers = [];
        this.content = [];
        this.length = 0;
    }

    read(has_headers, separator)
    {
        this.headers = [];
        this.content = [];

        var data = this.data.split(/(?:\r|\n|\r\n)+/);
        if(data.length > 0 && has_headers)
        {
            this.headers = data.splice(0, 1)[0].split(separator);
        }

        for(var row of data)
        {
            if(row.trim() !== "")
            {
                this.content.push(row.split(separator));
                var length = this.content[this.content.length - 1].length;
                if(length > this.length)
                {
                    this.length = length;
                }
            }
        }
    }
}