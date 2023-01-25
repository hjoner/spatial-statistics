import pandas as pd
import numpy as np
import json
from jenkspy import JenksNaturalBreaks

def atribui_cor(gdf):
    gdf['fatos'] = gdf['fatos'].fillna(0)
    lista = list(gdf.fatos.unique())


    ### JENKS
    jnb = JenksNaturalBreaks(4)
    jnb.fit(lista)
    breaks = jnb.inner_breaks_
    break1 = jnb.inner_breaks_[0]
    break2 = jnb.inner_breaks_[1]
    break3 = jnb.inner_breaks_[2]
    print(breaks)


    gdf['cor1'] = 0
    gdf['cor2'] = 0
    gdf['cor3'] = 0

    x = 0
    while x < len(gdf):
        if gdf['fatos'][x] <= break1:
            gdf['cor1'][x] = 254
            gdf['cor2'][x] = 229
            gdf['cor3'][x] = 217
        if gdf['fatos'][x] > break1 and gdf['fatos'][x] <= break2:
            gdf['cor1'][x] = 252
            gdf['cor2'][x] = 174
            gdf['cor3'][x] = 145
        if gdf['fatos'][x] > break2 and gdf['fatos'][x] <= break3:
            gdf['cor1'][x] = 251
            gdf['cor2'][x] = 106
            gdf['cor3'][x] = 74
        if gdf['fatos'][x] >= break3:
            gdf['cor1'][x] = 203
            gdf['cor2'][x] = 24
            gdf['cor3'][x] = 29

        x += 1
        
    return gdf

def atribui_cor_compara(gdf):
    gdf['fatos'] = gdf['fatos'].fillna(0)
    lista = list(gdf.fatos.unique())


    ### BREAKS FIXOS
    
    break1 = 0.75
    break2 = 0.25
    break3 = -0.25
    break4 = -0.75

    


    gdf['cor1'] = 0
    gdf['cor2'] = 0
    gdf['cor3'] = 0

    x = 0
    while x < len(gdf):
        if gdf['fatos'][x] >= break1:
            gdf['cor1'][x] = 202
            gdf['cor2'][x] = 0
            gdf['cor3'][x] = 32
        if gdf['fatos'][x] < break1 and gdf['fatos'][x] >= break2:
            gdf['cor1'][x] = 244
            gdf['cor2'][x] = 165
            gdf['cor3'][x] = 130
        if gdf['fatos'][x] < break2 and gdf['fatos'][x] >= break3:
            gdf['cor1'][x] = 247
            gdf['cor2'][x] = 247
            gdf['cor3'][x] = 247
        if gdf['fatos'][x] < break4 and gdf['fatos'][x] >= break4:
            gdf['cor1'][x] = 146
            gdf['cor2'][x] = 197
            gdf['cor3'][x] = 222
        if gdf['fatos'][x] <= break3:
            gdf['cor1'][x] = 5
            gdf['cor2'][x] = 113
            gdf['cor3'][x] = 176

        x += 1
    print(gdf['fatos'])
    return gdf