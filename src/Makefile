#  Makefile
#  Nine-Board Tic-Tac-Toe
#  COMP3411/9414/9814 Artificial Intelligence
#  Alan Blair
#  UNSW Session 1, 2014

CC = gcc
CFLAGS = -Wall -g -O3

default: agent

agent: agent.o client.o game.o common.h agent.h game.h
	$(CC) $(CFLAGS) -o agent agent.o client.o game.o

servt9: servt9.o game.o common.h game.h agent.h
	$(CC) $(CFLAGS) -o servt9 servt9.o game.o

randt9: randt9.o client.o game.o common.h agent.h game.h
	$(CC) $(CFLAGS) -o randt9 randt9.o client.o game.o

all: servt9 randt9 agent

%o:%c common.h agent.h
	$(CC) $(CFLAGS) -c $<

clean:
	rm -f servt9 randt9 agent *.o
