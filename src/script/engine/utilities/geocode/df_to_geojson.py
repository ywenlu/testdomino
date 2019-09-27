####################
# Required libraries
####################
import pandas as pd
import re
import numpy as np
import json
import sys
####################
####################

def geoPoint(long, lat):
    '''Create a geoJSON point given its longitude and latitude'''
    return str({"type": "Point", "coordinates": [long, lat]})

def geoPolygon(polygon_2D):
    '''Create a geoJSON polygon given its vertex coordinates passed as a 2D array'''
    return str({"type": "Polygon", "coordinates": [polygon_2D]})

def kwargs_dict(foo):
    '''Creates a dict of args names and values from a pandas Series'''
    d = {str(k): str(v) for k, v in zip(foo.index, foo.values)}
    return d

def feature_dict(id, geo_shape, **kwargs):
    '''Creates an individual GEO SHAPE dictionary'''

    '''Inputs:
    - A point Id (must be unique)
    - A valid GEO SHAPE (Point coordinates, Polygon coordinates,...)
    - A list of items to add as point properties
    '''

    '''Output:
    A GEO SHAPE compatible dict
    '''

    D = {"type":"Feature",
         "id":str(id),
         "properties":{str(k): str(v) for k, v in kwargs.items()},
         "geometry":geo_shape} #json.loads(geo_shape)
    
    return(D)

def Featurize(df, Id, GeoShape, property_list):
    '''Creates a list of individual GEO SHAPE dictionaries'''

    '''Inputs:
    - A pandas data frame containing the points (or polygons) locations
    - An Id column name: it can be any of the df columns, providing Ids are unique for each point
    - A valid GEO SHAPE column name (Point coordinates, Polygon coordinates,...)
    - A list of items to add as properties
    '''

    '''Output:
    A list of GEO SHAPE compatible dictionaries
    '''

    n = df.shape[0]
    features = []
    for ii in range(n):
        try:
            id = df[Id][ii]
            geo_shape = df[GeoShape][ii]
            args = kwargs_dict(df[property_list].iloc[ii])
            features.append(feature_dict(id, geo_shape, **args))
        except:
            #print("Error on idx: %d" % ii)
            break

    return features

# def clean_geoShape(df, GeoShape):
#     '''Check whether all of the entries have non empty coordinates.
#     In case of yes, the corresponding rows will be removed from df.
#     '''

#     if pd.isnull(df[GeoShape]).any():
#         idx = [ii for ii, v in enumerate(df[GeoShape]) if pd.isnull(v)]
#         df = df.dropna(subset=[GeoShape]).reset_index(drop=True)
#         print("%d entries have been removed due to missing Geo Shapes." % len(idx))

#     # Replace single quotes with double quotes in GEO SHAPE dicts
#     # df[GeoShape] = df[GeoShape].str.replace('\'','\"')

#     return df

def clean_geoShapes(df):
    '''
    Remove entries for which no location was found (coordinates = [nan, nan])
    input: a pandas data frame with a "Geo Shape" column (as dictionaries)
    output: a pandas data frame with the non located points removed (entire rows), if any
    '''

    # coordinates = [json.loads(d.replace("'", "\""))['coordinates'] for d in df['Geo Shape']]
    coordinates = [gs['coordinates'] for gs in df['Geo Shape']]
    idx = [i for i, coord in enumerate(coordinates) if 'nan' in coord]

    if len(idx) > 0:
        df = df.drop(idx).reset_index(drop = True)

    return df, len(idx)


def create_property_list(dfColumns, Id, GeoShape, property_list):
    '''Check whether all the args passed are valid (exist in df).
        If 'property_list' is empty (None) all the available columns in df will be used, excepting 'Id' and 'GeoShape'
    '''

    if property_list is not None:
        check = [arg in dfColumns for arg in property_list]
        try:
            assert(sum(check)==len(check))
        except AssertionError:
            #print("'%s' not in dataframe!" % property_list[check.index(False)])
            raise SystemExit
    else:
        property_list = list(dfColumns)
        for c in [Id, GeoShape]:
            property_list.remove(c)

    #print("Item(s) as propertie(s):")
    for p in property_list:
        #print("\t- %s" % p)
        pass

    return property_list

def make_geoJSON(df, GeoShape='Geo Shape', Id=None, property_list=None):
    '''This is the main function for creating a geoJSON file from a pandas dataframe'''

    '''Inputs:
    - A pandas data frame containing the points (or polygons) locations
    - An Id (a column name). It can be any of the df columns, providing values are unique for each point
    - A valid 'Geo Shape' column name (Point coordinates, Polygon coordinates,...)
    Notice that if Geo Shapes are not available, but 'Long' and 'Lat' are provided, make_geoJSON will create Geo Shapes for you.
    - A list of items to add as points properties. If 'None' (defaults) all of the columns will be used, excepting the 'Id'
    and the 'Geo Shape' columns.
    '''

    '''Output:
    A geoJSON file
    '''

    #print("\nBuilding geoJSON data...")
    
    df, n_missing = clean_geoShapes(df)

    if Id is None:
        df['Index'] = np.arange(df.shape[0])
        Id = 'Index'
    
    property_list = create_property_list(df.columns, Id, GeoShape, property_list)
    features = Featurize(df, Id, GeoShape, property_list)
    geojson_data = {"type":"FeatureCollection", "features":features}

    #print("\nFeatures have been created for %d entries." % len(features))
    #print("%d point(s) removed due to missing Geo Shapes!\n" % n_missing)

    return geojson_data

def save_geojson(geojson_data, filename):
    '''To save a geoJSON file on disk'''

    '''Inputs:
    - A geoJSON file
    - A filename
    Notice that if the filename as no '.geojson' extention, this will be added for you.
    '''

    '''Output:
    None
    '''

    if not re.match("(.*)\.geojson$", filename):
        filename += '.geojson'
        
    with open(filename, 'w') as f:
        json.dump(geojson_data, f, indent=4)

    return None

