# 4変数用ベイズ最適化プログラム
import h5py
import shutil
import numpy as np
import pandas as pd
import pathlib as path
import MovAveZ
import Calculateθh
import Calculateθh2
import Bayesian_Optimization
import csv
import os
import time


# 自分で設定する値
particle_radius = 0.00109  # m
drum_diameter = 100  # mm
h_exp = 51  # 52.6  # 51  # mm
θ_exp = 21.6  # 度
V_low_exp = 6.91
V_high_exp = 22.73
rot = 7.85  # 回転速度cm/s
test_num = 9
start_num = 1
end_num = 150
testcase = 24
σh = 0.918  # 0.586
σθ = 0.972
σV_low = 0.372
σV_high = 1.68
#μpp = 0.2
#μrpp = 0.01
#μwp = 0.235
#μrwp = 0.0122
point = 0
θ0 = 90
h0 = drum_diameter
###
flag = 0
cut = 17
ε = round(2*σh/h0 + 2*σθ/θ0 + 2*σV_low/rot + σV_high/rot, 4)
print("ε = "+str(ε))

# 標準化する関数


def Norm(θ, h, V_low, V_high):
    θ_norm = θ/θ0  # 30
    h_norm = h/h0  # 59.5
    V_low_norm = V_low/rot
    V_high_norm = V_high/rot

    return θ_norm, h_norm, V_low_norm, V_high_norm


# hexpとθexpの標準化を行う
θ_exp_norm, h_exp_norm, V_low_exp_norm, V_high_exp_norm = Norm(
    θ_exp, h_exp, V_low_exp, V_high_exp)
print("exp標準化後のh,θの値は"+str(θ_exp_norm), str(h_exp_norm))

L = 10  # 適当な値

# i.h5のファイルにoutputする

for k in range(start_num, end_num):

    if (flag == 0):
        try_num = k
    else:
        try_num = cut

    print("k = "+str(k), "try_num = "+str(try_num))

    # outputfile = "D:/hayashi_dem/drum_dem_test" + \str(test_num)+"/test"+str(test_num)+"_"+str(try_num)+"_data/0.h5"
    outputfile = "D:/hayashi_dem_GB/GB_drum_dem_test" + \
        str(test_num)+"/test"+str(test_num) + \
        "_" + str(try_num)+"_data/0.h5"

    h5file = h5py.File(outputfile, 'r+')
    dir = "CreatorData/"

    # list作成
    members = []

    # "CreatorData中のすべてのフォルダーを展開してlistに収納
    h5file[dir].visit(members.append)
    # パラメータ数を計算

    # 収納した0番目のフォルダー(0になる)を表示
    print(members[0])
    folder0 = "CreatorData/"+str(members[0])+"/Interactions"
    folderh = "CreatorData/"+str(members[0])+"/Particle Types/0/spheres"
    #particle_radius= h5file[folderh][0,"contactRadius"] [m]

    if (flag == 0):

        safetime = MovAveZ.MovAveZ(k, test_num)
        print("Time to reach steady state is "+str(safetime))

        #folder200 ="CreatorData/"+str(members[200])+"/Interactions"
        θ_h = Calculateθh.Calculateθh(
            int(safetime), particle_radius, k, test_num)
        # θ_h = Calculateθh2.Calculateθh2(
        # int(safetime), particle_radius, k, test_num)

        θ_dem = round(θ_h[0], 3)
        h_dem = round(θ_h[1]*1000, 3)
        V_low_dem = round(θ_h[2]*100, 3)
        V_high_dem = round(θ_h[3]*100, 3)
    else:
        θhdata = pd.read_csv("GB_θh_data"+str(test_num) +
                             ".csv", encoding="utf-8")
        θ_dem = θhdata.values[cut, 1]
        h_dem = θhdata.values[cut, 2]

    θhdata = [k, θ_dem, h_dem, V_low_dem, V_high_dem]
    print(θhdata)
    # θとhのあたいをきろく
    with open('GB_θh_data'+str(test_num) +
              '.csv', 'a', newline="")as f:
        writer = csv.writer(f)
        writer.writerow(θhdata)

    # θとhのあたいを標準化する
    θ_dem_norm, h_dem_norm, V_low_dem_norm, V_high_dem_norm = Norm(
        θ_dem, h_dem, V_low_dem, V_high_dem)
    L = round(abs(θ_exp_norm - θ_dem_norm) + abs(h_exp_norm -
              h_dem_norm) + abs(V_low_exp_norm - V_low_dem_norm)+abs(V_high_exp_norm - V_high_dem_norm), 3)

    print("dem標準化後のh,θの値は"+str(h_dem_norm), str(θ_dem_norm))
    print("L="+str(L))

    # 粒子の物性値を記録する

    particle_particle_Friction = h5file[folder0][0, "staticFriction"]
    particle_particle_rollingFriction = h5file[folder0][0, "rollingFriction"]
    particle_wall_Friction = h5file[folder0][2, "staticFriction"]
    particle_wall_rollingFriction = h5file[folder0][2, "rollingFriction"]

    print(particle_particle_Friction,
          particle_particle_rollingFriction, particle_wall_Friction, particle_wall_rollingFriction,  θ_dem, h_dem)
    friction = [particle_particle_Friction,
                particle_particle_rollingFriction, particle_wall_Friction, particle_wall_rollingFriction,  L, k]
    with open('GB_zikken_data_'+str(test_num) +
              '.csv', 'a', newline="")as f:
        writer = csv.writer(f)
        writer.writerow(friction)

    # ベイズ最適化
    if (k >= testcase):
        # 終了判定
        flag = 0

        change_particle_restitution, cut = Bayesian_Optimization.BayOpt(
            L, ε, k, test_num)
        if (L <= ε):
            if (abs(θ_dem - θ_exp) <= 2*σθ):
                point += 1
            if (abs(h_dem - h_exp) <= 2*σh):
                point += 1
            if (abs(V_low_dem - V_low_exp) <= 2*σV_low):
                point += 1
            if (abs(V_high_dem - V_high_exp) <= σV_high):
                point += 1

            print("point = "+str(point))
            if (point >= 3):
                file = path.Path("test.txt")
                file.touch()
                print("end")
                break

        point = 0

        if (abs(particle_particle_Friction - change_particle_restitution[0]) <= 0.01 and abs(particle_particle_rollingFriction - change_particle_restitution[1]) <= 0.002 and abs(particle_wall_Friction - change_particle_restitution[2]) <= 0.01 and abs(particle_wall_rollingFriction - change_particle_restitution[3]) <= 0.002):
            file = path.Path("test.txt")
            file.touch()
            print("end")
            break
        cut = int(cut)
        h5file.flush()
        h5file.close()
        if (cut == k):

            os.mkdir("D:/hayashi_dem_GB/GB_drum_dem_test"+str(test_num) +
                     "/test"+str(test_num)+"_"+str(k+1)+"_data")
            shutil.copy("D:/hayashi_dem_GB/GB_drum_dem_test"+str(test_num)+"/test"+str(test_num)+"_1_data/0.h5",
                        "D:/hayashi_dem_GB/GB_drum_dem_test"+str(test_num)+"/test"+str(test_num)+"_"+str(k+1)+"_data/0.h5")
            shutil.copyfile("D:/hayashi_dem_GB/GB_drum_dem_test"+str(test_num)+"/test"+str(test_num)+"_1.dem",
                            "D:/hayashi_dem_GB/GB_drum_dem_test"+str(test_num)+"/test"+str(test_num)+"_"+str(k+1)+".dem")
            shutil.copyfile("D:/hayashi_dem_GB/GB_drum_dem_test"+str(test_num)+"/test"+str(test_num)+"_1.dfg",
                            "D:/hayashi_dem_GB/GB_drum_dem_test"+str(test_num)+"/test"+str(test_num)+"_"+str(k+1)+".dfg")
            shutil.copyfile("D:/hayashi_dem_GB/GB_drum_dem_test"+str(test_num)+"/test"+str(test_num)+"_1.efd",
                            "D:/hayashi_dem_GB/GB_drum_dem_test"+str(test_num)+"/test"+str(test_num)+"_"+str(k+1)+".efd")
            shutil.copyfile("D:/hayashi_dem_GB/GB_drum_dem_test"+str(test_num)+"/test"+str(test_num)+"_1.ess",
                            "D:/hayashi_dem_GB/GB_drum_dem_test"+str(test_num)+"/test"+str(test_num)+"_"+str(k+1)+".ess")
            shutil.copyfile("D:/hayashi_dem_GB/GB_drum_dem_test"+str(test_num)+"/test"+str(test_num)+"_1.ptf",
                            "D:/hayashi_dem_GB/GB_drum_dem_test"+str(test_num)+"/test"+str(test_num)+"_"+str(k+1)+".ptf")

            nextoutputfile = "D:/hayashi_dem_GB/GB_drum_dem_test" + \
                str(test_num)+"/test"+str(test_num)+"_"+str(k+1)+"_data/0.h5"
            h5file = h5py.File(nextoutputfile, 'r+')
            dir = "CreatorData/"

            # list作成
            members = []

            # "CreatorData中のすべてのフォルダーを展開してlistに収納
            h5file[dir].visit(members.append)

            # 収納した0番目のフォルダー(0になる)を表示
            print(members[0])
            nextfolder = "CreatorData/"+str(members[0])+"/Interactions"

            # 元のデータを計算した配列の値に変換する
            h5file[nextfolder][0, "staticFriction"] = change_particle_restitution[0]
            h5file[nextfolder][0, "rollingFriction"] = change_particle_restitution[1]
            h5file[nextfolder][2, "staticFriction"] = change_particle_restitution[2]
            h5file[nextfolder][2, "rollingFriction"] = change_particle_restitution[3]

            # data[...]=change_particle_diameter

            print("----------------end----------------")

            # data1[...]=particle_1_diameter

            data = particle_0_restitution = h5file[folder0][0, "restitution"]
            print(data)

            # h5ファイルを閉じる
            h5file.flush()
            h5file.close()

            bat_file = " python.bat"
            command = bat_file
            command += " " + str(k+1) + " " + str(test_num)
            os.system(command)
        else:
            flag = 1
            print("次の探索点は = "+str(cut)+"番目に探索した点と同じです")

    k += 1
