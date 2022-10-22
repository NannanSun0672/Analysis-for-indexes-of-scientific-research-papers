"""
Create on June 27,2019

@author:nannan.sun

Function:

1.清洗未能够通过接口下载数据的pmid

2.进行二次数据下载

"""
import os
import sys
import pandas as pd

def pmid_clean(bug_Data_dir):
    with open(bug_Data_dir,"r") as fr:
        content = fr.readlines()
    pmid = list(set(content))
    print(len(pmid))
    with open("./Data/clean_pmid.txt","a") as fw:
        for num,id in enumerate(pmid):
            fw.write(id + "\n")



def clean_Data():
    clean_pmid_path = "./Data/clean_pmid.txt"
    excel_path = "./Data/pubmed_paper_info.xlsx"
    out_path = "./Data/clean_pmid.xlsx"
    pmid_list = list()
    with open (clean_pmid_path,"r")as fr:
        pmid = fr.readlines()
    #print(pmid)
    for id in pmid:
        if id !="\n":
            pmid_list.append(id[:-1])
    #print(pmid_list)
    Data = pd.read_excel(excel_path)
    #print(Data.head(10))
    Data_dict = Data.to_dict("list")
    #print(Data_dict)
    titles = list()
    pmids = list()
    for num,idx in enumerate(Data_dict["pmid"]):
        if str(idx) in pmid_list and idx not in pmids:
            pmids.append(idx)
            titles.append(Data_dict["title"][num])
    clean_dict = {"title":titles,"pmid":pmids}
    print(clean_dict)
    print(len(clean_dict["title"]))
    data_frame = pd.DataFrame(clean_dict)
    print(data_frame.head(10))
    data_frame.to_excel(out_path)




if __name__ =="__main__":
    #bug_Data_dir = "/Users/sunnannan/Documents/pubmed_obtained/debug_pmid.txt"
    #pmid_clean(bug_Data_dir)
    clean_Data()
