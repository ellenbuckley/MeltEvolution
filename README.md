![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)
# Melt Evolution

## Background

<img align="right" width="120" height="120" alt="image" src="https://user-images.githubusercontent.com/61250972/211591458-e8dac618-5ecf-4fc2-8d6c-edb28ea3e280.png">

The Melt Evolution assets provide users with tools to conduct melt pond classification based on Sentinel-2 imagery using  a Python framework. The code and results of this project are a result of *insert inforamtion about paper here* (Buckley et al., 2023). Previous methods (Buckley et al., 2020) were adjusted to include the near infrared (NIR) channel to further distinguish water and ice using the Normalized Difference Water Index (NDWI). 

$$NDWI=\frac{Green-NIR}{Green+NIR} $$
<p align="center">
  <img width="800" alt="image" src="https://user-images.githubusercontent.com/61250972/205079295-0835948f-f8ea-4abb-a386-55f2bf6ea614.png">
    <br>
    <em>Fig 1. Classification of Sentinel-2 imagery at -114.0° W, 80.5° N on July 21, 2020. Sentinel-2 True Color Image (TCI) complex (left) and classification results (right), (Buckley et al., 2020). </em>
</p>

The melt-pond classification assets are broken into several scripts to aid users step-by-step through data acquisition, processing, classification, and analysis. An in-depth explanation will be provided in the next section. The classification script is where most of the processing will be conducted combined with a end output. The classification procedures are briefly illustrated:

1. Reading in land masks to remove land pixels.
2. Removing image border pixels.
3. Determining ice pixels.
4. Determining water pixels.
5. Seperating open water and melt pond pixels.
6. Combining results into an HDF output.

Examples of these processing steps will be provided in the subsequent 'Examples' section.

## Assets

This GitHub repository features 5 scripts provided in the Jupyter Notebook format. Each script handles a specific function in the processing stream. Users should run each script in the order provided below.

### 1. [Sentinel-API_Query](https://github.com/JaeminEun/MeltEvolution/blob/main/Sentinel-API_Query.ipynb) 

This script provides users with Sentinel-2 data acquisition. This program retrieves imagery over a user-defined region (geojson) using the Sentinel API. To access the imagery, users will have to create an account through the Sentinel Open Access Hub. Users can change download parameters such as regions, dates, instruments, products, and cloud cover as needed.

```python
products = api.query(footprint,
                     date=('20200901', date(2020, 9, 4)), # Note differences in date format 
                     platformname='Sentinel-2',
                     producttype='S2MSI1C',
                     cloudcoverpercentage=(0, 10)) # Cloud cover paramters can be changed based on user preference
```

For additional details, please refer to the Sentinelsat documentation: https://sentinelsat.readthedocs.io/en/stable/.

### 2. [S2_FileUnzipAndMove](https://github.com/JaeminEun/MeltEvolution/blob/main/S2_FileUnzipAndMove.ipynb)

Downloads from the Sentinel-API are provided as .zip files with various sub-directories including imagery files (.jp2) and ancillary data. These downloads include all 13 bands from the Sentinel-2 instruments including an additional 'TCI' (True Color Image) file (14 total files). The melt pond classification only requires 4 bands: B02 (Red), B03 (Green), B04 (Blue), B08 (NIR). To process these bands, the 'S2_FileUnzipAndMove' script programatically unzips files and retrieves the relevant bands into individual directories. This script includes processing for the TCI files for users who may wish to verify classification results with the corresponding optical scene. Users who do not require TCI composites may simply remove the 'TCI' phrase in the iterated lists within the script.    

<p align="center">
  <img width="717" alt="image" src="https://user-images.githubusercontent.com/61250972/213506808-db92fdf6-11f4-4e21-84ad-6ae7a03faa59.png">
    <br>
    <em>Fig 2. Users who do not require the 'TCI' complex may remove this keyword argument in the script. </em>
</p>

### 3. [S2_Classification](https://github.com/JaeminEun/MeltEvolution/blob/main/S2_Classification.ipynb)

The image classifcation script processes Sentinel-2 tiles and classifies them following the algorithm described in Buckley et al. (2020, 2023). First, the land is masked from the Sentinel-2 tiles border identified. Next, the image enters the classifcation routine. The first step separates non-water and water pixels utilizing the knowledge that water is much more absorptive in infrared wavelengths than non water pixels. From here, the non-water pixels are classified as either "ice" or "other." The "other" category includes mixed pixels, or pixels containing more than one surface type, and other surfaces that are not very absorptive in the infrared and not as bright as ice in the red channel, e.g. newly formed ice. The pixels identified as water, are separated into open water and melt pond categories depending on their brightness in the blue channel. Melt ponds are lighter in color with higher reflectance values in the blue channel than open water. A full description of the algorithm with figures demonstrating each step can be found in Buckley et al., 2020. The addition of the near infrared channel into the analysis is discussed in Buckley et al., 2023.

The count of the number of pixels in each cateogry is logged to a text file ('results.txt'). The errors and warnings are recorded in a log file ('errorlog.txt'). An array, the shape of the Sentinel-2, records classification values for each pixel where 0= border/land, 1= ice, 2= open water, 3= melt pond, 4= other. This mask is saved to an hdf file, with other attributes including the sea ice concentration (SIC) and melt pond fraction (MPF) for the tile. The hdf5 file is stored in a separate folder 'classification_hdf' that will be created if it does not exist. The 'UsefulAssets' notebook has a tool (1. Assigning projection information for classified HDF files) that converts this hdf file to a georeferenced figure.  

### 4. [S2_Results_Analysis](https://github.com/JaeminEun/MeltEvolution/blob/main/S2_Results_Analysis.ipynb)

This notebook reads in the results file, 'results.txt', created in the S2_Classification notebook. The text file is read into a pandas dataframe and new columns are added that calculate MPF and SIC. We create a day of year "DOY" column for easy plotting. Then we show an example of a way to look at the parameters. We plot MPF versus time showing the five-day running statistics including median and interquartile range.

<p align="center">
  <img width="717" alt="image" src="https://user-images.githubusercontent.com/61250972/213509347-0af37a46-20a4-46c2-94e3-086c3ab1f8c6.png">
    <br>
    <em>Fig 3. Melt Pond Fraction (MPF) statistical outputs. </em>
</p>


### 5. [UsefulAssets](https://github.com/JaeminEun/MeltEvolution/blob/main/UsefulAssets.ipynb)

The 'UsefulAssets' notebook contains 3 functions which may aid users in comparing classification outputs as well as verifying results.

1. Assigning projection information for classified HDF files
2. Mosaic function for different classification/imagery types
3. Calculating Melt Pond Fraction (MPF) and Sea-Ice Concentration (SIC)

Conversion assets (1. and 2.) run off of GDAL tools. Coordinate extents may differ for users depending on their preferred GIS and the following figure has been provided to aid users in finding the correct order for extents.

<p align="center">
  <img width="900" alt="image" src="https://user-images.githubusercontent.com/61250972/213551632-c694edcc-e815-43ce-9bb1-740cc353bb02.jpeg">
    <br>
    <em>Fig 4. Order of spatial extent coordinates for projection conversion. </em>
</p>



## Examples

### 1. Text File Outputs

Numerical results from the classification script are logged as .txt files. These files are then passed into the *'S2_Results_Analysis'* script where key metrics such as Melt Pond Fraction (MPF) and Sea Ice Concentration (SIC) are calculated. 

<p align="center">
  <img width="675" alt="image" src="https://user-images.githubusercontent.com/61250972/213793942-cfe4fe68-8308-4d56-9df5-875e779b1173.png">
    <br>
    <em>Fig 5. Text file output from the classification script. </em>
</p>

### 2. MPF/SIC CSV Output Metrics

The *'S2_Results_Analysis'* script passes the previous .txt file into pandas dataframes and produces calculations of key metrics from the melt pond classification. Metrics are broken by pixel counts of specific classes as well as percent content of Melt Pond Fraction (MPF) and Sea Ice Concentration (SIC).

<p align="center">
  <img width="900" alt="image" src="https://user-images.githubusercontent.com/61250972/213751846-f0494c78-f9bc-4aba-aa9d-35941a0510ad.png">
    <br>
    <em>Fig 6. Example of MPF/SIC metrics processed as a .csv file. </em>
</p>

### 3. Classification Outputs

The *'S2_Classification'* script stages outputs in an HDF file. The HDF files include descriptions of key variables as well as brief summary metrics. 

<p align="center">
  <img width="900" alt="image" src="https://user-images.githubusercontent.com/61250972/213754758-4e5fb5f7-d674-46d1-8228-4cd74a5f4bbb.png">
    <br>
    <em>Fig 7. HDF classification results with variable descriptions. </em>
</p>

HDF outputs that have been georefferenced can be easily viewed within a GIS. The following is an example classification.

<p align="center">
  <img width="900" alt="image" src="https://user-images.githubusercontent.com/61250972/213785477-4ecc4fbe-d882-4a55-bd75-fb8f3a624bc5.jpg">
    <br>
    <em>Fig 8. Classification results converted to .tif format overlaid on the corresponding Sentinel-2 TCI complex. This classification features landmasking and only includes results in regions of sea-ice. </em>
</p>

### Acknowledgements 

This study is supported under NASA Cryosphere Program Grants 80NSSC17K0006, 80NSSC20K0966 and 80NSSC22K0815 (PI: Sinéad Farrell) and by the U.S. National Aeronautics and Space Administration (NASA) Earth Sciences Division under awards 80NSSC20K0975, 80NSSC22K1155, 80NSSC18K1439 and NNX17AG75G (PI: Ute Herzfeld). We acknowledges support from NASA’s New Investigator Program in Earth Science (80NSSC20K0658) and  the National Science Foundation (2138786) (PI: Melinda Webster). WorldView geospatial support for this work provided by the Polar Geospatial Center under NSF-OPP awards 1043681 and 1559691.

### References
Buckley, E. M., Farrell, S. L., Duncan, K., Connor, L. N., Kuhn, J. M., & Dominguez, R. T. (2020). Classification of sea ice summer melt features in high‐resolution IceBridge imagery. Journal of Geophysical Research: Oceans, 125(5), e2019JC015738. https://doi.org/10.1029/2019JC015738
Buckley, E. M., Farrell, S. L., Herzfeld, U. C., Webster, M., Trantow, T., Baney, O. N., Duncan, K., Han, H., Lawson, M. (2023). Observing the Evolution of Summer Melt on Multiyear Sea Ice with ICESat-2 and Sentinel-2 [Manuscript in Preparation]. 
