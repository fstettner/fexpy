# Module to import station locations

def import_array(name):

    if name=='NL':
        #NL
        array = [[-80.0,85.0],[80.0,48.0],[62.0,-89.0],[-82.0,-69.0],[0.0,0.0],[194.0, 565.0],[407.0,-427.0],[-699.0,-33.0]]

    elif name=='IS18':
        #station data IS18
        station_1 = [0,0,53.]
        station_2 = [160.0725,-29.0267, 71.]
        station_3 = [143.1280,-171.9277, 46.]
        station_4 = [-1.2109,-154.0650, 50.]
        station_5 = [79.1900,-77.0325, 87.]
        station_6 = [269.7245,494.5711, 140.]
        station_7 = [482.2352,-503.5024, 30.]
        station_8 = [-621.4199,-116.1070, 47.]
        array=[station_1, station_2, station_3, station_4, station_5, station_6, station_7, station_8]

    elif name=='IS37':
        #station IS37
        station_1 = [0,0,779]
        station_2 = [44.659,189.636,754]
        station_3 = [213.738,-85.89,812]
        station_4 = [-188.218,-118.243,795]
        station_5 = [568.98,425.008,737]
        station_6 = [275.49,899.097,713]
        station_7 = [1069.008,278.876,821]
        station_8 = [253.241,-584.525,667]
        station_9 = [-771.659,-401.582,741]
        station_10 = [-615.64,335.767,641]
        array=[station_1, station_2, station_3, station_4, station_5, station_6, station_7, station_8, station_9, station_10]


    return array
