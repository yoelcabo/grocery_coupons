#!/bin/bash

#Script that asks for repeated user input to register supermarket monopoly tickets

echo Who is the ticket owner?

read -p 'TicketOwner: ' owner

#while true get new ticket number and run the python command
while true
do

read -p 'Ticket#: ' ticketNum

echo $owner
echo $ticketNum

python monopoly.py --insert-code $ticketNum -c $owner

done
