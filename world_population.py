import datetime
import json
import numpy as np
import matplotlib.mlab as mlb
import matplotlib.pyplot as plt
import pygal
from pygal_maps_world.i18n import COUNTRIES

"""
@Author: Emily
@Date: 08/02/2018
task:
1.选择一个年份（比如2000年），将世界人口数据进行数据可视化（制作世界人口地图），并保存图片
2.绘制中国、印度、美国这三个国家人口从1960~2010年的增长图（折线图），并保存图片

"""


filename = 'population_data.json'

#Read json file
def read_file(filename):
    with open(filename) as f:
        pop_data = json.load(f)
    f.close()
    return pop_data

#produce country_code(two bits)
def get_country_code(country_name):
    for code, name in COUNTRIES.items():
        if name == country_name:
            return code
    return None

#get x,y chart data
def get_chart_data(data_dict, string):
    lst_x = []
    lst_y = []
    for data in data_dict:
        if data['Country Name'] == string:
            year = data['Year']
            lst_x.append(datetime.date(int(year), 12, 31))
            population = data['Value']
            lst_y.append(int(float(population)))
    return lst_x, lst_y

#To solve task2
def draw_map(filename):
    lst_Chx, lst_Chy, lst_Amx, lst_Amy, lst_Inx, lst_Iny = ([], [], [],[],[],[])
    pop_data = read_file(filename)
    lst_Chx, lst_Chy = get_chart_data(pop_data, 'China')
    lst_Amx, lst_Amy = get_chart_data(pop_data, 'American Samoa')
    lst_Inx, lst_Iny = get_chart_data(pop_data, 'India')
    plt.title('Population Increasing Chart')
    plt.figure()
    plt.plot(lst_Chx, lst_Chy, color = 'red', label = 'China Population')
    plt.plot(lst_Amx, lst_Amy, color = 'blue', label = 'American Population')
    plt.plot(lst_Inx, lst_Iny, color = 'green', label = 'India Population')
    plt.legend()
    plt.xlabel('Years')
    plt.ylabel('Population')
    plt.savefig('World_population.png')

#To solve task1
def draw_world_map(filename):
    cc_population = {}
    pop_data = read_file(filename)
    for pop_dict in pop_data:
         if pop_dict['Year'] == '2000':
            country_name = pop_dict['Country Name']
            population = int(float(pop_dict['Value']))
            code = get_country_code(country_name)
            if code:
                cc_population[code] = population
    wm = pygal.maps.world.World()
    wm.title = 'The World Population in 2000'
    wm.add('In 2000 Year', cc_population)
    wm.render_to_file('World_Population.svg')

if __name__ == '__main__':

    draw_world_map(filename)
    draw_map(filename)





