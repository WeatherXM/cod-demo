import glob, os
import sys
import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import math, json


def comp_plotter(obs, forecasts, xmajor_points, xmajor_labels, num_of_ws, num_of_models, ylabel,legend_names,graph_title,min,max,yticks_int,fn):
    fig = plt.figure(figsize=(25, 10))
    ax = plt.axes()
    fs = 20

    for l in range(0, num_of_models):
        plt.plot(forecasts[l], linewidth=2)
        ax.set_xlim([0, len(T_for_tot[l]) - 1])

    for l in range(0, num_of_ws):
        plt.plot(obs[l], linewidth=3,color='black')

    plt.title(graph_title, fontsize=fs)
    plt.legend(legend_names, fontsize=fs-4)
    plt.xticks(xmajor_points)
    ax.set_xticklabels(xmajor_labels, fontsize=fs)
    ax.tick_params(axis='both', which='major', labelsize=fs, length=10, width=2)
    ax.tick_params(which='minor', length=5, width=2)
    ax.grid(color='gray', linestyle='--', linewidth=0.4)
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(2)
    plt.xticks(rotation=45)
    plt.ylabel(ylabel, fontsize=fs)
    plt.yticks(np.arange(min, max+1, yticks_int))
    plt.savefig(out_path + fn + '.png')


def rmse(predictions, targets, nan_decision):
    p = []
    t = []
    if nan_decision == 'omit' and np.count_nonzero(np.isnan(predictions))<5 and np.count_nonzero(np.isnan(targets))<5:
        for c in range(0, len(predictions)):
            if (math.isnan(predictions[c])==False and math.isnan(targets[c])==False):
                p.append(predictions[c])
                t.append(targets[c])
        return np.sqrt(((np.array(p) - np.array(t)) ** 2).mean())
    else:
        return np.nan


def stats_plotter(stat_metric,ylabel,rmin,rmax,yticks_int,graph_title):
    fig = plt.figure(figsize=(25, 10))
    ax = plt.axes()
    fs = 20

    for l in range(0, num_of_models):
        plt.plot(stat_metric[l], linewidth=3)

    plt.title(graph_title, fontsize=fs)
    plt.legend(legend_names, fontsize=fs-4)
    plt.xticks(np.arange(0,len(xmajor_labels)))
    ax.set_xlim([0, len(xmajor_labels) - 1])
    ax.set_xticklabels(xmajor_labels, fontsize=fs)
    ax.tick_params(axis='both', which='major', labelsize=fs, length=10, width=2)
    ax.grid(color='gray', linestyle='--', linewidth=0.4)
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(2)
    plt.xticks(rotation=45)
    plt.ylabel(ylabel, fontsize=fs)
    plt.yticks(np.arange(rmin, rmax+0.01, yticks_int))

    if ylabel == 'r':
        a = ax.get_ygridlines()
        zero = a[10]
        zero.set_color('black')
        zero.set_linewidth(3)

        top = a[18]
        top.set_color('red')
        top.set_linewidth(3)

        bottom = a[2]
        bottom.set_color('red')
        bottom.set_linewidth(3)

    plt.savefig(out_path+graph_title+'.png')




if len(sys.argv) != 3:
    print('Not enough CLI arguments provided!')
    print('Please provide the path of the input directory and the path of the output directory')
    sys.exit(1)


pattern = sys.argv[1]
print('Using glob pattern: ', pattern)
for dir in glob.glob(pattern):
    exp_path = dir + '/'
    out_path = sys.argv[2] + '/'
    print('Will use files from ' + exp_path + ' and store images at ' + out_path)
    obs_path = exp_path + 'obs/'
    for_path = exp_path + 'for/'

    #Getting observation files
    os.chdir(obs_path)
    ws_fn = []
    c = 0
    for obsfile in glob.glob("*.csv"):
        ws_fn.append(obsfile)
        c = c + 1

    num_of_ws = len(ws_fn)

    #Getting forecast files
    os.chdir(for_path)
    model_fn = []
    c = 0
    for forfile in glob.glob("*.csv"):
        model_fn.append(forfile)
        c = c + 1

    num_of_models = len(model_fn)

    temperature = []
    rh = []
    wspd = []
    ts = []

    #Reading observations
    for l in range(0, num_of_ws):

        #Reading csv
        obs_path = obs_path + ws_fn[l]
        df_obs = pd.read_csv(obs_path)

        temperature.append(df_obs["temperature"].values.tolist())
        rh.append(df_obs["humidity"].values.tolist())
        wspd.append(df_obs["wind_speed"].values.tolist())
        ts.append(df_obs["date"].values.tolist())

        #Wind speed conversion from m/s to km/h
        for x in range(len(wspd[l])):
            wspd[l][x] = wspd[l][x]*3.6

        #Getting x-axis points and labels
        xmajor_points = []
        xmajor_labels = []
        for x in range(len(ts[l])):
            date_temp = re.split(r' |:|-', ts[l][x])
            date_temp_prev = '-1000'
            if (x==0):
                xmajor_points.append(x)
                xmajor_labels.append(str(date_temp[2]) + '/' + str(date_temp[1]))
            elif (x > 0):
                date_temp_prev = re.split(r' |:|-', ts[l][x - 1])

                if (l == 0 and (int(date_temp_prev[2]) != int(date_temp[2]))):
                    xmajor_points.append(x)
                    xmajor_labels.append(str(date_temp[2]) + '/' + str(date_temp[1]))

    #Reading models
    T_for_tot = []
    RH_for_tot = []
    WS_for_tot = []

    for l in range(0, num_of_models):

        T_for = []
        RH_for = []
        WS_for = []
        path = for_path + model_fn[l]
        df_for = pd.read_csv(path)

        col_labels = []
        for col in df_for.columns:
            col_labels.append(col)

        for x in range (9,len(df_for.columns)):
            T_for.append(df_for[col_labels[x]].values[0])
            RH_for.append(df_for[col_labels[x]].values[1])
            WS_for.append(df_for[col_labels[x]].values[2])

        T_for_tot.append(T_for)
        RH_for_tot.append(RH_for)
        WS_for_tot.append(WS_for)

    #Getting info for the graphs
    for l in range(0, num_of_models):
        model_fn[l]=model_fn[l][:-4] #Excluding csv from filenames to use them for graph legend

    for l in range(0, num_of_ws):
        ws_fn[l]=ws_fn[l][:-4] #Excluding csv from filenames to use them for graph legend

    #Getting start and end dates from observations
    end_day=re.split(r' |:|-', ts[0][len(ts[0])-1])
    start_day=re.split(r' |:|-', ts[0][0])
    days_of_data = int(end_day[2])-int(start_day[2])+1

    sd = start_day[2] + '/' + start_day[1] + '/' + start_day[0]
    ed = end_day[2] + '/' + end_day[1] + '/' + end_day[0]

    legend_names = model_fn + ws_fn


    #Finding margins of data
    mins = [10000]*(num_of_models+num_of_ws-1)
    maxs = [-10000]*(num_of_models+num_of_ws-1)

    for l in range(0, num_of_models):
        if min(T_for_tot[l])<mins[0]:
            mins[0]=min(T_for_tot[l])
        if min(WS_for_tot[l])<mins[2]:
            mins[2]=min(WS_for_tot[l])
        mins[1] = 0

        if max(T_for_tot[l])>maxs[0]:
            maxs[0]=max(T_for_tot[l])
        if max(WS_for_tot[l])>maxs[2]:
            maxs[2]=max(WS_for_tot[l])
        maxs[1] = 100

    for l in range(0, num_of_ws):
        if min(temperature[l])<mins[0]:
            mins[0]=min(T_for_tot[l])
        if min(wspd[l])<mins[2]:
            mins[2]=min(WS_for_tot[l])
    mins[0] = int(mins[0]-2)
    maxs[0] = int(maxs[0]+2)
    maxs[2] = int(maxs[2]+5)

    comp_plotter(temperature,T_for_tot,xmajor_points,xmajor_labels,num_of_ws,num_of_models,'Temperature [°C]',legend_names,'Temperature comparison for the period ' + sd + ' - ' + ed,mins[0],maxs[0],2,"temp")
    comp_plotter(rh,RH_for_tot,xmajor_points,xmajor_labels,num_of_ws,num_of_models,'RH [%]',legend_names,'RH comparison for the period ' + sd + ' - ' + ed,mins[1],maxs[1],10,'rh')
    comp_plotter(wspd,WS_for_tot,xmajor_points,xmajor_labels,num_of_ws,num_of_models,'Wind Speed Average [Km/h]',legend_names,'Wind Speed Average comparison for the period ' + sd + ' - ' + ed,mins[2],maxs[2],5,'ws')


    #Calculating stats

    #Preparing data for the statistical analysis
    #Making with 24 slots for each of the days
    T = [[[np.nan]*int(24) for i in range(days_of_data)] for j in range(num_of_models+num_of_ws)]
    RH = [[[np.nan]*int(24) for i in range(days_of_data)] for j in range(num_of_models+num_of_ws)]
    WS = [[[np.nan]*int(24) for i in range(days_of_data)] for j in range(num_of_models+num_of_ws)]

    for l in range(0, num_of_models+num_of_ws):
        for y in range(days_of_data):
            for x in range(0,24):
                if (l<num_of_models):
                    T[l][y][x] = T_for_tot[l][24*y+x]
                    RH[l][y][x] = RH_for_tot[l][24 * y + x]
                    WS[l][y][x] = WS_for_tot[l][24 * y + x]

                elif (l>=num_of_models):
                    T[l][y][x] = temperature[0][24*y+x]
                    RH[l][y][x] = rh[0][24 * y + x]
                    WS[l][y][x] = wspd[0][24 * y + x]

    #Statistical analysis
    T_cc = [[np.nan]*int(days_of_data) for i in range(num_of_models+num_of_ws)]
    T_rmse = [[np.nan]*int(days_of_data) for i in range(num_of_models+num_of_ws)]

    RH_cc = [[np.nan]*int(days_of_data) for i in range(num_of_models+num_of_ws)]
    RH_rmse = [[np.nan]*int(days_of_data) for i in range(num_of_models+num_of_ws)]

    WS_cc = [[np.nan]*int(days_of_data) for i in range(num_of_models+num_of_ws)]
    WS_rmse = [[np.nan]*int(days_of_data) for i in range(num_of_models+num_of_ws)]



    output = []
    for l in range(0, num_of_models):
        for y in range(days_of_data):
            T_cc[l][y] = stats.spearmanr(T[l][y],T[num_of_models][y],nan_policy='omit')[0]
            T_rmse[l][y] = rmse(T[l][y], T[num_of_models][y],'omit')

            RH_cc[l][y] = stats.spearmanr(RH[l][y], RH[num_of_models][y], nan_policy='omit')[0]
            RH_rmse[l][y] = rmse(RH[l][y], RH[num_of_models][y], 'omit')

            WS_cc[l][y] = stats.spearmanr(WS[l][y], WS[num_of_models][y], nan_policy='omit')[0]
            WS_rmse[l][y] = rmse(WS[l][y], WS[num_of_models][y], 'omit')
        results = {
            "T_rmse": list(zip(xmajor_labels, T_rmse[l])),
            "RH_rmse": list(zip(xmajor_labels, RH_rmse[l])),
            "WS_rmse": list(zip(xmajor_labels, WS_rmse[l])),
        }
        output.append(results)

    print(json.dumps(output))




    stats_plotter(T_cc,'r',-1,1,0.1,'Temperature (1-day ahead forecast) - Spearman Correlation')
    stats_plotter(RH_cc,'r',-1,1,0.1,'RH (1-day ahead forecast) - Spearman Correlation')
    stats_plotter(WS_cc,'r',-1,1,0.1,'Wind Speed (1-day ahead forecast) - Spearman Correlation')

    stats_plotter(T_rmse,'RMSE',0,5,1,'Temperature (1-day ahead forecast) - RMSE')
    stats_plotter(RH_rmse,'RMSE',0,30,2.5,'RH (1-day ahead forecast) - RMSE')
    stats_plotter(WS_rmse,'RMSE',0,15,2.5,'Wind Speed (1-day ahead forecast) - RMSE')
    print('')


