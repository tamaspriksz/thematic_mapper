
import plotter as pl

import tkinter as tk
import pandas as pd



def data_collector():

    settlement_list_get = []
    settlement_list_get.append(settlement_list_value.get())
    settlement_list.delete("1.0", tk.END)
    settlement_list.insert(tk.END, settlement_list_get)

    settlement_list_get.append(settlement_list_value2.get())
    settlement_list2.delete("1.0", tk.END)
    settlement_list2.insert(tk.END, settlement_list_get)

    position_get = position_value.get()
    position.delete("1.0", tk.END)
    position.insert(tk.END,position_get)

    detail_get = detail_value.get()
    detail.delete("1.0", tk.END)
    detail.insert(tk.END, detail_get)

    pl.map_details(telnevek=settlement_list_get, position=position_get, detail=detail_get)
    telep_to_show = pl.map_details(telnevek=settlement_list_get, position=position_get, detail=detail_get)
    out = pd.DataFrame(telep_to_show)
    list1.insert(tk.END, out)

    pl.plot_to_map(telnevek=settlement_list_get, position=position_get)

    return settlement_list_get, position_get, detail_get


window = tk.Tk()

b1 = tk.Button(window,text="Plot!", command=data_collector) #csak referálok a functionre
b1.grid(row=5, column=0) #, rowspan=2)


#labels
position=tk.Label(window,text="where to search (starts/contains/ends)")
position.grid(row=0,column=0)
position=tk.Text(window, height=1, width =20)
position_value=tk.StringVar()
position_e1 = tk.Entry(window, textvariable=position_value)
position_e1.grid(row=0, column=1)


settlement_list=tk.Label(window,text="what to search for - provide just one word")
settlement_list.grid(row=1,column=0)
settlement_list=tk.Text(window, height=1, width =20)
settlement_list_value=tk.StringVar()
settlement_list_e1 = tk.Entry(window, textvariable=settlement_list_value)
settlement_list_e1.grid(row=1, column=1)

settlement_list2=tk.Label(window,text="what to search for - provide just one word")
settlement_list2.grid(row=2,column=0)
settlement_list2=tk.Text(window, height=1, width =20)
settlement_list_value2=tk.StringVar()
settlement_list_e12 = tk.Entry(window, textvariable=settlement_list_value2)
settlement_list_e12.grid(row=2, column=1)


detail=tk.Label(window,text="Detail - yes/no")
detail.grid(row=3,column=0)
detail=tk.Text(window, height=1, width =20)
detail_value=tk.StringVar()
detail_e1 = tk.Entry(window, textvariable=detail_value)
detail_e1.grid(row=3, column=1)


list1=tk.Listbox(window, height=6,width=100)
list1.grid(row=4,column=1,rowspan=6,columnspan=2)

sb1=tk.Scrollbar(window, orient='horizontal')
sb1.grid(row=10,column=1,columnspan=6)

list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)




#ez mindenképp kell
window.mainloop()