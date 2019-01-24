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
import lxml.etree as ET
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
       x = 'Statement_12_2018.STA'
       print('Domyślna nazwa pliku: '+x)
    return x

def root_jpk():
    XML_NS = 'http://jpk.mf.gov.pl/wzor/2016/03/09/03092/'
    ETD_NS = 'http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2016/01/25/eD/DefinicjeTypy/'
    NS_MAP = {None: XML_NS, "etd": ETD_NS}
    rootname = ET.QName(XML_NS,'JPK')
    x = list()
    x.append(ET.Element(rootname,nsmap=NS_MAP))
    x.append(ET.ElementTree(x[0]))
    return x
    
def Naglowek(x,od,do):
    y = ET.SubElement(x, 'Naglowek')
    ET.SubElement(y, 'KodFormularza',attrib={'kodSystemowy':'JPK_WB(1)','wersjaSchemy':'1-0'}).text ='JPK_WB'
    ET.SubElement(y, 'WariantFormularza').text = '1'
    ET.SubElement(y, 'CelZlozenia').text = '1'
    ET.SubElement(y, 'DataWytworzeniaJPK').text = datetime.now().isoformat('T','seconds')
    ET.SubElement(y, 'DataOd').text = od.isoformat()
    ET.SubElement(y, 'DataOd').text = do.isoformat()
    ET.SubElement(y, 'DomyslnyKodWaluty').text = 'PLN'
    ET.SubElement(y, 'KodUrzedu').text = '1209' #kod urzędu dla Krakowa Nowej Huty

def Podmiot1(x):
# Dodać wprowadzanie z pliku json
# -------------------------------
    podmiot = ET.SubElement(x, 'Podmiot1')
    ident = ET.SubElement(podmiot,'IdentyfikatorPodmiotu')
    ET.SubElement(ident,'NIP').text = '6760013533'
    ET.SubElement(ident,'PelnaNazwa').text = 'Małopolska Spółka Handlowa A.Chwedczuk Spółka Jawna'
    ET.SubElement(ident,'REGON').text = '12344324'
    adres = ET.SubElement(podmiot, 'AdresPodmiotu')
    ET.SubElement(adres, 'KodKraju').text = 'PL'
    ET.SubElement(adres,'Wojewodztwo').text = 'małopolskie'
    ET.SubElement(adres,'Powiat').text = 'Kraków'
    ET.SubElement(adres,'Gmina').text = 'Kraków'
    ET.SubElement(adres,'Ulica').text = 'Nowolipki'
    ET.SubElement(adres,'NrDomu').text = '3'
    ET.SubElement(adres,'NrLokalu')
    ET.SubElement(adres,'Miejscowosc').text = 'Kraków'
    ET.SubElement(adres,'KodPocztowy').text = '31-532'
    ET.SubElement(adres,'Poczta').text = 'Kraków'
    
def NumerRachunku(x,trans):
    nrrach = ET.SubElement(x, 'NumerRachunku')
    nrrach.text = trans.data['account_identification']
    
def Salda(x,trans):
    bal = ET.SubElement(x,'Salda')
    pocz = ET.SubElement(bal,'SaldoPoczatkowe')
    pocz.text = repr(trans.data['final_opening_balance'].amount.amount)
    kon = ET.SubElement(bal,'SaldoKoncowe')
    kon.text = repr(trans.data['final_closing_balance'].amount.amount)

#def WyciagWiersz(x,tr):

#def WyciagCtrl(x,wiersze,debet,credit):

def UserData(t):
    isValid = False
    while not isValid:
        pod = input('Podaj datę '+t+' [rrrr-mm-dd]: ')
        try:
             d = datetime.strptime(pod,'%Y-%m-%d')
             isValid = True
        except ValueError:
             print('Błędna data, spróbuj ponownie')
    return d
    
if __name__ == '__main__':
    infile = ''
# path to the mt940 file
    path = './work'
    try: 
        sys.argv[1] 
    except IndexError: 
        infile = ''
    else:
        infile = sys.argv[1]
        
    mtf = mtfile(infile)
    if PT.isfile(path+'/'+mtf):
        alltran, xmlf = mt940.parse(path+'/'+mtf), xmlfile()
        print('NumerRachunku:'+repr(alltran.data['account_identification']))
#        print('SaldoPoczątkowe:'+repr(alltran.data['final_opening_balance'].amount.currency))
#        print('SaldoKoncowe:'+repr(alltran.data['final_closing_balance']))
        Ok = True
        while Ok:
            dataOd = UserData('Od')
            dataDo = UserData('Do')
            if dataOd<=dataDo:
              Ok = False
            else:
              print('Błędne daty')
        print(xmlf)
        root = root_jpk()
        Naglowek(root[0],dataOd,dataDo)
        Podmiot1(root[0])
        NumerRachunku(root[0],alltran)
        Salda(root[0],alltran)
#        for tr in alltan:
#            WyciagWiersz(root[0],tr)
            
        root[1].write(xmlf,pretty_print=True,doctype='<?xml version="1.0" encoding="UTF-8"?>')
        
    else:
        print('Nie ma pliku o nazwie: '+mtf)
    sys.exit(main(sys.argv))
