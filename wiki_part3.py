# pip install wheels
# pip install pipwin
#
# pipwin install numpy
# pipwin install pandas
# pipwin install shapely
# pipwin install gdal
# pipwin install fiona
# pipwin install pyproj
# pipwin install six
# pipwin install rtree
# pipwin install geopandas
# matplotlib==3.0.3
import pandas as pd

# import necessary packages
import matplotlib.pyplot as plt
import geopandas as gpd
import wiki_part1 as wp1
import reader


def plot_to_map(telnevek,position,detail='no'):
    #load the basemap
    telep = pd.DataFrame()
    # try:
    telep = reader.file_reader('C:\\Users\\TamasPriksz\\Desktop\\sajat\\project_wiki\\thematic_mapper\\DATA\\magyar_telep_nevek_all.xlsx')##all.xlsx')
    # except Exception as e:
    #     print("Settlement list not available", e)
    #
    # if not telep:
    # ### if the excel is not availbale, pull it from the net
    #     df_valid_tn = wp1.wikidownload_tulnev()
    #     df_valid = wp1.wikidownload_szavak()
    #     telep = df_valid.append(df_valid_tn)
    #     print(telep)

    basemap_itself = gpd.read_file('C:\\Users\\TamasPriksz\\Desktop\\sajat\\project_wiki\\thematic_mapper\\DATA\\appended_map_data_cleaned.shp')


    try:
        mapped_telep = wp1.telep_start_mapper(telep,telnevek,position)
        map_telep_combo = pd.merge(basemap_itself, mapped_telep[['telepnev','valid_start']], left_on='name', right_on='telepnev', how='left')
        if position == 'ends':
            telep_to_show = map_telep_combo.loc[map_telep_combo["valid_start"].isin([each_string.lower() for each_string in telnevek])] #'_'+
        elif position == 'contains':
            telep_to_show = map_telep_combo.loc[map_telep_combo["valid_start"].isin([each_string.lower() for each_string in telnevek])] #'_'+
        else:
            telep_to_show = map_telep_combo.loc[map_telep_combo["valid_start"].isin([each_string.capitalize() for each_string in telnevek])] #'_'+

        if detail == 'yes':
            print(telep_to_show)
        else:
            pass

        fig, ax = plt.subplots()
        basemap_itself.plot(ax=ax, facecolor='grey', alpha=0.1)
        basemap_itself.plot(facecolor='white', legend=False, figsize=(150, 100), alpha=0.1, ax=ax);

        telep_to_show.plot(ax=ax)
        telep_to_show.plot(facecolor="none", column='valid_start',categorical=True,legend=True, figsize=(150,100),ax=ax);

        plt.show()

    except KeyError:
        print('no data')



def input_data():
    settlement_list = []
    i = 0
    position = input('Choose search part - starts/ends/contains: ')
    details = input('Display settlement list - yes/no: ')
    print('Add up to 10 settlement - leave emtpy to skip')
    while i < 4:
        i = i+1
        settlement = input('Add settlement: ').capitalize()
        if not settlement:
            break
        else:
            settlement_list.append(settlement)


    return settlement_list, position, details

tellist, type, details = input_data()
#print(tellist, type)

plot_to_map(tellist, type ,details)

