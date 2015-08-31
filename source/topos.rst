Tune, Orbit and POSition measurement system (TOPOS)
***************************************************

Components of TOPOS
=====================

TOPOS SIGNAL CHAIN from BPM plates to ADC
------------------------------------------

The TOPOS signal chain from BPM plates to the ADCs. It is divided into three distinct stages. Each stage consists of switchable attenuators and amplifiers.

.. image:: /images/topos1.jpeg

And here is the result after simulation of the above circuit:

.. image:: /images/topos2.png

*Code for the above circuit in Ngspice looks like this:*

.include att10.cir

.include att20.cir

.include att30.cir

.include amp10.cir

.include amp20.cir

.model switch1 sw 

Vin 1 0 ac sin(0 100m 10meg)

// Vsw1=5 and vsaw1=-5 for Off 1 

Vsw1 sn1 0 DC 5	

swa1 1 2 sn1 0 switch1 OFF

Vswa1 sna1 0 DC -5		

Xatt35 img1 2 att30

swaimg2 1 img1 sna1 0 switch1 OFF

// switchable attenuator of -30db

Vsw2 sn2 0 DC -5

swa2 2 3 sn2 0 switch1 OFF

Vswa2 sna2 0 DC 5		

Xatt31 img2 3 att30

swaimg3 2 img2 sna2 0 switch1 OFF

// head ampliflier of 20db

rser1	3 0 1meg

Xamp20 3 4 amp20

// switchable attenuator of -20db

Vsw4 sn4 0 DC -5

swa4 4 5 sn4 0 switch1 OFF

Vswa4 sna4 0 DC 5		

Xatt20 img4 5 att20

swaimg5 4 img4 sna4 0 switch1 OFF

// switchable attenuator of -10db

Vsw3 sn3 0 DC 5		

swa3  5 6 sn3 0 switch1 OFF

Vswa3 sna3 0 DC -5

Xatt10 img3 6 att10		

swaimg6 5 img3 sna3 0 switch1 OFF

// drive amplifier of 20db

Xamp21 6 7 amp20

rser2	6 0 75

// post amplifier

Xamp10 7 8 amp10

rser3	7 0 75

.CONTROL

AC 	DEC 	5 100k 1000MEG

tran 1ns 1us

plot V(1) v(2) v(3) v(4) v(5) v(6) v(7) v(8)

.include plotng.txt

  The exctra files which are include in above code can found here:
  
BaseBand tune(Q) measurement system (BBQ)
------------------------------------------
Simple Schemaic of BBQ system configuration at SIS-18 for low energy signal is shown in below circuit:

.. image:: /images/bbql.jpeg

Simple Schemaic of BBQ system configuration at SIS-18 for high energy signal is shown in below circuit:

.. image:: /images/bbqh.jpeg

And here is the result after simulation of the above circuit:

.. image:: /images/bbq1.png

*Ngspice code for one BPM plate is given here:*

| // THS3001 SUBCIRCUIT
| // HIGH SPEED, CURRENT FEEDBACK, OPERATIONAL AMPLIFIER  
| // TEMPLATE=X^@REFDES %IN+ %IN- %Vcc+ %Vcc- %OUT @MODEL
| // CONNECTIONS:      NON-INVERTING INPUT
| //                  | INVERTING INPUT
| //                  | | POSITIVE POWER SUPPLY
| //                  | | | NEGATIVE POWER SUPPLY
| //                  | | | | OUTPUT
| //                  | | | | | 
| //                  | | | | | 
| //                  | | | | | 
.SUBCKT THS3001     1 nois 3 4 5 

| // INPUT 
| Q1	31 32 2 NPN_IN 4
| QD1	32 32 1 NPN 4
| Q2	7 15 2 PNP_IN 4
| QD2	15 15 1 PNP 4

| // PROTECTION DIODES 
| D1	1 3 Din_N 
| D2	4 1 Din_P 
| D3	5 3 Dout_N 
| D4	4 5 Dout_P 

VNoiw nois 2 dc 0 TRNOISE (1m 1n 0 0 )

| // SECOND STAGE 
| Q3	17 31 11 PNP 2
| Q4	16 7 13 NPN 2
| QD3	30 30 17 PNP 3
| QD4	30 30 16 NPN 3
| C1	30 3  0.4p  
| C2	4 30  0.4p  
| F1	3 31 VF1 1
| VF1	33 34 0V
| F2	7 4 VF2 1
| VF2	35 6 0V
| F3	3 12 VF3 1
| VF3	34 11 0V
| F4	14 4 VF4 1
| VF4	13 35 0V

| // FREQUENCY SHAPING 
| E1	18 0 17 0 1
| E2	19 0 16 0 1
| R1	44 18 25
| R2	19 42 25
| C3	0 14  9p  
| C4	0 12  9p
| L1	44 14 2.8n
| L2	42 12 2.8n

| // OUTPUT 
| Q5	3 14 28 NPN 128
| Q6	4 12 29 PNP 128
| C5	28 9  7p  
| R5	9 5  100  
| L3	28 10  30n  
| R7	10 5  8 
| Re	28 29 Rt 50 
| C6	29 21  7p  
| R4	21 5  100  
| L4	29 22  30n  
| R6	22 5  8  

| // BIAS SOURCES 
| G1	3 32 3 4 1.656e-6
| G2	15 4 3 4 1.656e-6
| I1     3 32  DC 308e-6 
| I2    15 4  DC 307e-6
| V1	3 33 0.83
| V2	6 4 0.83


.MODEL Rt RES TC1=-0.006              

| // DIODE MODELS 
| .MODEL Din_N D  IS=10E-21 N=1.836 ISR=1.565e-9 IKF=1e-4 BV=30 IBV=100E-6 RS=105 TT=11.54E-9 CJO=2E-12 VJ=.5 M=.3333
| .MODEL Din_P D  IS=10E-21 N=1.836 ISR=1.565e-9 IKF=1e-4 BV=30 IBV=100E-6 RS=160 TT=11.54E-9 CJO=2E-12 VJ=.5 M=.3333
| .MODEL Dout_N D IS=10E-21 N=1.836 ISR=1.565e-9 IKF=1e-4 BV=30 IBV=100E-6 RS=60  TT=11.54E-9 CJO=2E-12 VJ=.5 M=.3333
| .MODEL Dout_P D IS=10E-21 N=1.836 ISR=1.565e-9 IKF=1e-4 BV=30 IBV=100E-6 RS=105 TT=11.54E-9 CJO=2E-12 VJ=.5 M=.3333

| // TRANSISTOR MODELS 
| .MODEL NPN_IN NPN 
| + IS=170E-18 BF=100 NF=1 VAF=100 IKF=0.0389 ISE=7.6E-18
| + NE=1.13489 BR=1.11868 NR=1 VAR=4.46837 IKR=8 ISC=8E-15
| + NC=1.8 RB=251.6 RE=0.1220 RC=197 CJE=120.2E-15 VJE=1.0888 MJE=0.381406
| + VJC=0.589703 MJC=0.265838 FC=0.1 CJC=133.8E-15 XTF=272.204 TF=12.13E-12
| + VTF=10 ITF=0.294 TR=3E-09 XTB=1 XTI=5 KF=25E-15

| .MODEL NPN NPN 
| + IS=170E-18 BF=100 NF=1 VAF=100 IKF=0.0389 ISE=7.6E-18
| + NE=1.13489 BR=1.11868 NR=1 VAR=4.46837 IKR=8 ISC=8E-15
| + NC=1.8 RB=251.6 RE=0.1220 RC=197 CJE=120.2E-15 VJE=1.0888 MJE=0.381406
| + VJC=0.589703 MJC=0.265838 FC=0.1 CJC=133.8E-15 XTF=272.204 TF=12.13E-12
| + VTF=10 ITF=0.147 TR=3E-09 XTB=1 XTI=5

| .MODEL PNP_IN PNP 
| + IS=296E-18 BF=100 NF=1 VAF=100 IKF=0.021 ISE=494E-18
| + NE=1.49168 BR=0.491925 NR=1 VAR=2.35634 IKR=8 ISC=8E-15
| + NC=1.8 RB=251.6 RE=0.1220 RC=197 CJE=120.2E-15 VJE=0.940007 MJE=0.55
| +  VJC=0.588526 MJC=0.55 FC=0.1 CJC=133.8E-15 XTF=141.135 TF=12.13E-12 
| + VTF=6.82756 ITF=0.267 TR=3E-09 XTB=1 XTI=5 KF=25E-15

| .MODEL PNP PNP 
| + IS=296E-18 BF=100 NF=1 VAF=100 IKF=0.021 ISE=494E-18
| + NE=1.49168 BR=0.491925 NR=1 VAR=2.35634 IKR=8 ISC=8E-15
| + NC=1.8 RB=251.6 RE=0.1220 RC=197 CJE=120.2E-15 VJE=0.940007 MJE=0.55
| +  VJC=0.588526 MJC=0.55 FC=0.1 CJC=133.8E-15 XTF=141.135 TF=12.13E-12 
| + VTF=6.82756 ITF=0.267 TR=3E-09 XTB=1 XTI=5

| .ENDS

.include lt1192.cir

| .MODEL germ d
| +IS=1.88569e-06 RS=0.160685 N=1.03056 EG=0.634401
| +XTI=0.5 BV=20 IBV=1.5e-05 CJO=1.20949e-10
| +VJ=0.4 M=0.520353 FC=0.5 TT=0
| +KF=0 AF=1

//BPM simulation program for NGspice

C1 1 2 50PF

C2 2 0 50PF

XOP1	2 3 4 5 6	LT1192

RO1	3	0	100

RO2	3	6	100

CO1	6	7	15nF

ri1	2	0	1meg

rl	7	0	1meg

VCC1 	4 0 DC 15V

VEE1	5 0 DC -15V

D1 7 8 germ

C3 8 0 1nF 

R2 8 0 1k

C4 8 9 1pf

XOP2	9 10 11 12 13	THS3001

RO3	10	0	10

RO4	10	13	100

C03	13 	14 	1pf

ri2	9	0	1meg

R3	14	0	10k

VCC2	11 0 DC 15v

VEE2	12 0 DC -15v

rfilt	14	15	160

cfilt	15	0	1pf 

AVSRC %V([1]) filesrc

.model filesrc filesource (file="current_profile2.txt" )

.CONTROL

//AC 	DEC 	 1k 500MEG
//PLOT mag(V(2,7)) xlog

TRAN 1NS 5uS

plot  v(1) V(7) v(8) v(15)

plot v(7) v(8)

.include plotng.txt

Simple OPAMP schematic
-----------------------

*Here is the simple schematic of OPAMP:*

.. image:: /images/opamp.jpeg

*And here is the code for simulation of above circuit using LT1192:*

Amplifier of 20db

| .SUBCKT amp20 1 6
| .include lt1192.cir
| XOP	1 2 3 4 5	LT1192
| R1	2	0	100
| R2	2	5	1000
| cL	5	6	15nf
| rl	6	0	1k
| VCC 	3 0 DC 15V
| VEE	4 0 DC -15V
| .ENDS

| Xamp 1 2 amp20
| vin 1 0 ac sin(0 1m 10meg)
| .control
| AC DEC 100 1k 100MEG
| .include plotng.txt

Here you can the results after simulation:

Magnitude response at the oputput

.. image:: /images/omag.png

Phase response at the oputput

.. image:: /images/ophase.png

