package common

import (
	"fmt"
	log "github.com/sirupsen/logrus"
	"strings"
)

// BetsMessageBuilder Builder for a BET message
type BetsMessageBuilder struct {
	inBatch uint
	bets    strings.Builder
}

func NewBetsMessageBuilder() *BetsMessageBuilder {
	return &BetsMessageBuilder{
		inBatch: uint(0),
		bets:    strings.Builder{},
	}
}

// AddBet Adds a bet to the message to be sent
func (msg *BetsMessageBuilder) AddBet(line string) {
	if len(strings.Split(line, CommaSeparator)) != FieldsPerLine {
		log.Errorf("action: read_file | result: fail | error: wrong format, skipping line '%v'", line)
		return
	}
	msg.bets.WriteString(line)
	msg.bets.WriteString(CommaSeparator)
	msg.inBatch++
}

func (msg *BetsMessageBuilder) CanAddBet(BatchSize uint) bool {
	return msg.inBatch < BatchSize
}

// Build Builds the BET message to be sent
func (msg *BetsMessageBuilder) Build(id string) string {
	betsToSend := msg.bets.String()
	betsToSend = strings.TrimSuffix(betsToSend, ",")
	return fmt.Sprintf("BET,%d,%s,%s", msg.inBatch, id, betsToSend)
}

// Reset Restarts the builder
func (msg *BetsMessageBuilder) Reset() {
	msg.inBatch = 0
	msg.bets.Reset()
}

func (msg *BetsMessageBuilder) HasBets() bool {
	return msg.inBatch > 0
}
