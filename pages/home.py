import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import haversine_distances
from math import radians
import time
st.write("homeee")
# Sidebar setup
st.sidebar.title('Sidebar')
with st.sidebar:
    upload_file = st.sidebar.file_uploader('Upload a file containing earthquake data')

    # Check if file has been uploaded
    if upload_file is not None:
        df = pd.read_csv(upload_file)
        st.session_state['df'] = df;
    for key in st.session_state.keys():
        if key=='df':
            df=st.session_state['df'];
            lf=df.head();
            st.write(lf);
# # Create two dataframes with city names and lat-long in degrees
# locations_A = pd.DataFrame({
#     'city_A' :     ['Atlanta', 'Aspen', 'Albuquerque', 'Ann Arbor'],
#     'latitude_A':  [ 33.75,     39.19,   35.08,         42.28],
#     'longitude_A': [ -84.39,    -106.82, -106.65,       -83.74]
# })
# locations_B = pd.DataFrame({
#     'city_B':      ['Boston', 'Baltimore', 'Berkley', 'Bellevue'],
#     'latitude_B' : [ 42.36,    39.29,       37.87,     47.61],
#     'longitude_B': [ -71.06,   -76.61,      -122.27,   -122.20]
# })

# # add columns with radians for latitude and longitude
# locations_A[['lat_radians_A','long_radians_A']] = (
#     np.radians(locations_A.loc[:,['latitude_A','longitude_A']])
# )
# locations_B[['lat_radians_B','long_radians_B']] = (
#     np.radians(locations_B.loc[:,['latitude_B','longitude_B']])
# )


# dist = sklearn.neighbors.DistanceMetric.get_metric('haversine')
# dist_matrix = (dist.pairwise
#     (locations_A[['lat_radians_A','long_radians_A']],
#      locations_B[['lat_radians_B','long_radians_B']])*3959
# )
# # Note that 3959 is the radius of the earth in miles
# df_dist_matrix = (
#     pd.DataFrame(dist_matrix,index=locations_A['city_A'], 
#                  columns=locations_B['city_B'])
# )


# # Unpivot this dataframe from wide format to long format.
# # When you unpivot, the data in the pivot table becomes a
# # column named 'value'. Rename this column to 'miles' for clarity.
# df_dist_long = (
#     pd.melt(df_dist_matrix.reset_index(),id_vars='city_A')
# )
# df_dist_long = df_dist_long.rename(columns={'value':'miles'})
# More Table Styling
def color_surplusvalue(val):
    if str(val) == '0':
        color = 'azure'
    elif str(val)[0] == '-':
        color = 'pink'
    else:
        color = 'green'
    return 'background-color: %s' % color

heading_properties = [('font-size', '16px'),('text-align', 'center'),
                    ('color', 'black'),  ('font-weight', 'bold'),
                    ('background', 'white'),('border', '1.2px solid')]

cell_properties = [('font-size', '16px'),('text-align', 'center'),('color', 'black')]

dfstyle = [{"selector": "th", "props": heading_properties},
            {"selector": "td", "props": cell_properties}]

# Expander Styling
st.session_state['line']=""
def distance(geo,location1):
    location1_radian = [radians(_) for _ in location1]
    location2 = [geo.Latitude, geo.Longitude]
    location2_radian = [radians(_) for _ in location2]
    result = haversine_distances([location1_radian, location2_radian])
    # st.write(result)
    result = result * 6371000/1000  # multiply by Earth radius to get kilometers
    # st.write(result)

    return result[0][1]

newdf = pd.DataFrame({
    'Name': ['TVM', 'COCHIN', 'DELHI'],
    'Latitude': [8.524139, 	9.931233, 	28.644800],
    'Longitude':[76.936638, 76.267303, 77.216721],
    'Distance':[0,0,0]
})
my_location=pd.DataFrame({
    'Place':['adoor','kayamkulam','alappuzha'],
    'Latitude':[9.152967,9.171331,9.496963],
    'Longitude':[76.735611,76.501497,76.331908]
})
st.write(newdf)
newdf['Distance']=[distance(newdf.iloc[i],[9.16989, 76.503159]) for i in range(len(newdf))]
st.write(":heavy_minus_sign:" * 74)
st.subheader("Updated with :blue[distance] ")
st.write(newdf);
styler_mostsimilar = (newdf.style
            .set_properties(**{'background': 'azure', 'border': '1.2px solid'})
            .hide(axis='index')
            .set_table_styles(dfstyle)
            .applymap(color_surplusvalue, subset=pd.IndexSlice[:, ['Distance']])
            )                                                  
st.table(styler_mostsimilar)
minValue = newdf['Distance'].min();
st.write(minValue);
minValueName=newdf.query('Distance==@minValue')['Name'].values[0];
st.write(minValueName);

st.write("The nearest place is   ",minValueName)
# distanceDf=newdf
# # distanceDf = distanceDf.assign(Product=lambda x: (x['Latitude'] * x['Longitude']))
# st.write(distanceDf)
# st.write(newdf.iloc[0])
# distance(newdf.iloc[0])
# distanceDf=distanceDf.assign(Distance = lambda x: (distance(x)))
# st.write(distanceDf)
my_location=pd.DataFrame({
    'Place':['adoor','kayamkulam','alappuzha'],
    'Latitude':[9.152967,9.171331,9.496963],
    'Longitude':[76.735611,76.501497,76.331908]
})
my_location['Distance']=[distance(my_location.iloc[i],[9.931233,76.267303]) for i in range(len(newdf))]
print(my_location.head());
line="i am moving to kochi";
t = st.empty()
t.write(st.session_state['line'])
for ind in my_location.index:
  print(my_location['Place'][ind]);
  time.sleep(2)
  place,lat,lon,distance=my_location['Place'][ind],my_location['Latitude'][ind],my_location['Longitude'][ind],my_location['Distance'][ind]
#   st.write("I am currently at ",place,"   ",distance.round(1)," km from kochi");
  line = "I am currently at "+place+"   "+str(distance.round(1))+" km from kochi";
  print(line)
  st.session_state['line']=line;
  t.write(st.session_state['line'],key="line")
