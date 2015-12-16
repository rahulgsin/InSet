
.. sidebar:: Navigation Links

   * :doc:`Home<index>`
   * :ref:`Table of contents<index_label>`
   * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`  

Ngspice user guide
**************************************
.. image:: /images/nglogo.jpg

Download the latest version of ngspice by clicking the following link:
http://sourceforge.net/projects/ngspice/files/

You can find detailed installation guide here: http://sourceforge.net/p/ngspice/ngspice/ci/master/tree/INSTALL?format=raw

How to install ngspice on Linux
================================

The following software packages must be installed in your system to compile ngspice:

|  *bison, flex, X11 headers, libs*

You can install the above requirements by executing the following commands in the terminal :

|  ``sudo apt-get update``
|  ``sudo apt-get install build-essential linux-headers-`uname -r```
|  ``sudo apt-get install libtool automake autoconf``
|  ``sudo apt-get install flex bison texinfo``
|  ``sudo apt-get install libx11-dev libxaw7-dev``

1)After downloading the latest version of ngspice and required packages, unpack the tarball file(e.g. ngspice-26.tar.gz) by writing the following command in the terminal:

|  ``$ tar -zxvf ngspice-26.tar.gz``

2)Now chnage the directory where you can find the INSTALL file. After doing this write the following commands in the terminal:

|  ``$ mkdir release``
|  ``$ cd release``
|  ``$ ../configure --with-x --enable-xspice --disable-debug --enable-cider --with-readline=yes --enable-openmp``
|  ``$ make 2>&1 | tee make.log``
|  ``$ sudo make install``

This will give you a fully featured ngspice in Linux.

How to use Ngspice
=====================
|  1)Open any editor.

|  2)Write a code for your circuit and save it as *.cir* extension. 

|  3)Open Terminal 

|  4)Execute the following command:

|  ``ngspice``

|  5)Change the directory where you save your file.

|  6)Run the following command:

|  ``source <filename.cir>``

NGspice and python interfacing for BPM
=======================================
Figure shows the output at one of the plate of BPM in Python and Ngspice

.. image:: /images/ngsp.png


.. automodule:: ngplot
    :members:

use the manual here to learn about NGspice: [NGSPICE]_.

