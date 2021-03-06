
.. sidebar:: Navigation Links

   * :doc:`Home<index>`
   * :ref:`Table of contents<index_label>`
   * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`  

Common Modules
#################

The common modules consist of electronics, optics systems cables etc. They are described and documented here.

Electronics
****************
General Electronics modules

Amplifiers
=============
Generic amplifier and attenuator definition
Figure shows the example of amplificaiton of current profile of 10Mhz frequnecy with a gain of 20db

.. image:: /images/amp.png

.. automodule:: AmpAttModule
    :members:

SPICE examples
^^^^^^^^^^^^^^^

LT1192
-------
You can find the datasheet of LT1192 here: http://cds.linear.com/docs/en/datasheet/1192fa.pdf

Here is Gain(2) vs frequency characteristics:

.. image:: /images/lt1192.jpg

| 1)Gain Bandwidth product, Av = 5:350 Mhz
| 2)Slew rate = 450 V/us
| 3)Input noise voltage = 9nV/sqHz 

LT1363
-------
You can find the datasheet of LT1363 here: http://cds.linear.com/docs/en/datasheet/1363fa.pdf

Here is Gain(2) vs frequency characteristics:

.. image:: /images/lt1363.jpg

| 1)Gain Bandwidth product = 70 Mhz
| 2)Slew rate = 1000 V/us
| 3)Input noise voltage = 9 nV/sqHz 

LT1722
-------
You can find the datasheet of LT1722 here: http://cds.linear.com/docs/en/datasheet/172234fb.pdf

Here is Gain(2) vs frequency characteristics:

.. image:: /images/lt1722.jpg

| 1)Gain Bandwidth product = 200 Mhz
| 2)Slew rate = 70 V/us
| 3)Input noise voltage = 3.8 nV/sqHz 

MAX477
-------
You can find the datasheet of MAX477 here: http://datasheets.maximintegrated.com/en/ds/MAX477.pdf

Here is Gain(2) vs frequency characteristics:

.. image:: /images/max477.jpg

| 1)Gain Bandwidth product = 300Mhz -3dB Bandwidth (Av=+1)
| 2)200 Mhz Full-power Bandwidth(Av=+1)
| 3)Slew rate = 1100 V/us
| 4)Input noise voltage = 5 nV/sqHz

THS3001
-------
You can find the datasheet of THS3001 here: http://www.ti.com.cn/cn/lit/ds/slos217h/slos217h.pdf

Here is Gain(2) vs frequency characteristics:

.. image:: /images/ths3001.jpg

| 1)Gain Bandwidth product = 420Mhz
| 2)Slew rate = 6500 V/us
| 3)Input noise voltage = 1.6 nV/sqHz

Diodes
===========


SPICE examples
^^^^^^^^^^^^^^^

Schottky Barrier Diodes: NSR0320MW2T1G
---------------------------------------

You can find the datasheet of NSR0320MW2T1G here: http://www.farnell.com/datasheets/1708337.pdf

| 1)Low Forward voltage = 0.24V (IF = 10mA)
| 2)Total capacitance = 29pF


ADCs
=========
.. automodule:: AdcModule
    :members:

Frequency response or Transfer Function
********************
Figure shows the example of Transfer function module

.. image:: /images/tf.png

.. automodule:: SpiceFrequencyResponse
    :members:


Lenses
*********
