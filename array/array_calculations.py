import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import cmath
import math


def array_layout(stations):
    #Function to plot the array layout of infrasound station

    ####input
    #maximum range of both axis
    axis_limit = 1200
    #value you see beside of 0 on the axis e.g. (-500,0,500)
    axis_value = 500
    #name of the array (for title)
    array_name = 'IS18'
    #location of short lines on axis
    minor_ticks = [-1000,-750,-500,-250,0,250,500,750,1000]
    #save plot (0 (not save), 1 (save))
    save = 0
    ####

    #Preparing data
    x_stations = np.zeros(len(stations))
    y_stations = np.zeros(len(stations))
    for i in xrange(len(stations)):
        x_stations[i] = stations[i][0]
        y_stations[i] = stations[i][1]

    ######Plotting
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    plt.gca().set_aspect('equal', adjustable='box')

    plt.title(array_name, fontsize=18, fontweight='bold')
    plt.plot(x_stations,y_stations,'ko',markersize=10)

    plt.xlabel('x(m)',size=18, fontweight = 'bold')
    plt.ylabel('y(m)',size=18, fontweight = 'bold')

    plt.xlim(-axis_limit,axis_limit)
    plt.ylim(-axis_limit,axis_limit)
    
    # size and length of ticks
    ax.xaxis.set_tick_params(width=1, length=8., which='major', labelsize=15)
    ax.xaxis.set_tick_params(width=1, length=4., which='minor')
    ax.yaxis.set_tick_params(width=1, length=8., which='major', labelsize=15)
    ax.yaxis.set_tick_params(width=1, length=4., which='minor')

    # ticks (values on axis)
    ax.set_xticks([-axis_value,0,axis_value])
    ax.set_xticks(minor_ticks,minor=True)
    ax.set_yticks([-axis_value,0,axis_value])
    ax.set_yticks(minor_ticks,minor=True)

    #plt.grid(b=True, which='minor', linestyle='-')
    fig.tight_layout()
    if save==1:
        print 'Array_layout is saved'
        plt.savefig('Array_layout.png')
    else: 
        plt.show()

def array_distance_angle_elements(stations):
    # Function to plot a distance angle plot on an array

    ####input
    #axis limits
    x_min= 900
    x_max = 1300
    y_min = 0
    y_max = 190
    #values on axis
    x_axis_values = [1000,1100,1200]
    y_axis_values = [50,100,150]
    # small ticks (lines) on axis
    minor_ticks_x = [950,1000,1050,1100,1150,1200,1250]
    minor_ticks_y = [25,50,75,100,125,150,175]
    #save plot (1 is save, 0 is not save)
    save = 0
    ####

    #Preparing data
    distance = []
    angle = []

    x_stations = np.zeros(len(stations))
    y_stations = np.zeros(len(stations))
    for i in xrange(len(stations)):
        x_stations[i] = stations[i][0]
        y_stations[i] = stations[i][1]


    #Calculation distance and angle
    for i in range(len(stations)):
        for j in range(len(stations)):
            if i!=j:
                distance.append(np.sqrt((x_stations[i]-x_stations[j])**2+(y_stations[i]-y_stations[j])**2))

                angle.append(abs(np.degrees(np.arctan2((y_stations[i]-y_stations[j]),(x_stations[i]-x_stations[j])))))

    ##Plot of Angle and Distance between each element of the array
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    plt.plot(distance,angle,'ko',markersize=10)
    
    plt.xlim(x_min,x_max)
    plt.ylim(y_min,y_max)

    plt.xlabel('Distance (m)',size=18, fontweight='bold')
    plt.ylabel('Angle (deg)', size=18, fontweight='bold')
 
    # size and length of ticks
    ax.xaxis.set_tick_params(width=1, length=8., which='major', labelsize=15)
    ax.xaxis.set_tick_params(width=1, length=4., which='minor')
    ax.yaxis.set_tick_params(width=1, length=8., which='major', labelsize=15)
    ax.yaxis.set_tick_params(width=1, length=4., which='minor')

    # ticks (values on axis)
    ax.set_xticks(x_axis_values)
    ax.set_xticks(minor_ticks_x,minor=True)
    ax.set_yticks(y_axis_values)
    ax.set_yticks(minor_ticks_y,minor=True)

    #plt.grid(b=True, which='minor', linestyle='-')
    fig.tight_layout()

    if save==1:
        print 'Distance_Angle_plot is saved'
        plt.savefig('Array_layout.png', format='png')
        plt.close(fig)
    else: 
        plt.show()
        plt.close(fig)
   

def array_response(stations, frequency):
    
    ###input

    slowness_grid_limits = 0.005
    grid = 1000

    # save plot (1 (save), 0 (not save)) 
    save = 1




    ##slowness grid


    ###
    
    number_stations = len(stations)
    slowness = np.linspace(-slowness_grid_limits,slowness_grid_limits,grid)
    array_response = np.zeros((len(slowness),len(slowness)),dtype = np.complex)

    
    # Calculate array response
    for i in xrange(len(slowness)):
        for j in xrange(len(slowness)):
            R_sum = 0.
            for st in xrange(number_stations):
                R_sum = R_sum + cmath.exp(-(1.j)*2*np.pi*frequency*((slowness[j]*stations[st][0])+slowness[i]*stations[st][1]))
            array_response[i][j] = (abs((1./number_stations)*R_sum))**2

    #####

    ###Plot - Array Response at p_y = 0 line
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    
    plt.plot(slowness,array_response[len(slowness)/2][:], linewidth=3.0, color="k")
    plt.grid()
    plt.xlim(min(slowness),max(slowness))
    plt.ylim(-0.2,1.2)
    plt.xlabel(r"$p_x (s/m)$", size=18)
    plt.ylabel("Response", size=18, fontweight='bold')

    fig.tight_layout()
   
    if save==1:
        print 'Array_Response_Line is saved'
        plt.savefig('Array_Response_Line.png', format='png')
        plt.close(fig)
    else: 
        plt.show()
        plt.close(fig)
   

   
   #####

    ###Plot - Array response in slowness grid
    fig,ax = plt.subplots()
    
    #calculation radius
    radius = 1./340.
    circle1 = plt.Circle((0, 0), radius, color='k',fill=False, linewidth=3.0)

    #range of colorbar
    v = np.linspace(0,1,11, endpoint=True)

    #plot
    pl3 = plt.contourf(slowness, slowness, array_response,v)
    plt.grid()
    ax.add_patch(circle1)
    c3 = plt.colorbar(pl3)

    #plot box with used frequency value
    ax.text(0.0018, -0.0042, '%s Hz' %(frequency),fontsize=18,fontweight='bold', color='black', bbox=dict(facecolor='white', edgecolor='black', pad=15.0))

    #plot labels
    plt.xlabel("$p_x \ (s/m)$", size=25)
    plt.ylabel("$p_y \ (s/m)$", size=25)
    plt.gcf().subplots_adjust(bottom=0.15,left=0.2)

    frame1 = plt.gca()
    frame1.set_xticklabels([0.004,0.002,0,-0.002,-0.004])
    plt.show()
    plt.close(fig)


