"""
Create on  july 3, 2019

@author:nannan.sun

function

1.读取原始数据表

2.分析数据表中的影响因子分布

3.分析数据表中被引用量的分布

"""
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
class pubmed_data(object):
    def __init__(self,ori_input_path):
        self.data_info = pd.read_excel(ori_input_path)
        self.years = ["2014","2015", "2016", "2017", "2018", "2019"]
    def magazine_clean(self):
        """
        获取杂志名称数据，搜索影响因子
        :return:
        """
        magzine_name = self.data_info["Magazine"]
        magzine_name_dict = magzine_name.to_dict()
        print(len(magzine_name_dict))
        magzine_name_list = list()
        for num,name in magzine_name_dict.items():
            if name not in magzine_name_list:
                magzine_name_list.append(name)
        print(magzine_name_list)
        print(len(magzine_name_list))
        idx = [i for i in range(len(magzine_name_list))]
        print(len(idx),idx)
        magzine_name_series = pd.Series(dict(zip(idx,magzine_name_list)))
        print(magzine_name_series)
        magzine_name_series.to_excel("./Data/magine_name.xlsx")

    def Save_IF_total(self):
        """
        整合期刊影响因子到总表格中，并存储
        :return:
        """
        magazine_IF_path = "./Data/magazine_name.xlsx"
        magazine_IF_name = pd.read_excel(magazine_IF_path)
        #print(magazine_IF_name)
        magazine_IF= magazine_IF_name.ix[:,["magazine_name","min_IF","max_IF"]]
        #print(magazine_IF)
        magazine_IF_dict = magazine_IF.to_dict("list")
        #print(magazine_IF_dict)
        magazine_dict = {}
        for num,magazine_name in enumerate(magazine_IF_dict["magazine_name"]):
            magazine_dict.update({magazine_name:{"min_IF":magazine_IF_dict["min_IF"][num],"max_IF":magazine_IF_dict["max_IF"][num]}})
        #print(magazine_dict)
        data_info_dict = self.data_info.to_dict("list")
        #print('data_info_dict["Magazine"]',data_info_dict["Magazine"][278].strip("."))
        IF_dict = {"min_IF":[],"max_IF":[]}

        for num,magazine_name in enumerate(data_info_dict["Magazine"]):
            print("magazine_name",num,magazine_name.strip("."))
            IF_dict["min_IF"].append(magazine_dict[magazine_name.strip(".")]["min_IF"])
            IF_dict["max_IF"].append(magazine_dict[magazine_name.strip(".")]["max_IF"])
        print(len(IF_dict["min_IF"]))
        data_info_dict.update(IF_dict)
        print(data_info_dict)
        Data_frame = pd.DataFrame(data_info_dict)
        Data_frame.to_excel("./Data/total_info_pubmed.xlsx")
    def Analysis_IF(self):
        """
        1.分析不同年限的杂志影响因子分布-柱状图
        2.不同年限的影响因子与引用量之间的关系-折线图
        3.整体影响因子分布-柱状图

        :return:
        """
        self.pubmed_info = pd.read_excel("./Data/total_info_pubmed.xlsx")
        #print(self.pubmed_info)
        #整个数据集的IF分布
        mid_IF_dict = {"mid_IF":[]}
        IF_sections = {"0-1":[],"1-3":[],"3-5":[],"5-10":[],"10-30":[],">30":[]}
        info = self.pubmed_info.ix[:,["year","citing","min_IF","max_IF"]]
        #print(info)
        info_dict = info.to_dict("list")
        #print(info_dict)

        for num,min_if in enumerate(info_dict["min_IF"]):
            #print(num)
            if min_if != 0:
                mid_IF = (min_if + info_dict["max_IF"][num])/2
                #print("mid_IF",mid_IF)
                mid_IF_dict["mid_IF"].append(mid_IF)
            elif min_if == 0:
                mid_IF_dict["mid_IF"].append(min_if)
                #print(min_if,info_dict["max_IF"][num])

        #print("mid_IF_dict",len(mid_IF_dict["mid_IF"]))

        info_dict.update(mid_IF_dict)
        #print(info_dict)
        info_add_midif = pd.DataFrame(info_dict)
        cnt_1 = 0
        for num,mid_IF in enumerate(mid_IF_dict["mid_IF"]):

            if float(mid_IF) >= float(0) and float(mid_IF) < float(1):
                IF_sections["0-1"].append(mid_IF)

            elif float(mid_IF) >= float(1) and float(mid_IF) < float(3):

                IF_sections["1-3"].append(mid_IF)

            elif float(mid_IF) >= float(3) and float(mid_IF) < float(5):

                IF_sections["3-5"].append(mid_IF)
            elif float(mid_IF) >= float(5) and float(mid_IF) < float(10):

                IF_sections["5-10"].append(mid_IF)
            elif float(mid_IF) >= float(10) and float(mid_IF) < float(30):

                IF_sections["10-30"].append(mid_IF)
            elif float(mid_IF) >= float(30):

                IF_sections[">30"].append(mid_IF)


        IF_sections_static = {"0-1":len(IF_sections["0-1"]),"1-3":len(IF_sections["1-3"]),"3-5":len(IF_sections["3-5"]),"5-10":len(IF_sections["5-10"]),"10-30":len(IF_sections["10-30"]),">30":len(IF_sections[">30"])}
        #print(IF_sections_static)
        #####1.绘制柱状图
        #self.plot_IF_bar(IF_sections_static)
        #####2.绘制每一年的柱状图图
        info_years = {}
        info_add_midif_dict = info_add_midif.to_dict("list")
        #print(len(info_add_midif_dict["year"]))
        for num, year in enumerate(self.years):

            info_years[str(year)] = info_add_midif[info_add_midif["year"] == int(year)]
            #print(year,info_years[str(year)].shape)
        years_IF = {}
        for year,data_frame_info in info_years.items():
            if_section={"0-1":[],"1-3":[],"3-5":[],"5-10":[],"10-30":[],">30":[]}
            data_dict = data_frame_info.to_dict("list")
            #print(data_dict)
            for mid_IF in data_dict["mid_IF"]:
                if mid_IF >= 0 and mid_IF < 1:
                    if_section["0-1"].append(mid_IF)
                elif mid_IF >= 1 and mid_IF < 3:
                    if_section["1-3"].append(mid_IF)
                elif mid_IF >= 3 and mid_IF < 5:
                    if_section["3-5"].append(mid_IF)
                elif mid_IF >= 5 and mid_IF < 10:
                    if_section["5-10"].append(mid_IF)
                elif mid_IF >= 10 and mid_IF < 30:
                    if_section["10-30"].append(mid_IF)
                elif mid_IF >= 30:
                    if_section[">30"].append(mid_IF)
            #print(if_section)

            years_IF.update({year:{"0-1":len(if_section["0-1"]),"1-3":len(if_section["1-3"]),"3-5":len(if_section["3-5"]),"5-10":len(if_section["5-10"]),"10-30":len(if_section["10-30"]),">30":len(if_section[">30"])}})
        #print(years_IF)
        IF_dis = {"0-1":[],"1-3":[],"3-5":[],"5-10":[],"10-30":[],">30":[]}
        for t,value in years_IF.items():
            IF_dis["0-1"].append(value["0-1"])
            IF_dis["1-3"].append(value["1-3"])
            IF_dis["3-5"].append(value["3-5"])
            IF_dis["5-10"].append(value["5-10"])
            IF_dis["10-30"].append(value["10-30"])
            IF_dis[">30"].append(value[">30"])
        #print(IF_dis)
        self.plot_year_IF(self.years, IF_dis)
        ####3.绘制折形图
        #print(info_years)
        self.info_data_dict = dict()
        #save_path = "/Users/sunnannan/Documents/pubmed_obtained/" + "IF_citing"+ ".xlsx"
        writer = pd.ExcelWriter(save_path)
        #for year,info in info_years.items():
            #info.sort_values("mid_IF", inplace=True)
            #print(year)
            #print(info)
            ###存储排列数据
            #info.to_excel(writer,year)




            #info_dict = info.to_dict("list")

            #self.info_data_dict.update({year:info_dict})
        #print(self.info_data_dict)
        #writer.save()
        #self.plot_line_chart(self.info_data_dict)

    def plot_line_chart(self,input_Data):
        """
        绘制不同年份的影响因子与引用量之间的关系折线图
        :param input_data:
        :return:
        """
        print(input_Data)
        plt.figure()
        plt.plot(input_Data["2014"]["mid_IF"],input_Data["2014"]["citing"],color = "blue",label="2014")
        plt.legend()
        plt.xlabel('IF')
        plt.ylabel('counts for citing')
        plt.figure()
        plt.plot(input_Data["2015"]["mid_IF"], input_Data["2015"]["citing"], color="red", label="2015")
        plt.legend()
        plt.xlabel('IF')
        plt.ylabel('counts for citing')
        plt.figure()
        plt.plot(input_Data["2016"]["mid_IF"], input_Data["2016"]["citing"], color="skyblue", label="2016")
        plt.legend()
        plt.xlabel('IF')
        plt.ylabel('counts for citing')
        plt.figure()
        plt.plot(input_Data["2017"]["mid_IF"], input_Data["2017"]["citing"], color="green", label="2017")
        plt.legend()
        plt.xlabel('IF')
        plt.ylabel('counts for citing')
        plt.figure()
        plt.plot(input_Data["2018"]["mid_IF"], input_Data["2018"]["citing"], color="yellow", label="2018")
        plt.legend()
        plt.xlabel('IF')
        plt.ylabel('counts for citing')
        plt.figure()
        plt.plot(input_Data["2019"]["mid_IF"], input_Data["2019"]["citing"], color="grey", label="2019")
        plt.legend()
        plt.xlabel('IF')
        plt.ylabel('counts for citing')
        plt.show()

    def plot_year_IF(self,x_labels,y):
        """
        绘制不同年限阶段的不同影响因子区间的文章数量
        :param x:
        :param y:
        :return:
        """
        print("x",x_labels)
        print("x",x_labels[1:-1])
        print("y",y)
        matplotlib.rcParams['font.sans-serif'] = ['SimHei']
        matplotlib.rcParams['axes.unicode_minus'] = False
        x = range(len(x_labels[1:-1]))
        """
        绘制条形图
        left:长条形中点横坐标
        height:长条形高度
        width:长条形宽度，默认值0.8
        label:为后面设置legend准备
        """
        rects1 = plt.bar(left=x, height=y["0-1"][1:-1], width=0.15, alpha=0.8, color='red', label="0-1")
        rects2 = plt.bar(left=[i + 0.15 for i in x], height=y["1-3"][1:-1], width=0.15, color='green', label="1-3")
        rects3 = plt.bar(left=[i + 0.3 for i in x], height=y["3-5"][1:-1], width=0.15, color='blue', label="3-5")
        rects4 = plt.bar(left=[i + 0.45 for i in x], height=y["5-10"][1:-1], width=0.15, color='grey', label="5-10")
        rects5 = plt.bar(left=[i + 0.6 for i in x], height=y["10-30"][1:-1], width=0.15, color='yellow', label="10-30")
        rects6 = plt.bar(left=[i + 0.75 for i in x], height=y[">30"][1:-1], width=0.15, color='black', label=">30")
        plt.ylim(0, 50)  # y轴取值范围
        plt.ylabel("counts for paper")
        """
        设置x轴刻度显示值
        参数一：中点坐标
        参数二：显示值
        """
        plt.xticks([index + 0.2 for index in x], x_labels[1:-1])
        plt.xlabel("years")
        plt.title("IF_distribution")
        plt.legend()  # 设置题注
        # 编辑文本
        for rect in rects1:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2, height + 1, str(height), ha="center", va="bottom")
        for rect in rects2:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2, height + 1, str(height), ha="center", va="bottom")
        for rect in rects3:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2, height + 1, str(height), ha="center", va="bottom")

        for rect in rects4:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2, height + 1, str(height), ha="center", va="bottom")

        for rect in rects5:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2, height + 1, str(height), ha="center", va="bottom")

        for rect in rects6:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2, height + 1, str(height), ha="center", va="bottom")

        plt.show()

    def plot_IF_bar(self,IF_static_dict):
        """
        绘制整体数据的影响因子
        :param IF_static_dict:
        :return:
        """
        print(IF_static_dict)
        x_labels = []
        y_values = []
        for key,value in IF_static_dict.items():
            x_labels.append(key)
            y_values.append(value)
        print(x_labels,y_values)
        x = range(len(x_labels))
        rects = plt.bar(left=x,height=y_values,width=0.3,alpha = 0.8,color="blue",label= "IF_Distribution")
        plt.ylim(0,150)
        plt.ylabel("counts of paper")
        plt.xticks(x,x_labels)
        plt.xlabel("IF_section")
        plt.title("IF_distribution in total data")
        #编辑文本数据
        for num,rect in enumerate(rects):
            plt.text(rect.get_x() + rect.get_width() / 2, y_values[num] +1, str(y_values[num]), ha="center", va="bottom")
        plt.legend()
        plt.show()

    def Analysis_citing(self):


        self.slice_data = self.data_info.ix[:,["pmid","citing","year"]]
        self.num_dict = {"0":[],"1-10":[],"10-30":[],"30-100":[],">100":[]}

        info_years = {}

        for num,year in enumerate(self.years):
            info_years[str(year)] = self.slice_data[self.slice_data["year"] == int(year)]
        for year,data_info in info_years.items():
            self.citing_distri = {"0":[],"1-10":[],"10-30":[],"30-100":[],">100":[]}
            data_info_dict = data_info.to_dict("list")
            print(str(year)+"文章总数为",len(data_info_dict["citing"]))
            for citing_value in data_info_dict["citing"]:
            #print(citing_value)
                if int(citing_value) == 0:
                    self.citing_distri["0"].append(citing_value)
                elif int(citing_value) >= 1 and int(citing_value) < 10:
                    self.citing_distri["1-10"].append(citing_value)
                elif int(citing_value) >= 10 and int(citing_value) <30:
                    self.citing_distri["10-30"].append(citing_value)
                elif int(citing_value) >= 30 and int(citing_value)<100:
                    self.citing_distri["30-100"].append(citing_value)
                elif int(citing_value) >= 100:
                    self.citing_distri[">100"].append(citing_value)
            for key,value_list in self.citing_distri.items():
                self.num_dict[key].append(len(value_list))
        print("最终文章分布列表",self.num_dict)
        #绘制citing条形图
        self.plot_citing_bar(self.years,self.num_dict)

    def plot_citing_bar(self,x_list,y_dict):
        """
        绘制关于不同年限引用率的堆叠图
        :param x_list:
        :param y_dict:
        :return:
        """
        print("x_list",x_list)
        print("y_dict",y_dict)
        new_y_dict = {}
        new_x_list = ["0","1-10","10-30","30-100",">100"]
        for num,y_tuple in enumerate(zip(y_dict["0"], y_dict["1-10"],y_dict["10-30"],y_dict["30-100"],y_dict[">100"])):
            new_y_dict.update({str(num):list(y_tuple)})
        print(new_y_dict)

        matplotlib.rcParams['font.sans-serif'] = ['SimHei']
        matplotlib.rcParams['axes.unicode_minus'] = False
        x = range(len(x_list[1:-1]))

        rects1 = plt.bar(left=x, height=y_dict["0"][1:-1], width=0.15, alpha=0.8, color='red', label="0")
        rects2 = plt.bar(left=[i + 0.15 for i in x], height=y_dict["1-10"][1:-1], width=0.15, color='green', label="1-10")
        rects3 = plt.bar(left=[i + 0.3 for i in x], height=y_dict["10-30"][1:-1], width=0.15, color='blue', label="10-30")
        rects4 = plt.bar(left=[i + 0.45 for i in x], height=y_dict["30-100"][1:-1], width=0.15, color='grey', label="30-100")
        rects5 = plt.bar(left=[i + 0.6 for i in x], height=y_dict[">100"][1:-1], width=0.15, color='yellow', label=">100")

        #plt.bar(x,np.array(new_y_dict["0"]),width=0.45, alpha=0.8, color='red', label="2015")
        #plt.bar(x,np.array(new_y_dict["1"]), width=0.45, color='green', label="2016",bottom= np.array(new_y_dict["0"]))

        #plt.bar(x, np.array(new_y_dict["2"]), width=0.45, color='blue', label="2017",bottom=np.array(new_y_dict["1"])+np.array(new_y_dict["0"]))
        #plt.bar(x, new_y_dict["3"], width=0.45, color='grey', label="2018",bottom=np.array(new_y_dict["1"])+np.array(new_y_dict["0"])+np.array(new_y_dict["2"]))
        #plt.bar(x, new_y_dict["4"], width=0.45, color='yellow', label="2019",bottom=np.array(new_y_dict["1"])+np.array(new_y_dict["0"])+np.array(new_y_dict["2"])+np.array(new_y_dict["3"]))

        for rect in rects1:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2, height + 1, str(height), ha="center", va="bottom")
        for rect in rects2:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2, height + 1, str(height), ha="center", va="bottom")
        for rect in rects3:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2, height + 1, str(height), ha="center", va="bottom")

        for rect in rects4:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2, height + 1, str(height), ha="center", va="bottom")

        for rect in rects5:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2, height + 1, str(height), ha="center", va="bottom")

        plt.ylim(0,50)
        plt.ylabel("The nums for paper")
        plt.xticks(x, x_list[1:-1])
        plt.xlabel("years")
        plt.title("Distribution statistics of citation ")
        plt.legend()
        plt.show()

if __name__ == "__main__":
    original_data = "./Data/pubmed_paper_info_2.xlsx"
    pm_data = pubmed_data(original_data)
    pm_data.Analysis_citing()
