const app = require("express")();
const httpServer = require("http").createServer(app);
const options = {
    cors: {
        origin: '*',
    }
};
const io = require("socket.io")(httpServer, options);
const bodyParser = require('body-parser');
const port = process.env.PORT || 4000;

app.use(bodyParser.json());

const broadcastToChannel = (channel, event, data) => {
    io.to(channel).emit(event, data);
};

app.post('/broadcast', function (req, res) {

    res.end();

    const input = req.body;
    const {channel, event, data} = input;
    broadcastToChannel(channel, event, data);
});

io.on("connection", socket => {
    socket.on('subscribe', function (room) {
        socket.join(room);
    });
    socket.on('unsubscribe', function (room) {
        socket.leave(room);
    });
});


httpServer.listen(port, () => {
  console.log(`Socket.IO server running at http://localhost:${port}/`);
});