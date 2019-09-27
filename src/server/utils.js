const readline = require("readline").createInterface({ input: process.stdin, output: process.stdout });

console.read = function(message, hide, ...args)
{
    if(args.length > 0)
    {
        var callback = args[args.length - 1];
        if(callback !== undefined && typeof callback === "function")
        {
            args = args.slice(0, args.length - 1)
            readline.question("{0} ".format(message.format(...args)), callback);
        }
    }
}

String.prototype.format = function()
{
    return this.replace(/{(\d+)}/g, (match, number) => typeof arguments[number] != "undefined" ? arguments[number] : match);
}

