TOPOS SIGNAL CHAIN from BPM plates to ADC
******************************************

``.include att10.cir
.include att20.cir
.include att30.cir
.include amp10.cir
.include amp20.cir
*.include buf.cir
.model switch1 sw 

Vin 1 0 ac sin(0 100m 10meg)

*switchable attenuator of -30db
* Vsw1=5 and vsaw1=-5 for Off 1 
Vsw1 sn1 0 DC 5	
swa1 1 2 sn1 0 switch1 OFF
Vswa1 sna1 0 DC -5		
Xatt35 img1 2 att30
swaimg2 1 img1 sna1 0 switch1 OFF
*
*switchable attenuator of -30db
Vsw2 sn2 0 DC -5
swa2 2 3 sn2 0 switch1 OFF
Vswa2 sna2 0 DC 5		
Xatt31 img2 3 att30
swaimg3 2 img2 sna2 0 switch1 OFF
*
*head ampliflier of 20db
rser1	3 0 1meg
Xamp20 3 4 amp20
*
*switchable attenuator of -10db
*always off---> dont disturb this ckt 
*Vsw5 sn5 0 DC 5		
*swa5 4 img05 sn5 0 switch1 OFF
*Vswa5 sna5 0 DC -5
*Xatt10 img04 img05 att10		
*swaimg4 4 img05 sna3 0 switch1 OFF

*buffer
*Xbuf1 4 img05 buf
*
*switchable attenuator of -20db
Vsw4 sn4 0 DC -5
swa4 4 5 sn4 0 switch1 OFF
Vswa4 sna4 0 DC 5		
Xatt20 img4 5 att20
swaimg5 4 img4 sna4 0 switch1 OFF
*
*switchable attenuator of -10db
Vsw3 sn3 0 DC 5		
swa3  5 6 sn3 0 switch1 OFF
Vswa3 sna3 0 DC -5
Xatt10 img3 6 att10		
swaimg6 5 img3 sna3 0 switch1 OFF

*drive amplifier of 20db
Xamp21 6 7 amp20
rser2	6 0 75
*
*post amplifier
Xamp10 7 8 amp10
rser3	7 0 75
*
.CONTROL
AC 	DEC 	5 100k 1000MEG
*plot mag(v(1)) mag(v(2)) mag(v(3)) mag(v(4)) mag(v(5)) mag(v(6)) mag(v(7)) mag(v(8))
tran 1ns 1us
plot V(1) 
plot v(2)
plot v(3)
plot v(4)
plot v(5)
plot v(6)
plot v(7)
plot v(8)
*.include plotng.txt``
