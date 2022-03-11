import geopandas as gp
import pandas as pd
from os import listdir

def main():
    # Change the path
    path = 'D:/Ebola/grass/Ebola/output/'
    # Here we read corrected shapefiles
    onlyfiles = [f for f in listdir(path) if ('_corrected.shp' in f) and ('.xml' not in f)]

    # Here we extract all unique road types
    road_types = []
    names = []
    for f in onlyfiles:
        names.append(f.replace('_Road200km_corrected.shp', ''))
        df = gp.read_file(path + f)

        # Some unification of column names
        try:
            df.rename({'Road_type':'road_type'}, axis=1, inplace=True)
        except:
            pass
        try:
            df.rename({'Road_Type': 'road_type'}, axis=1, inplace=True)
        except:
            pass

        df = df[['cat', 'road_type', 'len', 'geometry']]

        a = list(df['road_type'].unique())
        for t in a:
            if t not in road_types:
                road_types.append(t)

    # Here we create a dataframe of all study areas with road length (classified by type) for each year
    road_length = pd.DataFrame(index=names, columns=road_types)
    for f in onlyfiles:
        name = f.replace('_Road200km_corrected.shp', '')
        df = gp.read_file(path + f)

        # Some unification of column names
        try:
            df.rename({'Road_type': 'road_type'}, axis=1, inplace=True)
        except:
            pass
        try:
            df.rename({'Road_Type': 'road_type'}, axis=1, inplace=True)
        except:
            pass

        df = df[['cat', 'road_type', 'len', 'geometry']]

        aux = df.groupby('road_type').sum()['len'].reset_index()
        for idx, row in aux.iterrows():
            road_length.loc[name, row['road_type']] = row['len']

    road_length = road_length.reset_index()
    road_length['year'] = road_length["index"].str[-4:]
    road_length['location'] = road_length["index"].str[:-4]
    road_length.drop('index', inplace=True, axis=1)
    road_length.set_index('location', inplace=True)
    road_length.to_csv(path + 'Road_length.csv') # Change the output path

if __name__ == '__main__':
    main()