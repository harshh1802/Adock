from socketio import Client
import logging
import time
from threading import Event

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RedisEventListener:
    def __init__(self, server_url):
        # Configure client without ping settings
        self.sio = Client(
            logger=True,
            engineio_logger=True,
            reconnection=True,
            reconnection_delay=1,
            reconnection_delay_max=5
        )
        self.server_url = server_url
        self.connected = False
        self.exit_event = Event()
        
        # Set up event handlers
        self.sio.on('connect', self.on_connect)
        self.sio.on('disconnect', self.on_disconnect)
        self.sio.on('connect_error', self.on_connect_error)
        self.sio.on('start', self.on_start)
        self.sio.on('stop', self.on_stop)
        self.sio.on('dynamicAds', self.on_dynamic_ads)
        
    def connect(self):
        """Connect to the Socket.IO server"""
        try:
            logger.info(f"Attempting to connect to {self.server_url}")
            self.sio.connect(
                self.server_url,
                transports=['websocket']
            )
            
            # Keep the connection alive until exit_event is set
            while not self.exit_event.is_set():
                if not self.sio.connected:
                    logger.warning("Connection lost, attempting to reconnect...")
                time.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("Shutting down client...")
            self.exit_event.set()
            self.sio.disconnect()
        except Exception as e:
            logger.error(f"Connection failed: {str(e)}")
            
    def on_connect(self):
        """Handler for successful connection"""
        self.connected = True
        logger.info('Successfully connected to server')
        
    def on_disconnect(self):
        """Handler for disconnection"""
        self.connected = False
        if not self.exit_event.is_set():
            logger.warning('Disconnected from server - will attempt to reconnect')
        
    def on_connect_error(self, error):
        """Handler for connection errors"""
        logger.error(f"Connection error: {error}")
        
    def on_start(self, data):
        """Handler for 'start' event"""
        logger.info(f'Received start event: {data}')
        # Add your processing logic here
        
    def on_stop(self, data):
        """Handler for 'stop' event"""
        logger.info(f'Received stop event: {data}')
        # Add your processing logic here
        
    def on_dynamic_ads(self, data):
        """Handler for 'dynamicAds' event"""
        logger.info(f'Received dynamicAds event: {data}')
        # Add your processing logic here

if __name__ == '__main__':
    server_url = 'http://p2826.local:8081'
    client = RedisEventListener(server_url)
    client.connect()