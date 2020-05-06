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
import functions as fns
import reader


def data_get():
    telep = pd.DataFrame()
    telep = reader.file_reader('C:\\Users\\TamasPriksz\\Desktop\\sajat\\project_wiki\\thematic_mapper\\DATA\\magyar_telep_nevek_all.xlsx')
    basemap_itself = gpd.read_file('C:\\Users\\TamasPriksz\\Desktop\\sajat\\project_wiki\\thematic_mapper\\DATA\\appended_map_data_cleaned.shp')

    return telep, basemap_itself


def detail_show(value='no'):
    if value == 'yes':
        return True
    else:
        return False


def data_to_map(telnevek,position):

    telep, basemap_itself = data_get()

    try:
        mapped_telep = fns.telep_start_mapper(telep=telep, telep_to_map=telnevek, position=position)
        map_telep_combo = pd.merge(basemap_itself, mapped_telep[['telepnev','valid_start']], left_on='name', right_on='telepnev', how='left')
        if position == 'ends':
            telep_to_show = map_telep_combo.loc[map_telep_combo["valid_start"].isin([each_string.lower() for each_string in telnevek])] #'_'+
        elif position == 'contains':
            telep_to_show = map_telep_combo.loc[map_telep_combo["valid_start"].isin([each_string.lower() for each_string in telnevek])] #'_'+
        else:
            telep_to_show = map_telep_combo.loc[map_telep_combo["valid_start"].isin([each_string.capitalize() for each_string in telnevek])] #'_'+

    except KeyError:
        print('no data')

    return telep_to_show, basemap_itself



def plot_to_map(telnevek, position):

    telep_to_show, basemap_itself = data_to_map(telnevek=telnevek, position=position)

    fig, ax = plt.subplots()
    basemap_itself.plot(ax=ax, facecolor='grey', alpha=0.1)
    basemap_itself.plot(facecolor='white', legend=False, figsize=(150, 100), alpha=0.1, ax=ax);

    telep_to_show.plot(ax=ax)
    telep_to_show.plot(facecolor="none", column='valid_start', categorical=True, legend=True, figsize=(150, 100),
                       ax=ax);

    plt.show()


def map_details(telnevek, position, detail='no'):

    if detail_show(detail) == True:
        telep_to_show, basemap_itself = data_to_map(telnevek=telnevek, position=position)

        return telep_to_show

    else:
        pass




    # else:
    #
    #     fig, ax = plt.subplots()
    #     basemap_itself.plot(ax=ax, facecolor='grey', alpha=0.1)
    #     basemap_itself.plot(facecolor='white', legend=False, figsize=(150, 100), alpha=0.1, ax=ax);
    #
    #     telep_to_show.plot(ax=ax)
    #     telep_to_show.plot(facecolor="none", column='valid_start',categorical=True,legend=True, figsize=(150,100),ax=ax);
    #
    #     plt.show()






