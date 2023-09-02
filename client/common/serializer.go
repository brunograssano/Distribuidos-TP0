package common

import (
	"encoding/binary"
	"fmt"
	log "github.com/sirupsen/logrus"
)

// Serializer Middleware between business logic and communication logic.
// Serializes and deserializes messages sent through the socket
type Serializer struct {
	conn *ClientStream
	ID   string
}

// NewSerializer Creates a new serializer. The connection will be managed by the serializer
func NewSerializer(ID string, ServerAddress string) *Serializer {
	serializer := &Serializer{
		conn: NewClientStream(ID, ServerAddress),
		ID:   ID,
	}
	return serializer
}

// SendBet Sends a single bet to the server.
func (s *Serializer) SendBet(Name string, Surname string, Document string, BirthDate string, Number string) error {
	betMessage := fmt.Sprintf("BET,%d,%s,%s,%s,%s,%s,%s", 1, s.ID, Name, Surname, Document, BirthDate, Number)
	dataToSend := []byte(betMessage)
	bytesToSendVal := len(dataToSend)
	log.Infof("action: send_message | client_id: %v | msg size: %v | Sending message: %v",
		s.ID,
		bytesToSendVal,
		betMessage,
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
func (s *Serializer) RecvResponse() (string, error) {
	messageSizeBytes, err := s.conn.Recv(4)
	if err != nil {
		return "", err
	}
	messageSize := int(binary.BigEndian.Uint32(messageSizeBytes))
	log.Infof("action: receive_message | result: success | client_id: %v | expected msg size: %v",
		s.ID,
		messageSize,
	)
	message, err := s.conn.Recv(messageSize)
	if err != nil {
		return "", err
	}
	decodedMsg := string(message)
	log.Infof("action: receive_message | result: success | client_id: %v | msg: %v",
		s.ID,
		decodedMsg,
	)
	return decodedMsg, err
}

// Close Closes the connection to the server
func (s *Serializer) Close() {
	s.conn.Close()
}
