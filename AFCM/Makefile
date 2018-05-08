CC=gcc
LIB=-lm
CFLAGS=-O2 -w

all : afcm

afcm : afcm.o
	${CC} ${CFLAGS} -o afcm afcm.o ${LIB}

afcm.o : afcm.c
	${CC} ${CFLAGS} -c afcm.c

clean:
	rm -f afcm
	rm -f *.o
	rm -f *~
