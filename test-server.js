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
            if (body.length > 1e6) {
                request.connection.destroy();
            }
            payload = JSON.parse(body);
            console.log(payload);
        });
	} 
    response.writeHeader(200, {'Content-Type': 'application/json'});
    response.end('\n*** Broadcast received! ***\n');
}

var server = http.createServer(handleRequest);

server.listen(PORT, function(){
    console.log("Server listening on: http://localhost:%s", PORT);
});