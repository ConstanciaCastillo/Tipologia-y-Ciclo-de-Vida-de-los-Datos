#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import os


URL ='http://www.aemet.es/es/eltiempo/prediccion/provincias'
req = requests.get(URL)
status_code = req.status_code

df = pd.DataFrame(columns=['PROVINCIA','POBLACION', 'TEMP_MAXIMA_HOY', 'TEMP_MINIMA_HOY','TEMP_MAXIMA_MANANA','TEMP_MINIMA_MANANA'])
for dia in (1,2):

 contador = 0
 if status_code == 200:

    # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
   soup = BeautifulSoup(req.text, "html.parser")
   body = soup.find('ul',attrs={'class':'oculta_enlaces'})
   #print(body) 
   
   for row in body.findAll("a"): 
       URL2='http://www.aemet.es' 
       provincia = row.string
       URL2= URL2+row.get('href')+str(dia)
       #print(URL2)
       req2 = requests.get(URL2)
       status_code2 = req2.status_code 
       
       if status_code2 == 200:
        soup2 = BeautifulSoup(req2.text, "html.parser")
        body2= soup2.find('tbody')
        #print(body2)
        

        for row in body2.findAll("tr"):
            cells = row.findAll('td')
            
            temp_maxima=cells[0].find(text=True)
            temp_minima=cells[1].find(text=True)
            cells = row.findAll('th')
            poblacion=cells[0].find(text=True)
            
            
            
            if dia == 1:
               df.loc[contador]=[provincia,poblacion,temp_maxima,temp_minima,'null','null']
            if dia ==2:
               
               df.loc[contador]['TEMP_MAXIMA_MANANA']=temp_maxima
               df.loc[contador]['TEMP_MINIMA_MANANA']=temp_minima
            contador = contador + 1
      
      
            
       else:
        print(status_code)
     
 else:   
    print(status_code)     
df.to_csv('temperaturas_poblaciones_hoy_y_manana.csv', index=False, header=True,sep=';',decimal='.')    

