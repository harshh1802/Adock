const app = require('express')();
const http = require('http').Server(app);
const io = require('socket.io')(http);

const reconnectInterval = 2000;

app.get('/', function (req, res) {
  res.sendFile(__dirname + '/index.html');
});

io.use((socket, next) => {
  const originalEmit = socket.emit;
  socket.emit = function (event, ...args) {
      console.log(`Event received: ${event}, Data:`, args);
      originalEmit.apply(socket, [event, ...args]);
  };
  next();
});

io.sockets.on('connection', function (socket) {
  socket.on('subscribe', function (room) {
    console.log('joining room', room);
    socket.join(room);
  })

  socket.on('unsubscribe', function (room) {
    socket.leave(room);
  })

    // Broadcast the event to all connected clients  
    socket.on('message', (data) => {         
        io.emit('message', data);                            
    });                                              
                                                   
    socket.on('start', (data) => {               
        io.emit('start', data);             
      });                               
                                                 
      socket.on('stop', (data) => {                
        io.emit('stop', data);                
      });

      socket.on('cameraAnalytics', (data) => {                
        io.emit('cameraAnalytics', data);                
      });

      socket.on('dynamicAds', (data) => {                
        io.emit('dynamicAds', data);                
      });

                                   
  });                              
                                                   
  http.listen(8080, function () {                  
    console.log('listening on *:8080');
  });                     