import express from 'express';
import { createServer } from 'http';
import { Server } from 'socket.io';

const app = express();
app.use(express.json({ limit: '10mb' }));

const httpServer = createServer(app);
const io = new Server(httpServer, {
  cors: {
    origin: '*',
    methods: ['GET', 'POST']
  }
});

const PORT = 8003;

// Socket.io Real-Time Room Manager
io.on('connection', (socket) => {
  console.log(`🔌 [Socket.io] İstemci bağlandı: ${socket.id}`);

  // Join a specific event album room
  socket.on('join_album', (mediaKey) => {
    if (mediaKey) {
      socket.join(mediaKey);
      console.log(`📌 [Socket.io] ${socket.id} -> Odaya katıldı: ${mediaKey}`);
    }
  });

  // Leave album room
  socket.on('leave_album', (mediaKey) => {
    if (mediaKey) {
      socket.leave(mediaKey);
    }
  });

  // Client initiated media update
  socket.on('notify_media_change', (payload) => {
    const { mediaKey } = payload || {};
    if (mediaKey) {
      io.to(mediaKey).emit('media_updated', payload);
      io.emit('global_media_updated', payload);
    } else {
      io.emit('media_updated', payload);
    }
  });

  socket.on('disconnect', () => {
    console.log(`⚡ [Socket.io] İstemci ayrıldı: ${socket.id}`);
  });
});

// REST API endpoint for Python server or external Webhooks to notify Socket.io server
app.post('/api/socket-notify', (req, res) => {
  const payload = req.body || {};
  const { mediaKey } = payload;
  
  if (mediaKey) {
    io.to(mediaKey).emit('media_updated', payload);
  }
  io.emit('global_media_updated', payload);
  
  res.json({ success: true, broadcastedTo: mediaKey || 'global' });
});

app.get('/health', (req, res) => {
  res.json({ status: 'ok', activeClients: io.engine.clientsCount });
});

httpServer.listen(PORT, () => {
  console.log(`🚀 [Node.js Socket.io Server] Port ${PORT} üzerinde bağımsız olarak çalışıyor!`);
});
