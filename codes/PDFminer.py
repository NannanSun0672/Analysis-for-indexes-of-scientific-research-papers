"""
Create on Oct 9,2019

@author:nannan.sun

Function:

1.解析pdf，将pdf转换为tex格式

"""
import sys
import importlib
importlib.reload(sys)
import pandas as pd
#from pdfminer.pdfparser import PDFParser,PDFDocument
#from pdfminer.pdfinterp import PDFResourceManager,PDFPageInterpreter
#from pdfminer.converter import PDFPageAggregator
#from pdfminer.layout import LTTextBoxHorizontal,LAParams
#from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

"""
解析文本，保存到txt文本中

"""
path = "./Learning Semantic Textual Similarity from Conversations.pdf"
saved_path = "./Learning Semantic Textual Similarity from Conversations.txt"
def parse():
    fp = open(path,"rb")
    praser = PDFParser(fp)
    doc = PDFDocument()
    praser.set_document(doc)
    doc.set_parser(praser)
    # 提供初始化密码
    # 如果没有密码 就创建一个空的字符串
    doc.initialize()
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        #创建PDF资源管理器 来管理共享资源
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device =PDFPageAggregator(rsrcmgr,laparams=laparams)
        #创建一个pdf解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr,device)
        #循环遍历每次处理一个page内容
        for page in doc.get_pages():
            interpreter.process_page(page)
            #接受页面的LTpage对象
            layout = device.get_result()
            #这里的layout是一个LTpage对象,里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
            for x in layout:
                if (isinstance(x,LTTextBoxHorizontal)):
                    with open(saved_path,"a")as f:
                        results = x.get_text()
                        print(results)
                        f.write(results +"\n")
import camelot

pdf_table = "./Data/test_pdf/health.pdf"
saved_path = "./Data/test/health"
def table_extration():

    tables = camelot.read_pdf(pdf_table,pages="all",flavor="stream")
    print(tables)
    path = saved_path + ".csv"
    tables.export(path,f="csv",compress=False)
    print(tables[0])
    #print(tables[1].df)



if __name__ == "__main__":
    #parse()
    table_extration()





















