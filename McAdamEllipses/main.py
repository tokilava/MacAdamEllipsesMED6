import numpy as np
from matplotlib import patches
import cv2
import matplotlib.pyplot as plt
import pandas as pd
import os
import csv
import scipy.stats as stats

"""
xColumn = []
yColumn = []
AngleColumn = []
PointColumn = []
x1Column = []
y1Column = []


# Open the respective file that you want to clean up.
with open('Test30.txt', 'r') as f:
    # Create a CSV reader object
    reader = csv.reader(f)
    # Initialize the data list
    data = []
    # Loop over the rows in the CSV file
    for row in reader:
        # Check if the row is invalid
        if row[0] == "Data Invalid Error!": #sometimes in the raw datasets there is a row with "Data Invalid Error!" skip those.
            continue
        # Extract the values for x, y, Angle, Point, x1, and y1
        label = (row[0].split(":")[0].strip())
        thisData = (row[0].split(":")[1].strip())

        if label == "x":
            xColumn.append(thisData)
        if label == "y":
            yColumn.append(thisData)
        if label == "Angle":
            AngleColumn.append(thisData)
        if label == "Point":
            PointColumn.append(thisData)
        if label == "x1":
            x1Column.append(thisData)
        if label == "y1":
            y1Column.append(thisData)
    dataset =  ({'x': xColumn,
                 'y': yColumn,
                 'Angle': AngleColumn,
                 'Point': PointColumn,
                 'x1': x1Column,
                 'y1': y1Column
    })
    df = pd.DataFrame(dataset)
    df.to_csv('Test30Re1', sep=',', index=False)    #Create a new file with the cleaned up data.




targetXY = [(0.3,0.3), (0.4, 0.4), (0.35,0.42)]
targetAngle = 0

# Initialize the variables we are going to use for matching conditions.
totalPoints = 0
count = 0
totalx1 = 0
totaly1 = 0

#Loop through the test coordinates and set the x and y for the color center being tested on
for testCoordinates in targetXY:
    targetx = testCoordinates[0]
    targety = testCoordinates[1]
    targetAngle = 0
    print("Current test coordinates", targetx, targety)
        # Open the file and read its contents
    while (targetAngle < 316):
        with open('AllMales.txt', 'r') as f:
            reader = csv.reader(f)
            next(reader) # skip the header
            for row in reader:  #looping through all the rows of the dataset and setting the x,y angle etc. for that row
                x = float(row[0])   #set the values of the row to their respective values
                y = float(row[1])
                angle = int(row[2])
                point = float(row[3])
                x1 = float(row[4])
                y1 = float(row[5])

                # Check if the current row matches the conditions set, if x1 is larger than 1 or negative, we now that there was an error input, and therefore do not include those
                if x == targetx and y == targety and angle == targetAngle and x1 < 1 and y1 < 1 and x1 > 0 and y1 > 0:
                    totalPoints += point
                    totalx1 += x1
                    totaly1 += y1
                    count += 1

        # Calculating the average for Point, x1 and y1
        if count > 0:
            averagePoint = totalPoints / count
            meanx1 = totalx1 / count
            meany1 = totaly1 / count
            #we print out the average values, and then manually paste them into a new txt file.
            print(targetx, ",", targety, ",", targetAngle, ",", averagePoint, ",", meanx1, ",", meany1 )
            count = 0

        #Reset the points and increase the angle with 45 degrees
        totalPoints = 0
        totalx1 = 0
        totaly1 = 0
        targetAngle = targetAngle + 45
        

"""


rawSUSScore = []
calculatedSUSScore = []
originalData = 'dataset.txt'
pilotData = 'pilotdataset.txt'
SUSList = (originalData, pilotData)
originalDataMean = 0.0
originalDataSTD = 0.0
pilotDataMean = 0.0
pilotDataSTD = 0.0
counter = 1
calculatedSUSOriginal = []
calculatedSUSPilot = []

for item in SUSList:
    with open(item, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip the first row
        for row in reader:
            rawSUSScore.append(                         #Calculating a SUSscore requires each even answer to subtract 5 from, and each uneven answer to subtract 1 from
                int(row[0]) - 1 + (5 - int(row[1])) +
                int(row[2]) - 1 + (5 - int(row[3])) +
                int(row[4]) - 1 + (5 - int(row[5])) +
                int(row[6]) - 1 + (5 - int(row[7])) +
                int(row[8]) - 1 + (5 - int(row[9]))
            )
    for i in range(len(rawSUSScore)):
        calculatedSUSScore.append(rawSUSScore[i] * 2.5) #Lastly we add 2.5 to the calculated SUSscores we have just calulated above
    newMean = np.mean(calculatedSUSScore)               #Find the mean calculated SUS score
    std = np.std(calculatedSUSScore)                    #Find the standard deviation of the calulated SUS score
    if counter == 1:
        originalDataMean = newMean
        originalDataSTD = std
        calculatedSUSOriginal = calculatedSUSScore[:]     #We use the slice operator to create copies of calculatedSUSScore because otherwise it would be wiped clear and the list would be empty
        print("Calculated SUS score for final test:", originalDataMean, "STD for the SUS score:", originalDataSTD)
    if counter == 2:
        pilotDataMean = newMean
        pilotDataSTD = std
        calculatedSUSPilot = calculatedSUSScore[:]   #We use the slice operator to create copies of calculatedSUSScore because otherwise it would be wiped clear and the list would be empty
        print("Calculated SUS score for pilot test:", pilotDataMean, "Std for the SUS score:", pilotDataSTD)
    rawSUSScore.clear()
    calculatedSUSScore.clear()
    std = 0.0
    counter += 1



def calculateVariables(file):
    data = pd.read_csv(file)
    if file == 'MeanFemales.txt':
        color = (1,0,0)     #Set the ellipse to be a red color if its a female
    else:
        color = (0,0,1)     #Set the ellipse to be a blue color if its male
    data1 = data[(data["x"] == 0.3) & (data["y"] == 0.3)]       #split the dataset according to their center points
    data2 = data[(data["x"] == 0.35) & (data["y"] == 0.42)]
    data3 = data[(data["x"] == 0.4) & (data["y"] == 0.4)]
    dataList = [data1,data2, data3]
    for i in dataList:
        currentDataSet = i
        newPoints = currentDataSet[['x1', 'y1']].to_numpy().astype(np.float32)  #make an array out of all the points. Input for cv2.fitEllipse needs to be a 32-bit floating integer so we convert to that
        ellipse = cv2.fitEllipse(newPoints)     #we fit an ellipse to the datapoints called "newPoints"
        _, (lengthMajor, LengthMinor), angle = ellipse   #from the fitted ellipse we can gather the center, length major and lengt minor and the angle rotation of the ellipse. (We dont use the center, because we already have a center for the colorcenter we are testing)
        colorCenter = currentDataSet[['x', 'y']].to_numpy()   #gather the center of the ellipse from the data set, this is an array of 8 center points
        colorCenter = colorCenter[0, :]                         #we dont need 8 datapoints for the center, since it never changes, so we slice the first row and use that as input
        currentEllipse = patches.Ellipse((colorCenter), lengthMajor, LengthMinor,   #we create an ellipse from the arguments(centerpoint, lengt major and length minor and lastly the angle of rotation)
                                                 angle=angle, linewidth=1, fill=False, zorder=2, edgecolor=color)
        axes.add_patch(currentEllipse)      #add the ellipse to the figure



if __name__ == "__main__":
    figure = plt.figure()   #create a figure object
    axes = figure.add_subplot(111, aspect='auto')
    axes.set_xlim([0, 1])
    axes.set_ylim([0, 1])
    calculateVariables('MeanMales.txt')
    calculateVariables('MeanFemales.txt')
    plt.show()
