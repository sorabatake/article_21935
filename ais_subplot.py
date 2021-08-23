#!/usr/bin/env python

import numpy as np
import pandas as pd
from datetime import datetime as dt
import sys,io
import cartopy.crs as ccrs
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.cm import ScalarMappable
import cartopy
from scipy.stats import gaussian_kde
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from matplotlib.axes import Axes
from cartopy.mpl.geoaxes import GeoAxes
GeoAxes._pcolormesh_patched = Axes.pcolormesh


def main():

    datadir =  "/Volumes/MAC_SSD/AIS/"
    #date_index = pd.date_range("2021-03-23", periods=7, freq="D")
    #date_ary = date_index.to_series().dt.strftime("%Y%m%d")
    #print(date_ary)

    #l = []        
    #for d in date_ary :
    #    print(d)

    #    ais_file = datadir+'/ais_'+ date+'.csv'

    #    ais_df = pd.read_csv(ais_file)
    #   l.append(ais_df)
    #3/25，3/29，4/4，4/15
    date1 = 20210325
    date2 = 20210329
    date3 = 20210404
    date4 = 20210415
    date = [date1,date2,date3,date4]
    #ais_df = pd.concat(l)
    dfs = []
    for i in date:

        ais_file = datadir+'/ais_'+str(i)+'.csv'
        
        ais_df = pd.read_csv(ais_file)
        dfs.append(ais_df)
        
    # データ可視化

    dataplot(dfs,date)
    
    exit(0)


def dataplot(ais_dfs,date):
    # 可視化

    # draw
    #fig = plt.figure(figsize=(12,12))
    fig = plt.figure(figsize=(10,12))
    #fig.suptitle("AIS Plot",fontsize='24')
    #axs = plt.subplots(2, 2, figsize=(12,12), tight_layout=True,
                            #subplot_kw={'projection': ccrs.PlateCarree()})
    

    extent1 =[-31.315,79.80,-54.65,51.90]
    #スエズ運河周辺
    extent2 =[29.5,40,24.5,35.5]
    # 喜望峰東
    extent3 =[40,60,-20,20]
    # 喜望峰東
    extent4 =[-15,45,24.5,45]
    # 地中海入り口
    extent5 =[-15,10,35,45]

    #喜望峰西西経0度～30度、南緯15度～北緯30度
    extent6 =[-5,15,-15,10]

    extent7 =[-22,0,0,30]

    #東経30度～120度南緯15度～北緯30度
    extent8 =[40,110,-10,15]

    extent9 =[75,100,-10,15]

    extent10 =[40,75,0,20]

    extent11 =[75,100,0,10]

    extent12 =[40,75,5,15]
    extent14 =[100,115,0,10]
    extent15 =[105,115,3,10]
    extent16 =[78,113.4,3,10]
        
    # 描画範囲設定
    extent = extent16



    c = 0
    w = 4
    h = 1
    for i in range(2):
        for j in range(2):
            t = c + 1
            ax = fig.add_subplot(w,h,t,projection=ccrs.PlateCarree())
            
            ax.set_extent(extent)
            ais_df = ais_dfs[c]
            print(ais_df)
            # 可視化の領域を設定（スエズ運河周辺）
            ais_df.LON = pd.to_numeric(ais_df['LON'], errors='coerce')
            ais_df.LAT = pd.to_numeric(ais_df['LAT'], errors='coerce')

            ais_df = ais_df[ais_df.LON >= extent[0]]
            ais_df = ais_df[ais_df.LON <= extent[1]]
            ais_df = ais_df[ais_df.LAT >= extent[2]]
            ais_df = ais_df[ais_df.LAT <= extent[3]]
            cargo = ais_df[ais_df['VESSEL_TYPE'] == 'cargo_ships']
            tank = ais_df[ais_df['VESSEL_TYPE'] == 'tankships']
            l = [cargo,tank]
            df = pd.concat(l)
            imo = df["IMO"].nunique()


            # extent のデータ抽出

            print("IMO unique num."+str(imo))
            
            r = 0.1
            
            x_bin = int((extent[1] - extent[0]) / r + 1)
            y_bin = int((extent[3] - extent[2]) / r + 1)
            print(x_bin,y_bin)
            #hist = axs[i][j].hist2d(df.LON,df.LAT,bins=(x_bin,y_bin),cmap='jet',density=False,vmin=0,vmax=50)
            ax.add_feature(cartopy.feature.LAND.with_scale('50m'),zorder=0,edgecolor='black',)
            gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                                     linewidth=1, color='black', alpha=0.5, linestyle='--')

            # カーネル密度推定
            xy = np.vstack([df.LON,df.LAT])
            z = gaussian_kde(xy)(xy)
            s = ax.scatter(df.LON, df.LAT, c=z, s=0.5,cmap ='jet',vmin=0,vmax=0.03)
            # land , grid line 描画

            gl.xlabels_top = False
            gl.ylabels_left = False
            gl.xformatter = LONGITUDE_FORMATTER
            gl.yformatter = LATITUDE_FORMATTER
            gl.xlabel_style = {'size': 15, 'color': 'gray'}
            gl.ylabel_style = {'size': 15, 'color': 'gray'}
            #cbar=plt.colorbar(s,ax=ax)
            
            #cbar=plt.colorbar(hist[3],ax=axs[i][j])
            #cbar.set_label('ship density[0-1]',size=14,)

        
            #cbar.set_label('kde [0-1]',size=14)
            # calculate 2D histogram, the shape of hist is (bin_number, bin_number)
            d = str(date[c])
            year = d[0:4]
            month = d[4:6]
            day = d[6:8]
            strdate= year + '-'+month+'-'+day
            ax.set_title('AIS '+strdate+' 00-23(UTC)',fontsize=16)
            #axs[i][j].legend(loc='lower left')
            c = c + 1



    fs_suptitle  = 20
    fs_title     = 16
    fs_graticule = 12
    fs_cbar      = 16
    
    vmin, vmax = 0,0.05      ## colormap's range
    cmap = plt.cm.jet
    #ticks = [0,0.02,0.04,0.06,0.08,0.1]
    ticks = [0,0.01,0.02,0.03,0.04,0.05]
    #ticks = range(0,0.01,0.1)    ## locations of labels of colorbar
    ticklabels = ticks           ## labels of colorbar

    # prepare boundaries of colorbar
    cnorm = np.linspace(vmin,vmax,100)
    cnorml = colors.BoundaryNorm(cnorm,256)

    # make dummy field and remove labels and measures
    ax = fig.add_axes([0.1,0,0.8,0.4])
    ax.patch.set_facecolor('None')
    for loc in ['left','right','top','bottom']:
        ax.spines[loc].set_visible(False)

    ax.tick_params(axis='x',top='off',bottom='off',labelbottom='off',colors='white',grid_color='white',labelleft='off',labelright='off')
    ax.tick_params(axis='y',left='off',right='off',labelleft='off',colors='white',grid_color='white')

    # make mappable object for colorbar
    norm = colors.Normalize(vmin=vmin,vmax=vmax)
    mappable = ScalarMappable(cmap=cmap,norm=norm)
    mappable._A = []

    # draw common colorbar
    cb = fig.colorbar(s,ax=ax,aspect=50,pad=0.08,shrink=0.8,
                      orientation='horizontal')
    cb.ax.tick_params(labelsize=fs_cbar)
    cb.set_ticks(ticks)
    cb.set_ticklabels(ticklabels)

    cb.set_label('Density',size=14,)
    plt.savefig('ais_extent16.png',bbox_inches="tight")
    
    plt.clf()
    plt.close()
    exit
    return 0 

if __name__ == '__main__':
    main()
    
