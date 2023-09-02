package common

import (
	"net"

	log "github.com/sirupsen/logrus"
)

// ClientStream Interface to interact with the client socket
type ClientStream struct {
	conn  net.Conn
	ID    string
	msgID int
}

// NewClientStream Initializes client socket. In case of
// failure, error is printed in stdout/stderr and exit 1
// is returned
func NewClientStream(ID string, ServerAddress string) *ClientStream {
	conn, err := net.Dial("tcp", ServerAddress)
	if err != nil {
		// Exits the program
		log.Fatalf(
			"action: connect | result: fail | client_id: %v | error: %v",
			ID,
			err,
		)
	}
	log.Infof("action: connect | Connected to server on %v", ServerAddress)
	stream := &ClientStream{
		conn:  conn,
		ID:    ID,
		msgID: 1,
	}
	return stream
}

// Send Sends data in byte format to the server preventing short writes
func (c *ClientStream) Send(data []byte) error {
	for totalSent := 0; totalSent < len(data); {
		sent, err := c.conn.Write(data[totalSent:])
		if err != nil {
			log.Errorf("action: send_message | result: fail | client_id: %v | error: %v", c.ID, err)
			return err
		}
		totalSent += sent
	}
	log.Debugf("action: send_message | result: success | client_id: %v | encoded msg: %v", c.ID, data)
	c.msgID++
	return nil
}

// Recv Receives data from the server and returns it in byte format preventing short reads
func (c *ClientStream) Recv(size int) ([]byte, error) {
	data := make([]byte, size)
	for totalRecvBytes := 0; totalRecvBytes < size; {
		recvBytes, err := c.conn.Read(data[totalRecvBytes:])
		if err != nil {
			log.Errorf("action: receive_message | result: fail | client_id: %v | error: %v", c.ID, err)
			return data, err
		}
		totalRecvBytes += recvBytes
	}
	log.Debugf("action: receive_message | result: success | client_id: %v | encoded msg: %v", c.ID, data)
	return data, nil
}

// Close Closes the connection to the server
func (c *ClientStream) Close() {
	log.Info("action: closing_socket | Closing client socket")
	c.conn.Close()
}
