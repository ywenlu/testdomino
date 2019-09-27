const fs = require("fs")
const utils = require("./server/utils")
const db = require("./server/network/db")
const server = require("./server/network/server")

const LOG_CONNECTION_DB = "[LOG] Attempting connection to database...";
const LOG_CONNECTION_LISTEN = "[LOG] Listening on port {0}:{1}...";
const ERROR_CONFIG_INVALID = "[ERROR] Could not parse config file : invalid syntax";

function init(filename, callback)
{
    var config = {};
    if(fs.existsSync(filename))
    {
        try
        {
            config = JSON.parse(fs.readFileSync(filename).toString());
            if(callback !== undefined && typeof callback === "function")
            {
                callback(config);
            }
        }
        catch(error)
        {
            console.error("{0}\r\n{1}".format(ERROR_CONFIG_INVALID, error.stack));
        }
    }

    return config;
}

function listen(config, dbcon)
{
    console.log(LOG_CONNECTION_LISTEN.format(config.host, config.port));
    var socket = new server.Server(__dirname + config.path, dbcon, config.api, config.python_scripts);
    return socket.listen(config.host, config.port);
}

init("server.json", config =>
{
    if(config.db !== undefined)
    {
        console.log(LOG_CONNECTION_DB);
        var dbcon = new db.Connection(config.db.host, config.db.port, config.db.database, config.db.user);
        dbcon.connect(() => listen(config.website, dbcon));
    }
    else
    {
        listen(config.website);
    }
});