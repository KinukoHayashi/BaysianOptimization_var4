#!/usr/bin/env python
# coding: utf-8
# In[ ]:
#Z座標の移動平均を求めるプログラム
import h5py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
def MovAveZ(s):
    
    print("---MovAveZstart---")
    count = 0
    flag = 0
    time = []
    
    PositionZ_test_max = [[],[],[],[],[]]  #各りょういきのZ座標の最大値
    moving_avarage = [[],[],[],[],[]]   #移動平均
    for i in range (10,500,5):
        count+=1
        #print(“filename is” +str(i)+“.h5")
        time.append(i*2/100) #横軸 時間
        #print(“time is “+str(time))
        MAX_X = 0
        
        outputfile ="D:/hayashi_dem/drum_dem_test5/test5_"+str(s)+"_data/"+str(i)+".h5"
        #outputfile = "D:/hayashi_dem/drum_dem_test2/test2_20_data/"+str(i)+".h5"
        h5file = h5py.File(outputfile,'r+')
        dir = "TimestepData/"
        ## list作成
        members = []
        ## “CreatorData中のすべてのフォルダーを展開してlistに収納
        h5file[dir].visit(members.append)
        ## 収納した0番目のフォルダー(0になる)を表示
        #print (members[0])
        folder0 ="TimestepData/"+str(members[0])+"/ParticleTypes/0"
        ## 0粒子のPosition XYZの値をそれぞれリストに入れる
        PositionX_test = h5file[folder0+"/position"][:,0]
        PositionZ_test = h5file[folder0+"/position"][:,2]
        #粒子のX座標が一定値より大きい粒子は削除する
        PositionX_test_1 = []
        PositionZ_test_1 = []
        PositionX_test_2 = [[],[],[],[],[]]
        PositionZ_test_2 = [[],[],[],[],[]]
        for k in range(0,len(PositionX_test)-1):
            if(PositionX_test[k] <= MAX_X):#x座標が一定値より小さいばあい
                PositionX_test_1.append(PositionX_test[k])
                PositionZ_test_1.append(PositionZ_test[k])
        #Xの最しょう値のindex番号
        test_x_index_min = np.argmin(PositionX_test_1)
        Δ = (MAX_X - PositionX_test_1[test_x_index_min])/5
        #print(“Δ=“+str(Δ))
        for l in range(0,5):
            #print(str(PositionX_0_2[index_b] + i*Δ)+“~”+str(PositionX_0_2[index_b] + (i+1)*Δ))
            #粒子を区分ごとに仕分けする
            for t in range(0,len(PositionX_test_1)):
                if(PositionX_test_1[test_x_index_min] + l*Δ < PositionX_test_1[t] and PositionX_test_1[t] < PositionX_test_1[test_x_index_min] + (l+1)*Δ) :
                    #print(l,t)
                    PositionX_test_2[l].append(PositionX_test_1[t])
                    PositionZ_test_2[l].append(PositionZ_test_1[t])
            
            #領域内で最大のZざひょうをもつ粒子をとりだしてきろくする
            if(len(PositionZ_test_2[l]) != 0):
                
                z_index_max = np.argmax(PositionZ_test_2[l]) #Zの最大値のindex番号
                PositionZ_test_max[l].append(PositionZ_test_2[l][z_index_max])
                moving_avarage[l].append(sum(PositionZ_test_max[l])/count)
            else:
                moving_avarage[l].append(None)
        
        if(i % 50 == 0 and i>= 150 and flag ==0):

            for d in range(1,5):
                if(moving_avarage[d][len(moving_avarage[d])-1] != None and moving_avarage[d][len(moving_avarage[d])-1-10] != None):
                    grad = ((moving_avarage[d][len(moving_avarage[d])-1]-moving_avarage[d][len(moving_avarage[d])-1-10])/2)
                    #print(len(moving_avarage[1])-1,len(moving_avarage[1])-11)
                    print(d)
                    print(str(i/50)+"s"+str(grad))
                    
                    if(-0.0002>=grad or grad>=0.0002): 
                        break
                   
                if(d == 4):
                    steadytime = i/50
                    flag = 1
    
    if(flag ==0):
        steadytime = 15 #　10秒たっても定常状態にならなかった場合　よくかんがえる   
            
    print("\n")
    #print("moving_avarage[0]="+str(moving_avarage[0]))
    #print(“\n”)
    #print(len(time))
    #print(len(moving_avarage[0]))
    """
    plt.plot(time,moving_avarage[0],"r.",label = "region1")
    plt.plot(time,moving_avarage[1],"b.",label = "region2")
    plt.plot(time,moving_avarage[2],"g.",label = "region3")
    plt.plot(time,moving_avarage[3],"y.",label = "region4")
    plt.plot(time,moving_avarage[4],"k.",label = "region5")
    plt.legend()
    plt.xlabel("time [s]")#x軸の名前
    plt.ylabel("Moving average of Z [m]")#y軸の名前
    plt.xlim(0,10) #x軸の範囲
    plt.ylim(-0.05,0.05)#y軸の範囲
    #plt.plot(PositionX_0_max,np.multiply(a,PositionX_0_max)+b,“g--“)
    plt.grid()
    plt.show()
    """
    
    print("---Moving Average end---")
    #time =int(input("定常状態になる時間をきにゅうしてください") )
    return steadytime
    
# %%
