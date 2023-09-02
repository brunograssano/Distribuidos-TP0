package common

import log "github.com/sirupsen/logrus"

// ClientConfig Configuration used by the client
type ClientConfig struct {
	ID            string
	ServerAddress string
	Name          string
	Surname       string
	Document      string
	BirthDate     string
	Number        string
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

// StartClientLoop Send bet message to the server and wait for confirmation.
// In case of error it closes the connection and finishes
func (c *Client) StartClientLoop() {

	c.serializer = NewSerializer(c.config.ID, c.config.ServerAddress)
	err := c.serializer.SendBet(c.config.Name, c.config.Surname, c.config.Document, c.config.BirthDate, c.config.Number)
	if err != nil {
		c.serializer.Close()
		return
	}
	c.serializer.RecvResponse()
	log.Infof("action: apuesta_enviada | result: success | dni: %v | numero: %v", c.config.Document, c.config.Number)
	c.serializer.Close()

}
