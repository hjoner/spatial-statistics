import geopandas as gpd
from shapely.geometry import Point


def contagem(df, gdf):

    df['geometry'] = df[["lng", "lat"]].apply(Point, axis=1)
    df = gpd.GeoDataFrame(df)
    sjoin = gpd.sjoin(df, gdf, how='left')
    contagem = sjoin.full_text.value_counts().rename_axis('precincts').reset_index(name='counts')
    gdf['fatos'] = 0
    lista_gdf = list(contagem['precincts'])
    x = 0
    while x < len(gdf):
        if gdf['full_text'][x] in lista_gdf: 
            valor = contagem[contagem['precincts'] == gdf['full_text'][x]].reset_index(drop=True)
            valor = valor['counts'][0]
            gdf['fatos'][x] = valor

        if gdf['full_text'][x] not in lista_gdf:
            gdf['fatos'][x] = 0
            
        x += 1
    
    gdf.to_file('precincts2.GeoJSON', driver="GeoJSON")

    return gdf

