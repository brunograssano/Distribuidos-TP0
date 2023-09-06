package common

import (
	"encoding/binary"
	"fmt"
	log "github.com/sirupsen/logrus"
)

// Serializer Middleware between business logic and communication logic.
// Serializes and deserializes messages sent through the socket
type Serializer struct {
	conn          *ClientStream
	ID            string
	serverAddress string
}

// NewSerializer Creates a new serializer. The connection will be managed by the serializer
func NewSerializer(ID string, ServerAddress string) *Serializer {
	serializer := &Serializer{
		conn:          NewClientStream(ID, ServerAddress),
		ID:            ID,
		serverAddress: ServerAddress,
	}
	return serializer
}

// SendBet Sends a bet message to the server.
func (s *Serializer) SendBets(betsBuilder *BetsMessageBuilder) error {
	return s.send(betsBuilder.Build(s.ID))
}

// SendFinish Sends a finish message to the server
func (s *Serializer) SendFinish() error {
	return s.send(fmt.Sprintf("FIN,%s", s.ID))
}

// AskForWinners Sends a message for the server asking for the winners of this lotto agent
func (s *Serializer) AskForWinners() error {
	return s.send(fmt.Sprintf("WIN,%s", s.ID))
}

// Connect Connects to the server again
func (s *Serializer) Connect() {
	s.conn = NewClientStream(s.ID, s.serverAddress)
}

// send sends a string message to the server together with its size
func (s *Serializer) send(message string) error {
	dataToSend := []byte(message)
	bytesToSendVal := len(dataToSend)
	log.Infof("action: send_message | client_id: %v | msg size: %v | Sending message: %v",
		s.ID,
		bytesToSendVal,
		message,
	)
	bytesToSendArray := make([]byte, 4)
	binary.BigEndian.PutUint32(bytesToSendArray, uint32(bytesToSendVal))
	err := s.conn.Send(bytesToSendArray)
	if err != nil {
		return err
	}
	err = s.conn.Send(dataToSend)
	return err
}

// RecvResponse Receives a message from the server
func (s *Serializer) RecvResponse() (*ServerResponse, error) {
	messageSizeBytes, err := s.conn.Recv(4)
	if err != nil {
		return nil, err
	}
	messageSize := int(binary.BigEndian.Uint32(messageSizeBytes))
	log.Infof("action: receive_message | result: success | client_id: %v | expected msg size: %v",
		s.ID,
		messageSize,
	)
	message, err := s.conn.Recv(messageSize)
	if err != nil {
		return nil, err
	}
	decodedMsg := string(message)
	log.Infof("action: receive_message | result: success | client_id: %v | msg: %v",
		s.ID,
		decodedMsg,
	)
	return NewServerResponse(decodedMsg)
}

// Close Closes the connection to the server
func (s *Serializer) Close() {
	s.conn.Close()
}
