import pandas as pd
import os
from datetime import datetime
import re
from calendar import monthrange


class WraDataProcess:
    def __init__(self, filePath, fileName, outputName, timestep):
        self.filePath = filePath
        self.fileName = fileName
        self.outputName = outputName
        self.timestep = timestep
        self.file = None
        self.stNameList = None
        self.stIndexList = None
        self.readfile(filePath, fileName)
        self.fileManipulate()

    def timer(self, outputFile, timestep):
        if timestep == "hour":
            # start date
            startDate = re.split("/| ", outputFile["觀測日期"].iloc[0])
            start = pd.Timestamp(
                year=int(startDate[0]),
                month=int(startDate[1]),
                day=int(startDate[2]),
                hour=0,
            )

            # end date
            endDate = re.split("/| ", outputFile["觀測日期"].iloc[-1])
            end = pd.Timestamp(
                year=int(endDate[0]),
                month=int(endDate[1]),
                day=int(endDate[2]),
                hour=23,
            )

            dateRange = pd.date_range(start=start, end=end, freq="D")
            dateRangeList = [i.strftime("%Y/%#m/%#d 上午 12:00:00") for i in dateRange]
            dateRangeIndex = pd.date_range(start=start, end=end, freq="H")

            return dateRangeList, dateRangeIndex

        elif timestep == "day":
            # start year
            startYear = outputFile["年份"].iloc[0]
            startMonth = outputFile["月份"].iloc[0]
            start = pd.Timestamp(year=int(startYear), month=int(startMonth), day=1)

            # end year
            endYear = outputFile["年份"].iloc[-1]
            endMonth = outputFile["月份"].iloc[-1]
            endDay = monthrange(endYear, endMonth)[1]
            end = pd.Timestamp(year=int(endYear), month=int(endMonth), day=endDay)

            # 1. 建立一個date range, 以月為單位
            # 2. 將每月的天數算出來 ： monthRangeList
            dateRange = pd.date_range(start=start, end=end, freq="M")
            monthRangeList = [monthrange(i.year, i.month)[1] for i in dateRange]
            dateRangeIndex = pd.date_range(start=start, end=end, freq="D")

            return dateRange, monthRangeList, dateRangeIndex

        else:
            raise "timesep must be 'hour' or 'day'"

    def readfile(self, filePath, fileName):
        os.chdir(filePath)
        rawFile = pd.read_csv(fileName, encoding="BIG5")
        file = rawFile.replace(["無雨", "缺測"], [0, -9999])

        stNameList = [i.strip() for i in file.drop_duplicates(subset="站名")["站名"]]
        stIndexList = [i for i in file.drop_duplicates(subset="站名").index] + [len(file)]

        self.file = file
        self.stNameList = stNameList
        self.stIndexList = stIndexList

    def fileManipulate(self):
        dataDict = {}
        if self.timestep == "hour":
            dateRangeList, dateRangeIndex = self.timer(self.file, self.timestep)
            for i, stName in enumerate(self.stNameList):
                outputfile = self.file.iloc[
                    self.stIndexList[i] : self.stIndexList[i + 1]
                ].reset_index(drop=True)

                tempDict = {}
                dataList = []
                num = 0
                for date in dateRangeList:
                    if date == outputfile["觀測日期"].iloc[num]:
                        for hr in range(24):
                            data = float(outputfile.iloc[num, 4 + hr])
                            dataList.append(data)
                        num += 1
                    else:
                        for hr in range(24):
                            data = -9999
                            dataList.append(-9999)
                dataDict[stName] = dataList
                tempDict[stName] = dataList
                tempDF = pd.DataFrame(tempDict, index=dateRangeIndex)
                tempDF.to_csv(stName + ".csv", encoding="BIG5")

        if self.timestep == "day":
            dateRange, monthRangeList, dateRangeIndex = self.timer(
                self.file, self.timestep
            )
            for i, stName in enumerate(self.stNameList):
                outputfile = self.file.iloc[
                    self.stIndexList[i] : self.stIndexList[i + 1]
                ].reset_index(drop=True)

                tempDict = {}
                dataList = []
                num = 0
                for i, date in enumerate(dateRange):
                    year = date.year
                    month = date.month
                    if (
                        year == outputfile["年份"].iloc[num]
                        and month == outputfile["月份"].iloc[num]
                    ):
                        for day in range(monthRangeList[i]):
                            data = float(outputfile.iloc[num, 5 + day])
                            dataList.append(data)
                        num += 1
                    else:
                        for day in range(monthRangeList[i]):
                            data = -9999
                            dataList.append(-9999)
                dataDict[stName] = dataList
                tempDict[stName] = dataList
                tempDF = pd.DataFrame(tempDict, index=dateRangeIndex)
                tempDF.to_csv(stName + ".csv", encoding="BIG5")

        # export total dataframe
        totalDF = pd.DataFrame(dataDict, index=dateRangeIndex)
        totalDF.to_csv(self.outputName, encoding="BIG5")


if __name__ == "__main__":
    flag1 = True
    while flag1:
        filePath = input("File Path: ")
        if os.path.exists(filePath):
            flag1 = False
        else:
            print("Path does't exist, please enter an existing path")
    print("")
    print("")
    print(
        "---------------------------------------------------------------------------------"
    )

    flag2 = True
    while flag2:
        fileName = input(
            "File Name, enter complete file name included filename extension (Only Accept csv): "
        )
        if not fileName.endswith(".csv"):
            print("File name must included filename extension .csv")
        elif not os.path.isfile(os.path.join(filePath, fileName)):
            print("File does't exist, please enter an existing file")
        else:
            flag2 = False
    print("")
    print("")
    print(
        "---------------------------------------------------------------------------------"
    )

    flag3 = True
    while flag3:
        outputName = input(
            "File Output Name, enter complete file name included filename extension (Only Accept csv): "
        )
        if not outputName.endswith(".csv"):
            print("Output file name must included filename extension .csv")
        else:
            flag3 = False
    print("")
    print("")
    print(
        "---------------------------------------------------------------------------------"
    )

    flag4 = True
    while flag4:
        timestep = input("day or hour: ")
        if timestep == "day" or timestep == "hour":
            flag4 = False
        else:
            print("timestep must be day or hour")

    run = WraDataProcess(
        filePath=filePath, fileName=fileName, outputName=outputName, timestep=timestep
    )
