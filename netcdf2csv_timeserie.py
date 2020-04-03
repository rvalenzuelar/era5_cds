"""
	Convert NetCDF file to CSV

	Raúl Valenzuela
	Universidad de O'Higgins
	Instituto de Cs. de la Ingeniería
	2020

"""

import xarray as xr
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

iname = filedialog.askopenfilename()
oname = iname.replace('nc','csv')

ds = xr.open_dataarray(iname)
df = ds.to_dataframe()
df.to_csv(oname)

input('Press any key to exit')
