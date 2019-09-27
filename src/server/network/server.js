const express = require("express");
const spawn = require("child_process").spawn;
const path = require('path');
var fs = require('fs');

const ERROR_QUERY_NOTFOUND = "[ERROR] Query of name {0} not found in API";
const ERROR_SCRIPT_NOTFOUND = "[ERROR] Script of name {0} not found in python scripts";
const SUCCESS_SCRIPT_FOUND = "[PYTHON] Script of name {0} called";

const scriptDir = path.join(path.dirname(require.main.filename), "/script/");
const vizdir = path.join(path.dirname(require.main.filename), "/viz/");
const args_folder = path.join(path.dirname(require.main.filename), "/data/");

class Server
{
	constructor(path, dbcon, api, script)
	{
		this.socket = express();
		this.socket.use("/", express.static(path));
		this.socket.use(express.json({ limit: "100mb" }));

		this.socket.get("/api", (request, response) =>
		{
			if(this.dbcon !== undefined && request.query !== undefined && request.query.id !== undefined)
			{
				var query = this.api[request.query.id];
				var args = (request.query.args !== undefined) ? request.query.args : [];
				if(query !== undefined)
				{
					this.dbcon.get(query, args, rows =>
					{
						response.send(rows);
					});
				}
				else
				{
					console.error(ERROR_QUERY_NOTFOUND.format(request.query.id));
				}
			}
		});
		

		this.socket.post("/python_script", (request, response) =>
		{
			if(request.body !== undefined && request.body.id !== undefined)
			{
				var script = this.script[request.body.id];
				var args = (request.body.args !== undefined) ? request.body.args : [];
				if(script !== undefined)
				{
					console.log("PYTHON SCRIPT CALLED...")
		
					for (let index = 0; index < args.length ; index++)
					{
						args[index] = JSON.stringify(args[index]);
						if (!fs.existsSync(args_folder)){
							fs.mkdirSync(args_folder);
						}
						fs.writeFile(args_folder + 'args_' + index + '.json', args[index], 'utf8', (err) =>
						{
							if (err) throw err;
						});
					}
					
					var proc = spawn('python', [scriptDir + script]);
					proc.stdout.on('data', (data) =>
					{
						response.send(data);
					})
				}
				else
				{
					console.error(ERROR_SCRIPT_NOTFOUND.format(request.body.id));
				}
			}

		});

		this.socket.get("/visualisation", (request, response) =>
		{
			response.sendFile('hierarchical.html', {
				root: "C:/Users/alemercier/Documents/sherlock-ui/src/viz/"
			});
		});

		this.dbcon = dbcon;
		this.api = (api !== undefined) ? api : [];
		this.script = (script !== undefined) ? script : [];
	}

	listen(host, port)
	{
		this.socket.listen(port);
	}
}

module.exports.Server = Server