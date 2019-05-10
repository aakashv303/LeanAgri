from django.shortcuts import render
import openpyxl
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

def index(request):
    diseaseList = []
    imgList = []
    originList = []
    pestList = []
    exoticList = []
    import_path = r'C:\Users\Aakash Vaghela\Desktop\LeanAgri_Task\LeanAgri\data.xlsx'
    df = pd.read_excel(import_path, sheetname='Sheet1')
    df['Origin'] = df['Origin'].fillna("NA")
    df['Exotic'] = df['Exotic'].fillna("NA")
    df['Pest'] = df['Pest'].fillna("NA")
    for i in df.index:
        diseaseList.append(df['Disease name'][i])
        imgList.append(df['Image link'][i])
        originList.append(df['Origin'][i])
        pestList.append(df['Pest'][i])
        exoticList.append(df['Exotic'][i])
    data = zip(diseaseList, imgList, originList, pestList, exoticList)
    return render(request, 'index.html', {"data":data})
