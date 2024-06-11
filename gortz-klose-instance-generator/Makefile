# Subject: makefile for program gencflp
#          (c-program for generating test problem instances of the CFLP)
# Date   : August 15, 2001

# Compilers:
CC = gcc
CFLAGS = -O4 -Wall -I./

#uncomment the following if debugging is required
#CFLAGS = -g -Wall -I./

# objects, main program, libraries
obj  = gencflp.o rnd.o
main = gencflp
libs = -lm 

$(main):	$(obj)
	$(LINK.c) -o $@ $(obj) $(libs)
	
%.o:	%.c		
	$(COMPILE.c) $<

clean-o:
	rm -f $(obj)
	
clean:
	rm -f $(obj) $(main)
