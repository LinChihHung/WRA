from wradatacontrol.WRAdata import WraDataProcess
import os

def main(filePath, fileName, outputName, timestep):
    """
    filePath: 檔案位置
    fileName: 檔案名稱 (僅限csv檔) 例:北水局日流量.csv
    outputName: 輸出檔名 (僅限csv檔) 例:北水局日流量整理.csv
    timestep: 時資料或日資料 (hour or day)

    註: fileName 及 outputName 需包含副檔名
        timestep 僅可輸入 hour 或 day, 否則報錯
    """

    WraDataProcess(
        filePath=filePath, 
        fileName=fileName, 
        outputName=outputName, 
        timestep=timestep)
    

if __name__ == '__main__':
    """
    時流量 demo
    """
    # filePath = os.path.join(os.getcwd(), 'data', '九河局時流量')
    # fileName = '202100024_時流量.csv'
    # outputName = '九河局時流量New.csv'
    # timestep = 'hour'
    
    """
    日流量 demo
    """
    # filePath = os.path.join(os.getcwd(), 'data', '北水局日流量')
    # fileName = '北水局流量.csv'
    # outputName = '北水局流量New.csv'
    # timestep = 'day'

    # run function
    main(
        filePath=filePath, fileName=fileName, outputName=outputName, timestep=timestep
        )