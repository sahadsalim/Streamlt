import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import haversine_distances
from math import radians

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


def distance(geo):
    location1=[0.1245, 51.685]
    location1_radian = [radians(_) for _ in location1]
    location2 = [geo.Latitude, geo.Longitude]
    location2_radian = [radians(_) for _ in location2]
    result = haversine_distances([location1_radian, location2_radian])
    st.write(result)
    result = result * 6371000/1000  # multiply by Earth radius to get kilometers
    st.write(result)

    return result[0][1]

newdf = pd.DataFrame({
    'Latitude': [-0.123684, -0.129212, -0.123234],
    'Longitude': [51.485020, 51.507426, 52.476264],
    'Distance':[0,0,0]
})
st.write(newdf)
newdf['Distance']=[distance(newdf.iloc[i]) for i in range(len(newdf))]
st.write(":heavy_minus_sign:" * 74)
st.subheader("Updated with :blue[distance] ")
# distanceDf=newdf
# # distanceDf = distanceDf.assign(Product=lambda x: (x['Latitude'] * x['Longitude']))
# st.write(distanceDf)
# st.write(newdf.iloc[0])
# distance(newdf.iloc[0])
# distanceDf=distanceDf.assign(Distance = lambda x: (distance(x)))
# st.write(distanceDf)
