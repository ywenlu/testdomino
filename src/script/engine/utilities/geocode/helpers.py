from engine.utilities.geocode.geo_loc_classes import *
from engine.utilities.geocode.df_to_geojson import *
from engine.utilities.geocode.create_map import *


def file_path(*args):
    '''
    input: strings, a path and a file name to be concatenated as a full path
    output: string, a full path of the form "path/to/my_file"
    '''
    return "/".join(args)


def correct_abbrev(s, map_abbrev):
    '''
    inputs:
        s: string, an address contaning abbreviated routes, e.g AVE, ST,...
        map_abbrev: a dic containing the abbreviations and their full correspondences
    output: string, an address
    '''
    s = s.upper()
    Olds = list(set(map_abbrev.keys()) & set(s.split()))
    if Olds:
        for old in Olds:
            s = s.replace(old, map_abbrev[old])
    return s


def responses_to_df(responses):
    '''
    input: a list of google and/or osm objects
    output: a data frame
    '''
    df = pd.DataFrame({'Query': [r.query for r in responses],
                      'Response': [r.get_resp_address() for r in responses],
                      'Score': [r.score for r in responses],
                      'long': [r.get_longitude() for r in responses],
                      'lat': [r.get_latitude() for r in responses],
                      'Geo Shape': [r.geometry for r in responses]})
    
    df = check_duplicates(df)
    
    return df


def check_duplicates(df):
    '''
    Check whether there are not NaN duplicated coordinates
    input : a data frame with Geo Shapes
    output: a data frame with a supplementary 'Duplicated_coords' (1 if duplicated, 0 w/o)
    '''
    df['Duplicated_coords'] = df.duplicated(['lat', 'long'], keep = False)*1

    if any(df['Duplicated_coords'] > 0):
        #print("\nSuspicion of duplicated locations:")
        #print(df[['Query', 'lat', 'long']][df['Duplicated_coords']>0])
        pass
    return df


def run_queries(Queries, tol=100):
    '''
    input: a list of addresses
    output: a list of objects (osm and/or gg)
    '''

    # OSM queries first
    #print("\nQuerying OSM API...")
    responses = [osm(query) for query in Queries]
    
    # Find bad scores (>tol). It might be something like > some_tol (50, 100, ?)
    idx = [i for i, r in enumerate(responses) if r.score >= tol]
    #print("\nOSM: %d ambiguous or NULL result(s) (%.2f%%)!\n" % (len(idx), len(idx)*100.0/len(responses)))

    # Run Google API on bad OSM outputs : not found or bad score (match_score > tol)
    #print("Querying Google API on %d missing locations..." % len(idx))

    resp_gg = [gg(query) for query in Queries[idx]]

    # Replace ambiguous OSM responses with Google responses if valide, empty() o/w
    for i, l in zip(idx, resp_gg):
        if l.score < tol:
            responses[i] = l
        else:
            responses[i] = empty(l.query)

    # Final performance
    final_missing = [r.score >= tol for r in responses]
    n_missing = np.sum(final_missing)    
    n_queries = len(Queries)
    n_found = n_queries - n_missing 
    #print("\nFinal: %d location(s) found out of %d (%.2f%%)\n" % (n_found, n_queries, n_found*100./n_queries))
    
    if np.sum(final_missing)>0:
        missing = [r.query for r in responses if r.score >= tol]
        #print("Addresse(s) not found:")
        #print("\n".join(missing))

    return responses


def GeoLoc(df, tol):
    '''
    input: a data frame with:
            - mandatory columns used for querying APIs: 'Address', 'ZipCode', 'City', 'State', 'Country'
            - any other supplementary column(s) you may need
    output: a data frame with the corresponding geolocations
    '''
    mandatory = ['ZipCode', 'Country', 'Address',  'City', 'State']
    #mandatory = ['Address', 'ZipCode', 'City', 'Country']
    test_col = all([m in list(df.columns) for m in mandatory])

    if not test_col:
        sys.exit("Your data must contain the following mandatory columns: %s" % (", ".join(mandatory)))

    # ZipCode must contain 5 digits. Add a '0' on left if len(zipcode) < 5
    df['ZipCode'] = ["0" + str(z) if len(z) < 5 else z for z in df['ZipCode'].astype(str)]

    # Maybe not relevant to use 'Name' in Google requestes (GG_Queries)
    # GG_Queries = df.apply(lambda z: ", ".join(z), axis = 1)[:5]
    Queries = df[mandatory].apply(lambda z: ", ".join(z), axis = 1)

    # Run queries
    #print("%d address to locate..." % (len(Queries)))
    responses = run_queries(Queries, tol)
    
    # # Concatenate the initial df with responses, then return
    return pd.concat([df, responses_to_df(responses)], axis=1)


