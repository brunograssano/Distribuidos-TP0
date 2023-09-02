package common

import (
	"bufio"
	log "github.com/sirupsen/logrus"
	"os"
	"strings"
)

const FieldsPerLine = 5
const CommaSeparator = ","

// ClientConfig Configuration used by the client
type ClientConfig struct {
	ID            string
	ServerAddress string
	BetsFile      string
	BatchSize     uint
}

// Client Entity that encapsulates how
type Client struct {
	config     ClientConfig
	serializer *Serializer
	stop       chan bool
}

// NewClient Initializes a new client receiving the configuration
// as a parameter
func NewClient(config ClientConfig) *Client {
	client := &Client{
		config: config,
		stop:  make(chan bool, 1),
	}
	return client
}

// StopClient Closes the connection to the server and signals itself to finish
func (c *Client) StopClient() {
	if c.serializer != nil {
		c.serializer.Close()
	}
	c.stop <- true
	close(c.stop)
}

func (c *Client) closeBetsFile(f *os.File) {
	log.Infof("action: closing_file | Closing bets file")
	f.Close()
}

// StartClientLoop Send bet messages to the server and wait for confirmation.
// In case of error it closes the connection and finishes
func (c *Client) StartClientLoop() {

	c.serializer = NewSerializer(c.config.ID, c.config.ServerAddress)
	defer c.serializer.Close()
	f, err := os.Open(c.config.BetsFile)
	if err != nil {
		log.Errorf("action: open_file | result: fail | file_name: %v | error: %v", c.config.BetsFile, err)
		return
	}
	defer c.closeBetsFile(f)
	scanner := bufio.NewScanner(f)
	betsBuilder := strings.Builder{}
	inBatch := uint(0)

	for scanner.Scan() {
		select {
		case <-c.stop:
			return
		default:
		}
		line := scanner.Text()
		if inBatch < c.config.BatchSize {
			if len(strings.Split(line, CommaSeparator)) != FieldsPerLine {
				log.Errorf("action: read_file | result: fail | file_name: %v | error: wrong format, skipping line", c.config.BetsFile)
				continue
			}
			betsBuilder.WriteString(line)
			betsBuilder.WriteString(CommaSeparator)
			inBatch++
			continue
		}

		if c.sendBatch(inBatch, betsBuilder) != nil {
			return
		}
		betsBuilder.Reset()
		inBatch = 0
	}

	if inBatch != 0 && c.sendBatch(inBatch, betsBuilder) != nil {
		return
	}
	c.serializer.SendFinish()
	if err := scanner.Err(); err != nil {
		log.Errorf("action: read_file | result: fail | file_name: %v | error: %v", c.config.BetsFile, err)
	}

}

func (c *Client) sendBatch(inBatch uint, betsBuilder strings.Builder) error {
	err := c.serializer.SendBets(inBatch, betsBuilder.String())
	if err != nil {
		return err
	}
	_, err = c.serializer.RecvResponse()
	if err != nil {
		return err
	}
	log.Infof("action: apuestas_batch_enviadas | result: success")
	return nil
}
