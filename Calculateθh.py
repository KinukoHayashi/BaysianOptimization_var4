#CalculateΘh
import h5py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

def Calculateθh(safetime,particle_radius,k):
    print("---Calculateθhstart---")
    degree = 0
    hight = 0
    SAMPLE = 10 # サンプリングする粒子の個数
    MAX_X = 0 #X座標の最大値(これよりX座標が小さい粒子を選ぶ)
    MIN_Y = -1 #Y座標の最小値(これよりY座標が大きい粒子を選ぶ)
    MAX_Y = 1 #Y座標の最大値(これよりY座標が小さい粒子を選ぶ)
    count = 1
    for i in range (safetime*50,(safetime*50)+151,50): 
        
        PositionX_0_1 = []
        PositionY_0_1 = []
        PositionZ_0_1 = []
        PositionX_0_2 = []
        PositionY_0_2 = []
        PositionZ_0_2 = []
        PositionX_0_3 = []
        PositionY_0_3 = []
        PositionZ_0_3 = []
        PositionX_0_max = []
        PositionY_0_max = []
        PositionZ_0_max = []
        midX = []
        
        outputfile = "D:/hayashi_dem/drum_dem_test5/test5_"+str(k)+"_data/"+str(i)+".h5"
        h5file = h5py.File(outputfile,'r+')
        dir = "TimestepData/"
        ## list作成
        members = []
        ## "CreatorData中のすべてのフォルダーを展開してlistに収納
        h5file[dir].visit(members.append)
        ## 収納した0番目のフォルダー(0になる)を表示
        #print (members[0])
        folder0 ="TimestepData/"+str(members[0])+"/ParticleTypes/0"
        ## 0粒子のPosition XYZの値をそれぞれリストに入れる
        PositionX_0 = h5file[folder0+"/position"][:,0]
        PositionY_0 = h5file[folder0+"/position"][:,1]
        PositionZ_0 = h5file[folder0+"/position"][:,2]
        
        #高さの計算
        PositionZ_0_temp = sorted(PositionZ_0)
        H = PositionZ_0_temp[len(PositionZ_0_temp)-1]-PositionZ_0_temp[0] +particle_radius+particle_radius #m
        #print( particle_radius)
        #print( PositionZ_0_temp[len(PositionZ_0_temp)-1])
        #print( PositionZ_0_temp[0])
        print(str(H)+"m")
        
        #X座標の最小値を出力する.なおこの最大値を持つ粒子を点bとする
        index_b =  np.argmin(PositionX_0)
        #print("X 最小値 = "+str(np.min(PositionX_0)))
        #print("index番号 = "+str(index_b)+"\n")
        if(index_b > MAX_X):
            index_b =  np.argmax(PositionZ_0)
            MAX_X = (PositionX_0[index_b] + PositionX_0[index_b])/2
           
        #∠ABC (点B周りの角度)を算出する
        #粒子のX座標が一定値より大きい粒子は削除する

        for i in range(0,len(PositionX_0)-1):
            if(PositionX_0[i] <= MAX_X):#x座標が一定値より小さいばあい
                PositionX_0_1.append(PositionX_0[i])
                PositionY_0_1.append(PositionY_0[i])
                PositionZ_0_1.append(PositionZ_0[i])
        
        #print(len(PositionX_0_1))
        #y=y~y+Δyの範囲の粒子を抽出する どこの範囲を選ぶか未定
    
        for i in  range(0,len(PositionX_0_1)-1):
            if(PositionY_0_1[i] < MAX_Y and PositionY_0_1[i] > MIN_Y ): #yの範囲に含まれている場合
                PositionX_0_2.append(PositionX_0_1[i])
                PositionY_0_2.append(PositionY_0_1[i])
                PositionZ_0_2.append(PositionZ_0_1[i])
        print("yが"+str(MIN_Y)+"~"+str(MAX_Y)+"の範囲にある粒子の個数は"+str(len(PositionX_0_2))+"個です")
        
        index_b =  np.argmin(PositionX_0_2)
        print("X 最小値 = "+str(np.min(PositionX_0_2)))
        #print("index番号 = "+str(index_b)+"\n")
        b = np.array([PositionX_0_2[index_b],PositionY_0_2[index_b],PositionZ_0_2[index_b]])
        #print(str(b)+"\n")
        index_n =  np.argmax(PositionX_0_2)
        c = np.array([PositionX_0_2[index_n],PositionY_0_2[index_n],PositionZ_0_2[index_n]])
        #print(str(c)+"\n")

        
        #100この粒子をサンプリング
        Δ = (MAX_X - PositionX_0_2[index_b])/SAMPLE   
        print("Δ="+str(Δ))
        
        for i in range(0,SAMPLE):
            #print(str(PositionX_0_2[index_b] + i*Δ)+"~"+str(PositionX_0_2[index_b] + (i+1)*Δ))
            for t in range(0,len(PositionX_0_2)):
                if(PositionX_0_2[index_b] + i*Δ < PositionX_0_2[t] and PositionX_0_2[t] < PositionX_0_2[index_b] + (i+1)*Δ) :
                    
                    PositionX_0_3.append(PositionX_0_2[t])
                    PositionY_0_3.append(PositionY_0_2[t])
                    PositionZ_0_3.append(PositionZ_0_2[t])
                    
            if(len(PositionX_0_3) !=0):
                midX.append(PositionX_0_2[index_b]+(i+0.5)*Δ)
                index_max = np.argmax(PositionZ_0_3) #Zの最大値のindex番号
                PositionX_0_max.append(PositionX_0_3[index_max])
                PositionY_0_max.append(PositionY_0_3[index_max])
                PositionZ_0_max.append(PositionZ_0_3[index_max])
                PositionX_0_3.clear()
                PositionY_0_3.clear()
                PositionZ_0_3.clear()
        #print(len(midX))
        #print(len(PositionZ_0_max))

        A = np.array([midX,np.ones(len(midX))])
        A = A.T
        a,b = np.linalg.lstsq(A,PositionZ_0_max,rcond=None)[0]
        """
        plt.plot(midX,PositionZ_0_max,"ro")
        plt.plot(midX,np.multiply(a,midX)+b,"g--")
        plt.grid()
        plt.show()
        """
        θ = math.degrees(math.atan(a))
        print(str(count)+"回目の試行結果"+str(SAMPLE)+"個サンプリングしたときの動的安息角は"+str(θ)+"°です。高さは"+str(H)+"mです")
        degree = degree + θ
        hight = hight + H #m
        count = count + 1
    
    print(str(count-1)+"回の試行結果の平均は"+str(degree/(count-1))+"°です。高さは"+str(hight/(count-1))+"mです.")
    print("---Calculateθhend---")
    return degree/(count-1),(hight/(count-1))

