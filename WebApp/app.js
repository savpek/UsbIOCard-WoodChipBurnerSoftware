var express = require('express'),
    api = require('./routes/api'),
    http = require('http'),
    path = require('path'),
    logger = require('morgan'),
    methodOverride = require('method-override'),
    bodyParser = require('body-parser'),
    io = require('socket.io'),
    errorHandler = require('errorhandler');

var app = module.exports = express();

// all environments
app.set('port', process.env.PORT || 3000);
app.use(logger('dev'));
app.use(bodyParser());
app.use(methodOverride());
app.use(express.static(path.join(__dirname, 'public')));

// development only
if (app.get('env') === 'development') {
    app.use(errorHandler());
}

// production only
if (app.get('env') === 'production') {
}

app.get('/rest/settings', api.settings);

var server = http.createServer(app).listen(app.get('port'), function () {
    console.log('Express server listening at http://localhost:' + app.get('port'));
});

io.listen(server);
