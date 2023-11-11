from matplotlib import pyplot as plt
plt.figure()
font1 = {'family': 'Times New Roman', 'weight': 'normal', 'size': 10, }
plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置
    # legend = plt.legend( handles=[True,BIGRU],prop=font1)
plt.plot(data0, color='k', linestyle='-', linewidth='0.5', label='True')
plt.plot(data1, color='gold', linestyle='-', linewidth='0.5', label='#1')
plt.plot(data2, color='skyblue', linestyle='-', linewidth='0.5', label='#2')
plt.plot(data3, color='green', linestyle='-', linewidth='0.5', label='#3')
plt.plot(data4, color='g', linestyle='-', linewidth='0.5', label='#4')
plt.plot(data5, color='darkcyan', linestyle='-', linewidth='0.5', label='#5')
plt.plot(data6, color='c', linestyle='-', linewidth='0.5', label='#6')
plt.plot(data7, color='y', linestyle='-', linewidth='0.5', label='#7')
plt.plot(data8, color='violet', linestyle='-', linewidth='0.5', label='#8')
plt.plot(data9, color='coral', linestyle='-', linewidth='0.5', label='#9')
plt.plot(data10, color='darkorange', linestyle='-', linewidth='0.5', label='#10')
plt.plot(data11, color='teal', linestyle='-', linewidth='0.5', label='#11')
plt.plot(data12, color='r', linestyle='-', linewidth='0.5', label='#12')
plt.rcParams.update({'font.size': 8})#显示图列大小
plt.legend()
plt.grid()
    #plt.legend()
plt.xlabel('Times/5min', font1)
plt.ylabel('PV/KW', font1)
plt.rcParams['font.sans-serif'] = ['Times New Roman']


plt.show()