var http = require('http');

const PORT=2020; 

function handleRequest(request, response){
	var body = '';
	if (request.method == 'POST') {

		request.on('data', function (data) {
			/*****
			* -data --> Buffer --> hexadecimal nonsense
			* -kill connection for payloads > 1MB
			*/

            body += data;
            body = JSON.parse(body);
            if (body.length > 1e6) {
                request.connection.destroy();
            }
            console.log(body);
        });
	} 
    // return a response to client
    // response.end('Mission Accomplished');
    response.writeHeader(200, {'Content-Type': 'application/json'});
    // response.end(body);
    // response.end(JSON.stringify(body));
    response.end();
}

var server = http.createServer(handleRequest);

server.listen(PORT, function(){
    console.log("Server listening on: http://localhost:%s", PORT);
});