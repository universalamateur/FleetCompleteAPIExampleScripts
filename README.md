# FleetCompleteAPIExampleScripts
This is a collection of python scripts to collect data out of the Fleet Complete - FC Plus API

## The script FCPlusVehicleApiCalls.py
This script will call with the API key in the .env file all available vehicles.
The vehicle list will be saved into a CSV file in the running folder.
Next it will go through all thos evehicles and call the raw data of those from yesterday.
For each vehicle, if there was raw data or not, a csv file will be saved into the running folder.