import json, os
import pandas as pd
import numpy as np
template = './template-files/template.json'
with open(template, 'r') as json_data:
    updated = json.load(json_data)

###################################################
png_name = 'General Chemical_006.png'
lots_to_enter = True

####

# update the metadata of the json
meta = updated['metadata']
meta['Year'] = 1942
meta['Owner'] = 'General Chemical'
meta['County'] = 'St. Claire'
# meta['Address'] = 'E. St. Louis, ILL'
meta['Well Identity'] = '#8 - No Well'
# meta['Section'] = "3"
# meta['Township'] = "2N"
# meta['Range'] = "9W"
meta['Elevation TOW'] = 435.04
meta["Datum"] = "Water Level USGS"

####

# update the timeseries data
daily = pd.DataFrame(
    {'date': pd.date_range(f"{meta['Year']}-01-01",
                          f"{meta['Year']}-12-31",
                          freq='D')}
)
daily['water level'] = None

if lots_to_enter:
    daily.to_csv('./template-files/temp-water-levels.csv', index=False)
    input('Ready to continue?')
    daily = pd.read_csv('./template-files/temp-water-levels.csv', parse_dates=['date'])
else:
    # subsitute certain days ("mm-dd", measurement)
    subs = [
        # ("01-01", 407),
        # ("01-15", 408),
        # ("01-18", 407),
        # ("04-27", 408),
        # ("05-23", 408),
        # ("06-23", 408),
        # ("07-21", 408),
        # ("08-21", 408),
        # ("09-23", 408),
        # ("09-30", 411),
        # ("10-22", 410),
        # ("11-26", 411),
        # ("11-30", 408),
    ]
    for d, t in subs:
        idx = daily['date'] == pd.to_datetime(f"{meta['Year']}-{d}")
        daily.loc[idx,'water level'] = t

# print information to the updated json
data = updated['daily_data']
if type(daily.loc[0, 'date']) == str:
    daily.loc[:, 'date'] = pd.to_datetime(daily.loc[:, 'date'])
for idx in daily.index:
    data['date'].append(daily.loc[idx, 'date'].strftime('%Y-%m-%d'))
    if daily.loc[idx, 'water level'] == None or \
            np.isnan(daily.loc[idx, 'water level']):
        data['water level'].append('null')
    else:
        data['water level'].append(daily.loc[idx, 'water level'])


####

# # check that the json has been updated as you want
# from pprint import pprint
# pprint(updated)

# save the json
output = (r'C:\Users\alljones\University of Illinois - Urbana\EStL SIC (ISWS) - General\Data\Dark Data\dark pngs\Prototype Responses') #'./output/'
if not os.path.exists(output):
    os.makedirs(output)
fileout = f'{png_name.replace(".png",".json")}'
with open( os.path.join(output, fileout), 'w') as new_json:
    json.dump(updated, new_json, indent=4)

print(f"Data successfully saved to {os.path.join(output, fileout)}")