#!/bin/sh

message="[NETCAT] Hello, World!"

echo "Sending message to server..."
result=$(echo "$message" | nc $SERVER $PORT)

if [ "$result" == "$message" ] 
then
    echo "OK: Received the same message"
else
    echo "ERROR: Not the same message"
fi