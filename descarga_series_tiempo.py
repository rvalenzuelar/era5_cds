"""
    CDS script para descargar series de tiempo medias diarias de distintas
    variables de superficie en ERA5 (adatado del ejemplo de CDS).
    
    Instrucciones:
    
    - definir la variable
    - definir latitud y longitud
    - crea una figura y link de descarga
    
    Raúl Valenzuela
    Universidad de O'Higgins
    Instituto de Cs de la Ingeniería
    2020

"""


import cdstoolbox as ct

years = ['2017']

# '6h' o 'h'
daily_frequency = '6h'  

# 'daily_mean' o 'raw'
output_frequency = 'daily_mean'  

variables = {
    'Temperatura a 2m': '2m_temperature',
    'Temperatura punto rocío a 2m': '2m_dewpoint_temperature',
    'Viento 10m componente oeste': '10m_u_component_of_wind',
    'Viento 10m componente sur': '10m_v_component_of_wind',
    'Temperatura del suelo 0_7 cm': 'soil_temperature_level_1',
    'Temperatura del suelo 7_28 cm': 'soil_temperature_level_2',
    'Temperatura del suelo 28_100 cm': 'soil_temperature_level_3',
    'Temperatura del suelo 100_289 cm': 'soil_temperature_level_4',
    'Precipitación': 'total_precipitation',
}

layout = {
    'input_ncols': 3,
}

@ct.application(title='Descarga series de tiempo', layout=layout)

@ct.input.dropdown('var', label='Variable', values=variables.keys(), description='Seleccione variable')

@ct.input.text('lon', label='Longitude', type=float, default=-71.1, description='Grados decimales')

@ct.input.text('lat', label='Latitude', type=float, default=-34.6, description='Grados decimales')

@ct.output.livefigure()

@ct.output.download()

def plot_time_series(var, lon, lat):

    if daily_frequency == '6h':
        time = ['00:00', '06:00', '12:00', '18:00']
    elif daily_frequency == 'h':
        time = ['00:00', '01:00', '02:00', '03:00','04:00', '05:00',
                '06:00', '07:00', '08:00', '09:00','10:00', '11:00',
                '12:00', '13:00', '14:00', '15:00','16:00', '17:00',
                '18:00', '19:00', '20:00', '21:00','22:00', '23:00']            
    data = ct.catalogue.retrieve(
        'reanalysis-era5-single-levels',
        {
            'variable': variables[var],
            'grid': ['3', '3'],
            'product_type': 'reanalysis',
            'year': years,
            'month': [
                '01', '02', '03', '04', '05', '06',
                '07', '08', '09', '10', '11', '12'
            ],
            'day': [
                '01', '02', '03', '04', '05', '06',
                '07', '08', '09', '10', '11', '12',
                '13', '14', '15', '16', '17', '18',
                '19', '20', '21', '22', '23', '24',
                '25', '26', '27', '28', '29', '30',
                '31'
            ],
            'time': time,
        }
    )

    # Location selection

    # Extract the closest point to selected lon/lat (no interpolation).
    # If wrong number is set for latitude, the closest available one is chosen:
    # e.g. if lat = 4000 -> lat = 90.
    # If wrong number is set for longitude, first a wrap in [-180, 180] is made,
    # then the closest one present is chosen:
    # e.g. if lon = 200 -> lon = -160.
    data_sel = ct.geo.extract_point(data, lon=lon, lat=lat)

    # Daily mean on selection
    data_daily = ct.climate.daily_mean(data_sel)

    fig = ct.chart.line(data_daily)

    if output_frequency == 'daily_mean':
        output_data = data_daily
    elif output_frequency == 'raw':
        output_data = data_sel
        
    return fig, output_data
