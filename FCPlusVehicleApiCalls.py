import json
import datetime
import requests
import csv
import pandas as pd
import os, sys

def main():
    # Import the API key from the .env file in the running folder
    localFileApiKey='.env'
    with open(localFileApiKey) as enviromentFile:
        apiKey=enviromentFile.read()
    #print(apiKey)

    # Start a request on the Get vehiclesApi/Vehicles/get mehtod
    requestUrlVehicle = "https://app.ecofleet.com/seeme/Api/Vehicles/get"
    parametersRequestUrlVehicle = {
        "key" : apiKey,
        "json" : ""
    }
    response = requests.get(requestUrlVehicle, params=parametersRequestUrlVehicle)
    vehicles=response.json()
    dfVehicles = pd.json_normalize(vehicles, 'response')
    #save the full vehicle list out of the dataframe into a csv file
    currentDateAndTimeString = str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
    fileName='VehicleList '+ currentDateAndTimeString  +'.csv'
    print('Vehicle List will be saved in the file: ',fileName)
    with open(fileName, 'w') as csvfile: # Open file for export of vehilce data
        dfVehicles.to_csv(csvfile, index=False, line_terminator='\n', header=True) #write vehicle data to csv

    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    beginningTimeStamp=yesterday + ' 00:00:01+0100'
    endingTimeStamp=yesterday + ' 23:59:59+0100'
    #For every object in the vehicle list a call on the method Get vehiclesApi/Vehicles/getRawData will be started
    for oneVehicleId in dfVehicles['id'].values:
        requestUrlVehicle = "https://app.ecofleet.com/seeme/Api/Vehicles/getRawData"
        parametersRequestUrlVehicle = {
            "key" : apiKey,
            "objectId" : oneVehicleId,
            "begTimestamp" : beginningTimeStamp,
            "endTimestamp" : endingTimeStamp,  
            "json" : ""
        }
        response = requests.get(requestUrlVehicle, params=parametersRequestUrlVehicle)
        oneTempVehicle=response.json()
        dfOneTempVehicle = pd.json_normalize(oneTempVehicle, 'response')
        fileName='VehicleRawData '+ str(oneVehicleId) +' from '+ yesterday +'.csv'
        print('The raw data for vehicle ',oneVehicleId,' will be saved in the file: ' ,fileName)
        with open(fileName, 'w') as csvfile: # Open file for export of vehilce data
            dfOneTempVehicle.to_csv(csvfile, index=False, line_terminator='\n', header=True) #write vehicle data to csv

if __name__ == '__main__':
  main()