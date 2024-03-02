**Downloads**

- Download and install Python for Windows 64 bits version 3.12.0
https://www.python.org/downloads/release/python-3120/

- Download the complete project and unzip it into a folder

**Comments**

- Ensure that the main.py and data files are at the same level, the data folder is necessary for it to work correctly

**Requirements**

Install components below preferably in virtual env:
- pip install pandas
- pip install matplotlib
- pip install folium
 
**Instructions for Run**

- Add the Details_Data.csv, Price_AV_Itapema-001.csv and VivaReal_Itapema.csv files to the "data" folder
- Run the python main.py file (ensure your root directory is before the main.py file location

**Additional Comments**
- If the Price_AV_Itapema_filtered.csv file is in the "data" folder, it will be used instead of the Price_AV_Itapema-001.csv file. 
- If you want to monitor the generation of the filtered file, remove it (Price_AV_Itapema_filtered.csv) from the folder before running main.py
- Ensure that the machine has at least 20GB of RAM available for this first run when using function *gen_filtered_price_file*
- New function called *gen_filtered_price_file_chunk* was built, it opens the price file in parts, avoiding high memory consumption, just replace function *gen_filtered_price_file* in main.py
- Ensure that the Property_profile.csv file in the data folder is not in use before running main.py

