package common

import (
	log "github.com/sirupsen/logrus"
	"strconv"
	"strings"
)

const WinnerMessage = "WIN"
const LaterMessage = "LATER"

const MessageTypeIndex = 0
const TotalWinnersMessageIndex = 1
const WinnerDocumentOffsetInWinnersMessage = 2

// ServerResponse Represents a response from the server
type ServerResponse struct {
	messageType string
	Winners     []string
}

// NewServerResponse Serializes the string message into a ServerResponse struct
func NewServerResponse(msg string) (*ServerResponse, error) {
	parts := strings.Split(msg, CommaSeparator)
	messageType := parts[MessageTypeIndex]
	var Winners []string
	if messageType == WinnerMessage {
		totalWinners, err := strconv.Atoi(parts[TotalWinnersMessageIndex])
		if err != nil {
			log.Errorf("action: message_parser | result: fail | err: %v | msg: %v", err, msg)
			return nil, err
		}
		for i := 0; i < totalWinners; i++ {
			Winners = append(Winners, parts[i+WinnerDocumentOffsetInWinnersMessage])
		}
	}
	response := &ServerResponse{
		messageType: messageType,
		Winners:     Winners,
	}
	return response, nil
}

func (res *ServerResponse) WantsToAskLater() bool {
	return res.messageType == LaterMessage
}
