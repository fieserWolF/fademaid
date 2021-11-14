#!/usr/bin/env python

"""
fade2speedcode v1.01 [03.09.2017] *** by WolF
This program converts fade data (1000 bytes) to 6502 speedcode that fills certain areas.
Usage: ./fade2speedcode.py <input fade-file> <output speedcode-file> <speedcode startaddress in hex> <screen startaddress in hex>
Example: ./fade2speedcode.py input.fade output.bin $3000 $6000


output file structure:
----------------------
+0						1byte			max_position from fademaid
+1						max_position	jumptable low: holds the relative offset of each speedcode
+1+max_position			max_position	jumptable high: holds the relative offset of each speedcode
+1+(max_position*2)		unknown			speedcodes for each color



example of what the output speedcode looks like:
------------------------------------------------
;in: a=color
		sta $6000+(40*0)+0
		sta $6000+(40*0)+1
		sta $6000+(40*0)+2
		sta $6000+(40*1)+0
		sta $6000+(40*1)+1
		sta $6000+(40*1)+2
		sta $6000+(40*2)+0
		sta $6000+(40*2)+1
		sta $6000+(40*2)+2
		rts



using the output file:
----------------------
1. first, look up max_position in data.pos using a hex-editor.

2. include the binaries in acme like this:
		max_position		;optional: might be useful to know later in the code
			!binary "data.pos",1,0

		jumptable_low
			!binary "data.pos",max_position,1
		jumptable_high
			!binary "data.pos",max_position,1+max_position
		speedcodes
			!binary "data.pos",,1+(max_position*2)

3. call the speedcode in acme like this:
		!zone _call_speedcode
		_call_speedcode

		;in: x=position, y=new_color

		;-globals
		.jumptable_low	= jumptable_low
		.jumptable_high	= jumptable_high
		;-

			lda .jumptable_low,x
			sta .j+1
			lda .jumptable_high,x
			sta .j+2
		.j	jmp $ffff	;speedcode	y=new color
"""

import sys
import struct
import numpy



PROGNAME = 'fade2speedcode';
VERSION = '1.01';
DATUM = '03.09.2017';

#http://www.6502.org/tutorials/6502opcodes.html
OPCODE_STORE    = 0x8d  #sta absolute
#OPCODE_STORE    = 0x8e  #stx absolute
#OPCODE_STORE    = 0x8c  #sty absolute
OPCODE_RTS    = 0x60


def _do_it(
        filename_in,
        filename_out,
        user_speedcode_start,
        user_screen
    ) :
        
    WIDTH = 40
    HEIGHT = 25

    try:
        screen = int (user_screen, 16)	#convert from hex string
    except ValueError:
        screen = 0

    try:
        speedcode_start = int (user_speedcode_start, 16)	#convert from hex string
    except ValueError:
        speedcode_start = 0


    print ("Opening file \"%s\" for reading..." % filename_in)
    try:
        file_in = open(filename_in , "rb")
    except IOError as (errno, strerror):
        print("I/O error: \"%s\"\n" % strerror)
        return None

    buffer=[]

    data_in = file_in.read()
    for i in range( 0, len(data_in) ):
            temp = struct.unpack('B',data_in[i])
            buffer.append(temp[0])
    file_in.close()

    fade = numpy.asarray(buffer)
    #print fade

    max_value = max(buffer)

    # search for values and fill array
    fillmeall = []
    for c in range (0, max_value) :
#        print c
        fillme = []
        for y in range (0, HEIGHT) :
            for x in range (0, WIDTH) :
                if fade[y*WIDTH+x] == (c+1) :
                    fillme.append((y,x))
        fillmeall.append(fillme)
    fillmenp = numpy.asarray(fillmeall)    
#    print fillmenp

    # fill jumptable buffer
    speedcode_pos = speedcode_start
    jumptable = []
    for c in range (0, max_value) :
        jumptable.append( speedcode_pos )
        speedcode_pos += (len(fillmenp[c]*3)+1)   #3 bytes (!) are used for every sty $0000 + 1byte RTS at the end
 #       print len(fillmenp[c])

    jumptable_np = numpy.asarray(jumptable)
#    print jumptable_np





    print ("Opening file \"%s\" for writing..." % filename_out)
    try:
        file_out = open(filename_out , "wb")
    except IOError as (errno, strerror):
        print("I/O error: \"%s\"\n" % strerror)
        return None


    
    file_out.write(chr(max_value))




    #write jumptable low
    for c in range (0, max_value) :
        file_out.write(chr(jumptable_np[c] & 0b0000000011111111)) #low
    #write jumptable high
    for c in range (0, max_value) :
        file_out.write(chr(jumptable_np[c] >> 8)) #high
    
    
    #write speedcode
    addy = 0
    speedcode_size = 0
    for c in range (0, max_value) :
#        print "------------"
#        print c
#        print fillmenp[c]
#        print len(fillmenp[c])
#        print "------------"
        for i in range (0, len(fillmenp[c])) :
#                print fillmenp[c][i][0] #y
#                print fillmenp[c][i][1] #x
            addy = screen + fillmenp[c][i][0]*WIDTH + fillmenp[c][i][1]
            file_out.write(chr(OPCODE_STORE))
            file_out.write(chr(addy & 0b0000000011111111))   # <$6000+(40*0)+0
            file_out.write(chr(addy >> 8))   # >$6000+(40*0)+0
            speedcode_size += 3
        file_out.write(chr(OPCODE_RTS))
        speedcode_size += 1



    file_out.close()

    print "done. $%x bytes speedcode, $%x values" %(speedcode_size, max_value)
    
    return None



def _main_procedure() :
    print("%s v%s [%s] *** by WolF"% (PROGNAME, VERSION, DATUM))
    print("This program converts fade data (1000 bytes) to 6502 speedcode that fills certain areas.")
    
    if (len(sys.argv) != 5) :
        print("Usage: %s <input fade-file> <output speedcode-file> <speedcode startaddress in hex> <screen startaddress in hex>" % sys.argv[0])
        print("Example: %s input.fade output.bin 3000 6000" % sys.argv[0])
        return None
    else:
        _do_it(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])



if __name__ == '__main__':
    _main_procedure()
