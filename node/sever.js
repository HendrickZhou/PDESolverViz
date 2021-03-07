const httplib = require('http');

httplib.createServer(function(request, response){
    response.writeHead(200, {'content-type': 'text'});
    response.end('<!DOCTYPE html><html><stronge>hello you node js</stronge></html>');
}).listen(8888);

console.log("starting sever")