#!/usr/bin/env python
# coding: utf-8

# In[2]:


# import os
import pandas as pd

# import numpy as np
import plotly.express as pl
from pathlib import Path

# import datetime


# In[3]:


# TODO Pfad muss bei euch verändert werden. Ihr könnt gerne diese Zeile verändern, sodass sie bei uns allen funktioniert.
root_dir = "/Users/jonathan/Documents/GitHub/Uni/data-science-viz/project_wild_fire/data/bmel-statistik_de"

# Alle Dateien aus allen Directories zu pathlist hinzufügen, die mit "1B.csv" enden.
# Anschließend die Pfade in String umwandeln um sie sortieren zu können.
pathlist = Path(root_dir).rglob("*1B.csv")
pathlist = [str(file) for file in pathlist]
pathlist.sort()

# Auslesen der Dateien aus pathlist und erstellen von Dataframes aus den csv files.
# Hinzufügen zur dframes Liste um sie anschließend zu einem einzigen Dataframe zu vereinigen.
dframes = []
for path in pathlist:
    dframes.append(pd.read_csv(path))

df = pd.concat(dframes)
print(df)


# In[4]:


# Basic info über das Dataframe

print("columns: ", df.columns)
print("Rows :", df.index)
print("size: ", df.size)
print("shape: ", df.shape)
print("Number of Dimensions: ", df.ndim)
print(df.index)


# In[5]:


print(df.info)


# In[6]:


# Daten für Baden Würtemberg zwischen 1991-2020
df.loc[0]


# In[7]:


# Anzahl an Waldbränden in Baden-Würtemberg zwischen 1991-2020
print(df["Zusammen Anzahl "][0].astype(float))


# In[8]:


"""
Visualisierung der Anzahl an Waldbränden in Baden-Würtemberg zwischen 1991 und 2020 mit Trendlinie.
"""

fig = pl.scatter(
    x=range(1991, 2019), y=df["Zusammen Anzahl "][0].astype(float), trendline="ols"
)
fig.show()


# In[21]:


"""
Visualisierung der Waldbrandflächen in Deutschland pro Jahr. 
Hier werden allerdings Werte über tausend durch den '.' als Komma gelesen und sind deshlab nahe 0.'
"""


for i in range(0, 18):
    pl.scatter(x=range(1991, 2019), y=df["Zusammen Anzahl "][i].astype(float))

# fig1= pl.scatter(x = range(1991, 2019), y = df['Zusammen Anzahl '][18].astype(float))
# fig1.show()
# detuschland_fpj = df['Zusammen Anzahl '][18]
# print(detuschland_fpj)


# In[10]:


"""
Anzahl an Waldbränden in Bremen von 1991 - 2020

Hier sind noch 'o' anstatt '0' in den Daten"""
df["Zusammen Anzahl "][4]


# In[11]:


# Ein bisschen wasa ausprobieren
df.corrwith(df["Zusammen Anzahl "])


# In[ ]:


# In[ ]:
