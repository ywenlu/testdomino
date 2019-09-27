import os
import argparse
import webbrowser


##############################
# GEOLOC MAIN FUNCTION
##############################

def geoloc(fullpath, tol):
    filename = os.path.basename(fullpath)
    path = os.path.dirname(fullpath)
    geoloc_name = filename.replace(".csv", "_geoloc.csv")
    geojson_name = filename.replace(".csv", "_geoloc.geojson")

    #print("\nReading %s..." % filename)
    df = pd.read_csv(fullpath, sep=";", dtype=str, encoding="iso-8859-1")
    df = df.fillna("")

    # Querying APIs
    geoloc = GeoLoc(df, tol)

    # Saving geolocs as <input>.csv
    #print("\nSaving geoloc file...")
    geoloc.to_csv(file_path(path, geoloc_name), sep = ";", index = False, encoding="iso-8859-1")
    #print("File saved: %s" % file_path(path, geoloc_name))

    # Render geoJSON, then save it as <input>.geoJSON
    geojson = make_geoJSON(geoloc)
    #print("\nSaving geojson file...")
    save_geojson(geojson, file_path(path, geojson_name))
    #print("File saved: %s" % file_path(path, geojson_name))

    #print("\nDone !")

    #print("\n\t***************************")
    resp = input("\tPreview map (y/N)?: ")
    if resp.lower() == 'y':
        map_name = filename.replace(".csv", ".html")
        # map_ = create_map(file_path(path, geojson_name))
        map_ = folium_map(file_path(path, geojson_name))
        map_.save(outfile = file_path(path, map_name))
        url = 'file://' + os.path.abspath(file_path(path, map_name))
        webbrowser.open(url)
    else:
        sys.exit()


##############################
# RUN
##############################

if __name__ == '__main__':

    # #############################
    # %%% GET COMMAND LINE ARGS %%%
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', help="The full path to the file", type= str)
    parser.add_argument('--tol', help="Tolerance when comparing query and found address", type= int)

    args = parser.parse_args()

    fullpath = args.path
    tol =  args.tol
    geoloc(fullpath, tol)