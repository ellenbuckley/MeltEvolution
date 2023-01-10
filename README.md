![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)
# Melt Evolution

## Background

<img align="right" width="120" height="120" alt="image" src="https://user-images.githubusercontent.com/61250972/211591458-e8dac618-5ecf-4fc2-8d6c-edb28ea3e280.png">

The Melt Evolution assets provide users with tools to conduct melt pond classification based on Sentinel-2 imagery using  a Python framework. The code and results of this project are a result of *insert inforamtion about paper here* (Buckley et al., 2023). Previous methods (Buckley et al., 2020) were adjusted to include the near infrared (NIR) channel to further distinguish water and ice using the Normalized Difference Water Index (NDWI). 

$$NDWI=\frac{Green-NIR}{Green+NIR} $$
<p align="center">
  <img width="717" alt="image" src="https://user-images.githubusercontent.com/61250972/205079295-0835948f-f8ea-4abb-a386-55f2bf6ea614.png">
    <br>
    <em>Fig 1. Classification of Sentinel-2 imagery at -114.0° W, 80.5° N on July 21, 2020. Sentinel-2 True Color Image (TCI) complex (left) and classification results (right), (Buckley et al., 2020). </em>
</p>

The melt-pond classification assets are broken into several scripts to aid users step-by-step through data acquisition, processing, classification, and analysis. An in-depth explanation will be provided in the next section. The classification script is where most of the processing will be conducted combined with a end output. The classification procedures are briefly illustrated:

1. Reading in land masks to remove land pixels.
2. Removing image border pixels.
3. Seperating pixels between water and not water.
4. Determining ice pixels.
5. Seperating open water and melt pond pixels.
6. Combining results into an HDF output.

Examples of these processing steps will be provided in the subsequent 'Examples' section.

## Assets

This GitHub repository features 5 scripts provided in the Jupyter Notebook format. Each script handles a specific function in the processing stream. Users should run each script in the order provided below.

### 1. Sentinel-API_Query 

This script provides users with Sentinel-2 data acquisition. This program retrieves imagery over a user-defined region (geojson) using the Sentinel API. To access the imagery, users will have to create an account through the Sentinel Open Access Hub. Users can change download parameters such as regions, dates, instruments, products, and cloud cover as needed.

```python
products = api.query(footprint,
                     date=('20200901', date(2020, 9, 4)), # Note differences in date format 
                     platformname='Sentinel-2',
                     producttype='S2MSI1C',
                     cloudcoverpercentage=(0, 10)) # Cloud cover paramters can be changed based on user preference
```

For additional details, please refer to the Sentinelsat documentation: https://sentinelsat.readthedocs.io/en/stable/.

### 2. S2_FileUnzipAndMove

Downloads from the Sentinel-API are provided as .zip files with various sub-directories including imagery files (.jp2) and ancillary data. These downloads include all 13 bands from the Sentinel-2 instruments including an additional 'TCI' (True Color Image) file (14 total files). The melt pond classification only requires 4 bands: B02 (Red), B03 (Green), B04 (Blue), B08 (NIR). To process these bands, the 'S2_FileUnzipAndMove' script programatically unzips files and retrieves the relevant bands into individual directories. This script includes processing for the TCI files for users who may wish to verify classification results with the corresponding optical scene. Users who do not require TCI composites may simply remove the 'TCI' phrase in the iterated lists within the script.    

### 3. S2_Classification

### 4. S2_Results_Analysis

### 5. UsefulAssets

## Examples

### Acknowledgements 
