
import requests
import bs4
import pandas as pd
import reader


def wikidownload_telep():
    """
    settlement webscraper
    :return: df_telep settlement list in dataframe
    """

    base_url= "https://hu.wikipedia.org/wiki/Magyarorsz%C3%A1g_telep%C3%BCl%C3%A9sei:_"
    pagelist=["A,_%C3%81","B","C","Cs","D","E,_É","F","G","H","I,_Í","J","K","L","M","N","Ny","O,_Ó","Ö,_Ő","P","R","S","Sz","T","Ty","U,_Ú","Ü,_Ű","V","Z","Zs"]

    l=[]
    for page in pagelist:
        r= requests.get(base_url+str(page))
        c=r.content
        soup = bs4.BeautifulSoup(c, "html.parser")
        all = soup.find_all("div", {"class": "mw-parser-output"})[0].find_all("table", {"class": "wikitable sortable"})[0].find_all("td")
        for item in all:
            # print(item)
            d={}
            try:
                d["TELNEV"] = item.find("a").text
            except:
                pass
            if bool(d) == True:
                l.append(d)
        df_telep = pd.DataFrame(l)
    return df_telep

def wikidownload_szavak():
    """
    magyar főnevek letöltése
    :return: magyar főnevek listája, dataframe
    """
    base_url_t = "https://hu.wiktionary.org/wiki/Index:Magyar/"
    pagelist = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "w", "s", "t", "u","v", "x", "y", "z", "ö", "ő", "é", "ü", "ű", "ú"]

    l = []
    l2 = []
    for page in pagelist:
        url = str(base_url_t + str(page))
        print(url)
        r = requests.get(url)
        c = r.content
        soup = bs4.BeautifulSoup(c, "html.parser")
        out = soup.find_all("div", {"class": "mw-parser-output"})

        for item in out:
            try:
                lista = item.find_all("p")
                for item2 in lista:
                    try:
                        nd = item2.find_all("a")
                        try:
                            for item3 in nd:
                                d = {}
                                nd2 = item3.text
                                d["valid_words"] = nd2
                                if d:
                                    d["valid_words"] = str(nd2).capitalize()
                                    l.append(d)
                        except:
                            pass
                    except:
                        pass
            except:
                pass
    df_valid = pd.DataFrame(l)
    df_valid.drop_duplicates(keep="first", inplace=True)
    return df_valid


def wikidownload_tulnev():
    """
    magyar tulajdonnevek listája
    :return: magyar tulajdonnevek listája, dataframe
    """
    pagelist = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "w", "s", "t", "u","v", "x", "y", "z", "ö", "ő", "é", "ü", "ű", "ú"]
    base_url_t = "https://hu.wiktionary.org/wiki/F%C3%BCggel%C3%A9k:Magyar_tulajdonnevek/"

    df_valid_tn = pd.DataFrame()
    l = []
    l2 = []
    for page in pagelist:
        url = str(base_url_t + str(page))
        print(url)
        r = requests.get(url)
        c = r.content
        soup = bs4.BeautifulSoup(c, "html.parser")
        out = soup.find_all("div", {"class": "mw-parser-output"})
        for item in out:
            try:
                lista = item.find_all("p")[0].find_all("a")
                for item2 in lista:
                    d = {}
                    szo = item2.text
                    d["valid_words"] = szo
                    if d:
                        d["valid_words"] = str(szo).capitalize()
                        l.append(d)
            except:
                pass
    df_valid_tn = pd.DataFrame(l)
    df_valid_tn.drop_duplicates(keep="first", inplace=True)
    return df_valid_tn


def telep_start_mapper(telep, telep_to_map, position):
    """
    maps the selected settlements to the map
    :param telep: list of all available settlements
    :param telep_to_map: selected settlements to plot
    :param position: where to search for the telep_to_map in the telep list - starts/ends/contains
    :return: subselect of the map, limited to the selected settlements
    """
    out = []
    telep_list = list(telep["TELNEV"])
    for kiv in telep_to_map:
        for tel_nev in telep_list:
            d = {}
            if position == "starts":
                if tel_nev.startswith(kiv.capitalize()):
                    d["valid_start"] = kiv.capitalize()
                    d["telepnev"] = tel_nev
                    if d:
                        out.append(d)

            if position == "ends":
                if tel_nev.endswith(kiv.lower()):
                    d["valid_start"] = kiv.lower() #'_'+
                    d["telepnev"] = tel_nev
                    if d:
                        out.append(d)

            if position == "contains":
                if tel_nev.__contains__(kiv.lower()):
                    d["valid_start"] = kiv.lower() #'_'+
                    d["telepnev"] = tel_nev
                    if d:
                        out.append(d)

    mapped_telep = pd.DataFrame(out)
    print("telep kész")
    return mapped_telep



#########depeciated
def telep_info(telep):
    out=[]
    out2=pd.DataFrame()
    results_df = pd.DataFrame(None)
    results_df_e = pd.DataFrame(None)

    for index, row_table in telep.iterrows():
        for i in range(0,len(row_table["TELNEV"])):
            kb = row_table["TELNEV"][0:i+1]
            out_list = [row_table["TELNEV"], kb, len(kb)]
            fetch_series = pd.Series(out_list)
            results_df = results_df.append(fetch_series, ignore_index=True)
    results_df.columns=['fullname','starts','lvls']
    freq = results_df['starts'].unique()

    #ends
    for index, row_table in telep.iterrows(): #loop for countries
        for i in range(0,len(row_table["TELNEV"])):
            kb = row_table["TELNEV"][(len(row_table["TELNEV"])-1)-i:]
            out_list = [row_table["TELNEV"], kb, len(kb)]
            fetch_series = pd.Series(out_list)
            results_df_e = results_df_e.append(fetch_series, ignore_index=True)
    results_df_e.columns=['fullname','ends','lvls']
    freqe = results_df_e['ends'].unique()


    freq2 = results_df.groupby('starts')[['starts']].count()
    freq2.columns=['cnts_start']
    freq2.reset_index(inplace=True, drop=False)

    freqe = results_df_e.groupby('ends')[['ends']].count()
    freqe.columns=['cnts_end']
    freqe.reset_index(inplace=True, drop=False)

    app = pd.merge(results_df, freq2, on='starts')
    app2 = pd.merge(results_df_e, freqe, on ='ends')
    df_telep_map = pd.merge(app, app2, on='fullname')

    return df_telep_map