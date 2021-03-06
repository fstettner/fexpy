# -*- coding: utf-8 -*-

'''
Code for the calculation of the Fisher ratio and SNR of infrasound data
Felix Stettner April 2018
'''

import obspy
import numpy as np
import math
import matplotlib.pyplot as plt
import obspy.signal as signal
from obspy.signal.cross_correlation import correlate
from obspy import read

def fisher_calculator(st): 
        #input obspy stream

        #st = obspy.read("/db/2017/001/IS37/IS372017-001_01.00.wfdisc")
        #st = st.select(id=".I37H*..BDF")
        
        bin_data = np.zeros((len(st),len(st[0])))
        for t in range(len(st)):
            bin_data[t] = st[t].data
         
        ################################################
        ################### functions ##################
        ################################################
        def fisher_calc(bin_data):
            #first sum in denominator
            sum1 = np.sum(np.square(np.sum(bin_data, axis = 0)))
            #second sum in denominator
            sum2 = np.square(np.sum(np.sum(bin_data,axis=0)))
            #first sum numerator
            sum3 = np.sum(np.sum(np.square(bin_data), axis = 0))
            #second sum numerator
            sum4 = np.sum(np.square(np.sum(bin_data,axis=0))) 
 
            len_bin = float(bin_data.shape[1])
            pre_factor = (len_bin*(len(st)-1))/(len(st)*(len_bin-1))
            fisher = pre_factor*((sum1-(1./len_bin)*sum2)/(sum3-(1./len(st))*sum4))
            return fisher

        ################################################
        ################## main ########################
        ################################################

        #calculation fisher
        fisher = fisher_calc(bin_data)
        #print ('Fisher: ' + str(fisher))
        return fisher

def snr_calculator(st):
    fisher = fisher_calculator(st) 
    print (fisher) 
    number_of_array_elements = len(st)

    if fisher>1:
        snr = np.sqrt((fisher-1)/number_of_array_elements)
    else:
        snr = 'Too low snr (Fisher<1)'

    print (snr)

def align(st, year, julday, hour, minute, second, window_length, lon_station, lat_station, app_velocity, back_azimuth):
    
    signal_starttime = obspy.UTCDateTime(year=year, julday=julday, hour=hour, minute=minute, second=second)
    data_start = obspy.UTCDateTime(year=year, julday=julday, hour=0, minute=0, second=0)
    start_sample = int((signal_starttime-data_start)/st[0].stats.sampling_rate)

    bin_data = np.zeros((len(st), window_length*int(st[0].stats.sampling_rate)))

    p = 1./app_velocity
    px = p*np.cos(back_azimuth)
    py = p*np.sin(back_azimuth)
    
   #transformation lon/lat in x/y
    x_list = []
    y_list = []
    for i in range(len(lat_station)):
        x,y = signal.util.util_geo_km(lon_station[0],lat_station[0],lon_station[i],lat_station[i])
        x_list.append(x*1000)
        y_list.append(y*1000)

    #allignment
    for t in np.arange(len(st)):
        ssi = start_sample - int((px*x_list[t]+ py*y_list[t])*st[0].stats.sampling_rate)
        esi = ssi + window_length*int(st[0].stats.sampling_rate)
        bin_data[t] = st[t].data[ssi:esi]
        plt.plot(bin_data[t])

    plt.xlabel("Time [s]", fontsize=17, fontweight='bold')
    plt.ylabel("Pressure [Pa]", fontsize=17, fontweight='bold')
    plt.show()
    return st



def tdoa(st):
    times = []
    for i in range(len(st)):
        cc = signal.cross_correlation.correlate(st[i],st[0],100)
        shift, value = signal.cross_correlation.xcorr_max(cc)
        #print shift
        #print value
        
        #print st[0].stats.sampling_rate
        times.append(shift/st[0].stats.sampling_rate)
    return times

def inverse_localisation(st, array):
    
    velocity = 340
    time_list = tdoa(st)

    station_list = array
   
    #build up matrix A
    A = np.zeros((len(station_list)-1,4))
    for i in range(1,len(station_list)):
        A[i-1,0] = station_list[0][0] - station_list[i][0] 
        A[i-1,1] = station_list[0][1] - station_list[i][1]
        A[i-1,2] = station_list[0][2] - station_list[i][2]
        A[i-1,3] = time_list[i]*velocity

    #build up vector b
    b = np.zeros(len(station_list)-1)
    for i in range(len(station_list)-1):
        b[i] = 0.5*((time_list[i+1]*velocity)**2-station_list[i+1][0]**2+station_list[0][0]**2-station_list[i+1][1]**2+ \
                station_list[0][1]**2-station_list[i+1][2]**2+station_list[0][2]**2)

    A_pseudo = (np.linalg.inv(A.transpose().dot(A))).dot(A.transpose())
    x = A_pseudo.dot(b)
    print ('############################################')
    print ("Calculated location in m: %g m  %g m  %g m") %(x[0], x[1], x[2]) 
    lon, lat = signal.util.util_lon_lat(18.60763,69.07408, (x[0]/1000.), (x[1]/1000.))
    print ("Calculated location lon, lat: %g  %g ") %(lon,lat) 
    

    # plot solution
    # plot in a x/y grid
    for i in range(len(station_list)):
        plt.plot(station_list[i][0],station_list[i][1], "ro")
    
    plt.plot(x[0],x[1],"go")
    plt.axis('equal')
    plt.xlabel('x-coordinates [m]')
    plt.ylabel('y-coordinates [m]')
    plt.show()


def forward_localisation(st,array):

    station_list = array    
    window_length_fisher = 5
    length_of_signal = 20*20
    velocity = 340
    sampling_rate = st[0].stats.sampling_rate


    # make grid for forward-problem
    x_grid=np.linspace(-3000,3000,30)
    y_grid=np.linspace(-3000,3000,30)

    fisher_all = np.zeros((len(x_grid),len(y_grid)))
    n_samples = int(length_of_signal*sampling_rate)
    n_window =(window_length_fisher*st[0].stats.sampling_rate)
    bin_data = np.zeros((len(st), int(n_window)+1))

    fisher_list = []
    source_x = []
    source_y = []

    n_long = st[0].stats.npts
    n = n_long/(window_length_fisher*st[0].stats.sampling_rate)

    for t in range(1,int(n)-1):
        print "Run:  %d. out of %d runs" %(t,int(n)-2)
        t_start = st[0].stats.starttime+t*window_length_fisher 
        t_end = t_start+window_length_fisher
        
        #calculation for one time
        fisher_old = 0
        fisher = 0
        x_old = 0
        y_old = 0
        source_old = 0
        
        bin_data = np.zeros((len(st), int(n_window)+1))
        for x in range(len(x_grid)):
            for y in range(len(y_grid)): 
                source = [x_grid[x],y_grid[y],0]
                st2 = obspy.Stream()
                for i in range(0,len(station_list)):
                    time = (np.sqrt((source[0]-station_list[i][0])**2+(source[1]-station_list[i][1])**2+(source[2]-station_list[i][2])**2) \
                    -(np.sqrt((source[0]-station_list[0][0])**2+(source[1]-station_list[0][1])**2+(source[2]-station_list[0][2])**2)))/velocity
                    st[i].stats.sampling_rate = sampling_rate
                    st2.append((st[i].slice(t_start+time,t_start+window_length_fisher+time)))
                    #bin_data[i] = (st[i].slice(t_start+time,t_start+window_length_fisher+time)).data

                    #plt.plot(bin_data[i])
                #plt.show()
                fisher = fisher_calculator(st2)

                #print fisher
                if fisher>fisher_old:
                    fisher_old = fisher
                    source_old = source
                 
        #print source_old[0]
        source_x.append(source_old[0])
        source_y.append(source_old[1])
        fisher_list.append(fisher_old)
 
    return source_x, source_y, fisher_list



def qtau(st, array):
    time_list = tdoa(st)
    station_list = array
   
    ##########################################
    # Code for Qtau calculation based on TDOA (Time-Difference-of-Arrival)
    ##########################################

    # Sampling Rate
    sampling_rate = st[0].stats.sampling_rate

    N = int(len(station_list)*(len(station_list)-1)/2.)
    time_delay = np.zeros((N))
    X = np.zeros((N,2))
            
    #Time-Delay Compared to Array Element 1
    row = 0
    for t1 in range(len(station_list)-1):
        for t2 in range(t1+1,len(station_list)):
            X[row,0] = station_list[t1][0]-station_list[t2][0] 
            X[row,1] = station_list[t1][1]-station_list[t2][1] 
            time_delay[row] = time_list[t1]-time_list[t2]
            row = row + 1

    ##########################################
    ##### Algorithm for Qtau Calculation #####
    ##########################################

    C = np.dot(X.transpose(),X)
    R = np.dot((np.dot(X,np.linalg.inv(C))),X.transpose())
    I = np.identity(N)

    q = np.sqrt((np.dot(time_delay, np.dot((I-R),time_delay)))/(N-np.linalg.matrix_rank(R)))
    Q_tau = q*sampling_rate

    ##########################################
    #Output
    print ("Calculated Qtau-value: %.2g") %Q_tau
    print ('############################################')
