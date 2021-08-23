#!/usr/bin/env python

import numpy as np
import sys,io
import cartopy.crs as ccrs
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.cm import ScalarMappable
import cartopy
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from matplotlib.axes import Axes
from cartopy.mpl.geoaxes import GeoAxes
from matplotlib.colors import LinearSegmentedColormap

GeoAxes._pcolormesh_patched = Axes.pcolormesh

from osgeo import gdal, gdal_array

def main():
    #datadir =  "/Users/yoshik/Downloads/
    datadir =  "/Volumes/GoogleDrive/マイドライブ"

    date1 = "20210316-0322"
    date2 = "20210323-0329"
    date3 = "20210330-0405"
    date4 = "20210406-0412"
    date = [date1,date2,date3,date4]

    dfs = []
    for i in date:

        s5p_file = datadir+'/'+str(i)+'.tif'
        
        ds=gdal.Open(s5p_file, gdal.GA_ReadOnly)
        #b1 = ds.GetRasterBand(1).ReadAsArray()
        #print(ds.GetProjection())


        dfs.append(ds)
        
    # データ可視化

    dataplot(dfs,date)
    
    exit(0)


def dataplot(rs,dates):
    # 可視化


    # draw
    fig = plt.figure(figsize=(10,12))
    #fig = plt.figure(figsize=(12,12))
    #fig.suptitle("AIS Plot",fontsize='24')
    #axs = plt.subplots(2, 2, figsize=(12,12), tight_layout=True,
                            #subplot_kw={'projection': ccrs.PlateCarree()})


    #extent16 =[78,113.4,3,10]
    
    extent1 = [-25,120,-5,15]
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


    colors = ['black', 'blue', 'purple', 'cyan', 'green', 'yellow', 'red']

    colors = ['black', 'blue', 'purple', 'cyan', 'green', 'yellow', 'red']
    cmap = LinearSegmentedColormap.from_list("custom", colors, 256)
    cmap.set_under("white")  # 0より小さい値
    cmap.set_over("red")  # 4より大きい値
    cmap.set_bad("white")  # 無効な値
    c = 0
    w = 4
    h = 1
    for i in range(w):
        for j in range(h):
            t = c + 1
            #if c == 3:
            #    break
            ax = fig.add_subplot(w,h,t,projection=ccrs.PlateCarree())
            raster = rs[c]
            ax.set_extent(extent)
            xy = raster.GetGeoTransform() 
            x = raster.RasterXSize 
            y = raster.RasterYSize    
            lon_start = xy[0] 
            lon_stop = x*xy[1]+xy[0] 
            lon_step = xy[1]    
            lat_start = xy[3] 
            lat_stop = y*xy[5]+xy[3] 
            lat_step = xy[5]

            #cbar=plt.colorbar(s,ax=ax)
            lons = np.arange(lon_start, lon_stop, lon_step) 
            lats = np.arange(lat_start, lat_stop, lat_step)    
            xx, yy = np.meshgrid(lons,lats)
            #cbar=plt.colorbar(hist[3],ax=axs[i][j])
            #cbar.set_label('ship density[0-1]',size=14,)
            b1 = raster.GetRasterBand(1).ReadAsArray()
            #cf = ax.contourf(xx,yy,b1, transform=ccrs.PlateCarree(),vmin=0,vmax=5.0 * 10e-5,cmap='jet')
            mesh = ax.pcolormesh(lons,lats,b1, transform=ccrs.PlateCarree(),vmin=0,vmax=1.0 * 10e-5,cmap=cmap)

            ax.add_feature(cartopy.feature.LAND.with_scale('50m'),zorder=1,edgecolor='black',)
            gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                                     linewidth=1, color='black', alpha=0.5, linestyle='--')
            

            #s = ax.scatter(df.LON, df.LAT, c=z, s=0.5,cmap ='jet',vmin=0,vmax=0.05)
            # land , grid line 描画

            gl.xlabels_top = False
            gl.ylabels_left = False
            gl.xformatter = LONGITUDE_FORMATTER
            gl.yformatter = LATITUDE_FORMATTER
            gl.xlabel_style = {'size': 15, 'color': 'gray'}
            gl.ylabel_style = {'size': 15, 'color': 'gray'}
            
            print(dates[c])            

            ax.set_title(dates[c]+'',fontsize=16)
            c = c + 1



    fs_suptitle  = 20
    fs_title     = 16
    fs_graticule = 12
    fs_cbar      = 16
    
    vmin, vmax = 0,1.0*10e-5      ## colormap's range
    cmap = cmap
    #ticks = [0,0.02,0.04,0.06,0.08,0.1]
    ticks = [0,2.0*10e-5,4.0*10e-5,6.0*10e-5,8*10e-5,5*10e-5]
    ticklabels = ticks           ## labels of colorbar

    # prepare boundaries of colorbar
    #cnorm = np.linspace(vmin,vmax,100)
    #cnorml = colors.BoundaryNorm(cnorm,256)

    # make dummy field and remove labels and measures
    ax = fig.add_axes([0.1,0,0.8,0.4])
    ax.patch.set_facecolor('None')
    for loc in ['left','right','top','bottom']:
        ax.spines[loc].set_visible(False)
        
    ax.tick_params(axis='x',top='off',bottom='off',labelbottom='off',colors='white',grid_color='white',labelleft='off',labelright='off')
    ax.tick_params(axis='y',left='off',right='off',labelleft='off',colors='white',grid_color='white')

    # make mappable object for colorbar
    #norm = cmap.Normalize(vmin=vmin,vmax=vmax)
    #mappable = ScalarMappable(norm,cmap)
    #mappable._A = []

    # draw common colorbar
    cb = fig.colorbar(mesh,ax=ax,aspect=50,pad=0.08,shrink=0.8,
                      orientation='horizontal')
    #cb.ax.tick_params(labelsize=fs_cbar)
    #cb.set_ticks(ticks)
    #cb.set_ticklabels(ticklabels)

    cb.set_label('NO2_column_number_density mol/m^2',size=14)
    plt.savefig('no2_extent16.png',bbox_inches="tight")
    
    plt.clf()
    plt.close()

    return 0 

if __name__ == '__main__':
    main()
    
