#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  py_jpk_msh.py
#  
#  Copyright 2019 Slawomir Sygula <slawek@slawek-ThinkPad-T61>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import sys
import mt940
import os.path as PT
import xml.etree.ElementTree as ET
from datetime import date, time, datetime

def main(args):
    return 0

def xmlfile():
    x = 'jpk_wb'
    d = str(date.today().year)+str(date.today().month)
    x += d
    nr = 1
    while PT.isfile('./'+x+str(nr)+'.xml'):
         nr +=1
    return x+str(nr)+'.xml' 
       
def mtfile(x):
    if x != '':
       return x
    else:
       x = input('Podaj nazwę pliku: ')
    if x == '': 
       x = 'export20170328085554.mt940'
       print('Domyślna nazwa pliku: '+x)
       return x

def root_jpk():
    x = ET.Element('JPK',attrib={'xmlns':'http://jpk.mf.gov.pl/wzor/2016/03/09/03092/','xmlns:etd':'http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2016/01/25/eD/DefinicjeTypy/'})
    return x
    
def Naglowek(x):
    x = ET.SubElement(root, 'Naglowek')
    ET.SubElement(x, 'KodFormularza',attrib={'kodSystemowy':'JPK_WB(1)','wersjaSchemy':'1-0'}).text ='JPK_WB'
    ET.SubElement(x, 'WariantFormularza').text = '1'
    ET.SubElement(x, 'CelZlozenia').text = '1'
    ET.SubElement(x, 'DataWytworzeniaJPK').text = datetime.now().isoformat('T','seconds')

if __name__ == '__main__':
    infile = ''
    try: 
        sys.argv[1] 
    except IndexError: 
        infile = ''
    else:
        infile = sys.argv[1]
        
    mtf = mtfile(infile)
    if PT.isfile('./'+mtf):
        tran, xmlf = mt940.parse('./'+mtf), xmlfile()
        print(tran.data['account_identification'])
        print(xmlf)
        root = root_jpk()
        Naglowek(root)
        ET.ElementTree(root).write(xmlf,short_empty_elements=False)
        
    else:
        print('Nie ma pliku o nazwie: '+mtf)
    sys.exit(main(sys.argv))
