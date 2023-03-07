# CalculateΘh
import math
import h5py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

# じぶんで設定する値


def Calculateθh(safetime, particle_radius, nt, test_num):
    filenum = 150
    MIN_X = -0.016  # X座標の最小値(これよりX座標が大きい粒子を選ぶ)
    MAX_X = 0.016  # X座標の最大値(これよりX座標が小さい粒子を選ぶ)
    MIN_Y = -1  # Y座標の最小値(これよりY座標が大きい粒子を選ぶ)
    MAX_Y = 1  # Y座標の最大値(これよりY座標が小さい粒子を選ぶ)
    SAMPLE = round((MAX_X - MIN_X) / particle_radius)  # サンプリングする粒子の個数
    print("---Calculateθhstart---")
    print(SAMPLE)

    degree = 0
    hight = 0
    count = 1
    Velocity_low = 0
    Velocity_high = 0

    print(str(nt))
    for i in range(safetime*50, (safetime*50 + filenum + 1)):
        V_low_count = 0
        V_high = 0
        V_low = 0
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
        PositionZ_1 = [[] for i in range(0, 4)]
        PositionZ_2 = []
        midX = []
        VelocityX = []
        VelocityZ = []
        VelocityX_1 = [[] for i in range(0, 4)]
        VelocityZ_1 = [[] for i in range(0, 4)]
        # outputfile = "D:/hayashi_dem/drum_dem_test" + \str(test_num)+"/test"+str(test_num) + \"_"+str(nt)+"_data/"+str(i)+".h5"
        outputfile = "D:/hayashi_dem_GB/GB_drum_dem_test" + \
            str(test_num)+"/test"+str(test_num) + \
            "_" + str(nt)+"_data/"+str(i)+".h5"

        h5file = h5py.File(outputfile, 'r+')
        dir = "TimestepData/"
        # list作成
        members = []
        # "CreatorData中のすべてのフォルダーを展開してlistに収納
        h5file[dir].visit(members.append)
        # 収納した0番目のフォルダー(0になる)を表示
        #print (members[0])
        folder0 = "TimestepData/"+str(members[0])+"/ParticleTypes/0"

        # 0粒子のPosition XYZの値をそれぞれリストに入れる
        PositionX_0 = h5file[folder0 + "/position"][:, 0]
        PositionY_0 = h5file[folder0 + "/position"][:, 1]
        PositionZ_0 = h5file[folder0 + "/position"][:, 2]
        VelocityX = h5file[folder0 + "/velocity"][:, 0]
        #VelocityY = h5file[folder0 + "/velocity"][:, 1]
        VelocityZ = h5file[folder0 + "/velocity"][:, 2]

        # 壁面付近の粒子の移動速度
        for k in range(len(PositionX_0)-1):
            if (-0.004 <= PositionX_0[k] and PositionX_0[k] <= 0):
                if (-0.01 <= PositionY_0[k] and PositionY_0[k] <= -0.007):
                    if (-0.05 <= PositionZ_0[k] and PositionZ_0[k] <= -0.047):
                        vel = math.sqrt(
                            VelocityX[k] * VelocityX[k] + VelocityZ[k] * VelocityZ[k])
                        #print("V_low = " + str(vel))
                        V_low = V_low + vel
                        V_low_count += 1
        Velocity_low = V_low / V_low_count + Velocity_low
        #print("V_low_count= " + str(V_low_count))
        # if (i == safetime*50 + filenum):
        # 粉体層表面の粒子の移動速度
        dx = 0.01/4
        for k in range(len(PositionX_0)-1):
            if (-0.005 <= PositionX_0[k] and PositionX_0[k] <= 0.005):
                if (0.00 <= PositionY_0[k] and PositionY_0[k] <= 0.01):
                    for t in range(0, 4):  # 4分割した
                        if (-0.005 + t*dx < PositionX_0[k] and PositionX_0[k] < -0.005 + (t+1)*dx):
                            PositionZ_1[t].append(PositionZ_0[k])
                            VelocityX_1[t].append(VelocityX[k])
                            VelocityZ_1[t].append(VelocityZ[k])

        for t in range(0, 4):
            index_max = np.argmax(PositionZ_1[t])
            vel = math.sqrt(VelocityX_1[t][index_max] * VelocityX_1[t][index_max] +
                            VelocityZ_1[t][index_max] * VelocityZ_1[t][index_max])
            #print("V_high = " + str(vel))
            V_high = V_high + vel
        Velocity_high = V_high / 4 + Velocity_high

        # 高さの計算

        for l in range(len(PositionY_0)-1):
            if (-0.005 <= PositionY_0[l] and PositionY_0[l] <= 0.005):
                PositionZ_2.append(PositionZ_0[l])

        PositionZ_0_temp = sorted(PositionZ_2)

        if (PositionZ_0_temp[len(PositionZ_0_temp)-1]-PositionZ_0_temp[len(PositionZ_0_temp)-2] >= 2*particle_radius):
            H = PositionZ_0_temp[len(
                PositionZ_0_temp)-2]-PositionZ_0_temp[0] + particle_radius*2
        else:
            H = PositionZ_0_temp[len(
                PositionZ_0_temp)-1]-PositionZ_0_temp[0] + particle_radius*2  # m

        # print(str(H)+"m")

        # 動的安息角の計算
        # X座標の最大値を出力する.なおこの最大値を持つ粒子を点bとする

        index_b = np.argmax(PositionX_0)

        #print("X 最小値 = "+str(np.min(PositionX_0)))
        #print("index番号 = "+str(index_b)+"\n")
        # 粒子のXざひょうの最大値が左半分にあったとき

        if (PositionX_0[index_b] < MIN_X):
            index_c = np.argmax(PositionZ_0)  # Zざひょうがさいだいのりゅうすのインデックス
            MIN_X = (PositionX_0[index_c] + PositionX_0[index_b])/2

        # ∠ABC (点B周りの角度)を算出する
        # 粒子のX座標が動的安息角の範囲内におさまっている場合はリストに加える

        for i in range(0, len(PositionX_0)-1):
            if (PositionX_0[i] >= MIN_X and PositionX_0[i] <= MAX_X):  # x座標が一定値より大きいばあい
                PositionX_0_1.append(PositionX_0[i])
                PositionY_0_1.append(PositionY_0[i])
                PositionZ_0_1.append(PositionZ_0[i])

        # print(len(PositionX_0_1))
        # y=y~y+Δyの範囲の粒子を抽出する どこの範囲を選ぶか未定

        for i in range(0, len(PositionX_0_1)-1):
            if (PositionY_0_1[i] < MAX_Y and PositionY_0_1[i] > MIN_Y):  # yの範囲に含まれている場合
                PositionX_0_2.append(PositionX_0_1[i])
                PositionY_0_2.append(PositionY_0_1[i])
                PositionZ_0_2.append(PositionZ_0_1[i])
        #print("yが"+str(MIN_Y)+"~"+str(MAX_Y) +"の範囲にある粒子の個数は"+str(len(PositionX_0_2))+"個です")

        # Nこの粒子をサンプリング
        Δ = (MAX_X - MIN_X)/SAMPLE
        # print("Δ="+str(Δ))

        for i in range(0, SAMPLE):
            #print(str(PositionX_0_2[index_b] + i*Δ)+"~"+str(PositionX_0_2[index_b] + (i+1)*Δ))
            for t in range(0, len(PositionX_0_2)):
                # ある区間に粒子が入って入れば
                if (MIN_X + i*Δ < PositionX_0_2[t] and PositionX_0_2[t] < MIN_X + (i+1)*Δ):

                    PositionX_0_3.append(PositionX_0_2[t])
                    PositionY_0_3.append(PositionY_0_2[t])
                    PositionZ_0_3.append(PositionZ_0_2[t])

            if (len(PositionX_0_3) != 0):
                midX.append(MIN_X+(i+0.5)*Δ)  # 粒子のX座標を追加（範囲の中央値）
                index_max = np.argmax(PositionZ_0_3)  # Zの最大値のindex番号
                PositionX_0_max.append(PositionX_0_3[index_max])
                PositionY_0_max.append(PositionY_0_3[index_max])
                PositionZ_0_max.append(PositionZ_0_3[index_max])
                PositionX_0_3.clear()
                PositionY_0_3.clear()
                PositionZ_0_3.clear()
        # print(midX)
        # print(len(PositionZ_0_max))

        A = np.array([midX, np.ones(len(midX))])
        A = A.T
        a, b = np.linalg.lstsq(A, PositionZ_0_max, rcond=None)[0]
        """
        plt.plot(midX, PositionZ_0_max, "ro")
        plt.plot(midX, np.multiply(a, midX)+b, "g--")
        plt.grid()
        plt.show()
        """
        θ = math.degrees(math.atan(a))
        # print(θ*(-1))
        #print(str(count)+"回目の試行結果"+str(SAMPLE) +"個サンプリングしたときの動的安息角は"+str(θ)+"°です。高さは"+str(H)+"mです")
        degree = degree + θ*(-1)

        hight = hight + H  # m
        count = count + 1

    print(str(count-1)+"回の試行結果の平均は"+str(degree/(count-1)) +
          "°です。高さは"+str(hight/(count-1))+"mです.")

    print("Velocity_low ="+str(Velocity_low/filenum) +
          ",Velocity_high ="+str(Velocity_high/filenum))

    print("---Calculateθhend---")
    return degree/(count-1), (hight/(count-1)), Velocity_low/filenum, Velocity_high/filenum
