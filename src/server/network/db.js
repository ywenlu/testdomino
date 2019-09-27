const pg = require("pg")

const DEFAULT_HOST = "localhost";
const DEFAULT_PORT = "5432";
const DEFAULT_DATABASE = "postgres";
const DEFAULT_USER = "postgres";
const LOG_CONNECTION_SUCCESS = "[LOG] Connection established with user {0} on {1}:{2}/{3}"
const LOG_QUERY_SUCCESS = "[LOG] Query successful for {0} on {1}:{2}/{3} ({4})";
const PROMPT_PASSWORD = "[PROMPT] Password for {0} on {1}:{2}/{3} :";
const ERROR_CONNECTION_FAILED = "[ERROR] Could not connect with user {0} on {1}:{2}/{3}";
const ERROR_QUERY_FAILED = "[ERROR] Query failed for {0} on {1}:{2}/{3} ({4})";

class Connection
{
    constructor(host, port, database, user)
    {
        this.reset(host, port, database, user);
    }

    reset(host, port, database, user)
    {
        this.client = new pg.Client(
        {
            host: (host !== undefined) ? host : DEFAULT_HOST,
            port: (port !== undefined) ? port : DEFAULT_PORT,
            database: (database !== undefined) ? database : DEFAULT_DATABASE,
            user: (user !== undefined) ? user : DEFAULT_USER
        });
    }

    connect(callback)
    {
        console.read(PROMPT_PASSWORD, true, this.client.user, this.client.host, this.client.port, this.client.database, value =>
        {
            this.client.password = value;
            this.client.connect(error =>
            {
                if(!error && callback !== undefined && typeof callback === "function")
                {
                    console.error(LOG_CONNECTION_SUCCESS.format(this.client.user, this.client.host, this.client.port, this.client.database));
                    callback();
                }
                else
                {
                    console.error(ERROR_CONNECTION_FAILED.format(this.client.user, this.client.host, this.client.port, this.client.database));
                    this.client.end(() =>
                    {
                        this.reset(this.client.host, this.client.port, this.client.database, this.client.user);
                        this.connect(callback);
                    });
                }
            });
        });
    }

    get(query, args, callback)
    {          
        this.client.query(query, args, (error, res) =>
        {
            if(!error)
            {
                console.log(LOG_QUERY_SUCCESS.format(this.client.user, this.client.host, this.client.port, this.client.database, query));
                if(callback !== undefined && typeof callback === "function")
                {
                    callback(res.rows);
                }
            }
            else
            {
                console.error(ERROR_QUERY_FAILED.format(this.client.user, this.client.host, this.client.port, this.client.database, query));
                console.error(error.stack);
            }
        })
    }

    disconnect()
    {
        this.client.end();
    }
}

module.exports.Connection = Connection