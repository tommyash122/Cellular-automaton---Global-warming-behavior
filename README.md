
## About
This cellular automaton simulates a model of the Earth.
Earth, as we know, is in a state of global warming.
This model reflects how a small pollutant factor can have a general impact on the entire system, and how fragile this whole system is.

https://youtu.be/LI2y7nXF51g    
Link to a short video explaining the running of the automaton with two pollution factors, viewing the outputs differences and explanation of how I get the data.
(Hebrew)


https://youtu.be/eANeSECg19w  
Link to a video that comprehensively explains the code and all its functions and components.
(Hebrew)        

**Check out the [Global warming behavior](#Data-and-conclusions) that this automaton shows.**

## System requirements 
1) Python 3.4 and above installed.
2) files main.py and my_map.txt needs to be on the same folder.


134th day's pic:
![image](https://user-images.githubusercontent.com/84855441/201136668-30f81c2a-df3b-425f-a2aa-8b2f6580db67.png)


## Explanation

The automaton is a cellular automaton that contains many cells of different types that are categorized according to the colors.
  #### type
  - `Sea` - Blue
  - `Iceberg` - White
  - `Forest` - Green
  - `City` - Yellow
  - `Land` - Brown
  
  #### temperature
  The number that appears on each cell represents the current temperature of that cell.    
  Randomly determined within predetermined ranges by cell type. If our cell is a glacier then the range will be [-25,-15] else [20,30].    
  
  #### air pollution
  We will express the degree of air pollution in percentages as a real number ranging from 0 to 1 where 0 is 0% pollution and 1 is 100% polluted. 
  Air pollution comes exclusively from a city-type cell and each cell produces a component of **0.01 (that can be changed)**  
  that adds to current air pollution level per day. 
  In our automaton there is an element of wind, We'll go into more detail about it later, and the same wind transmits the pollution to all the cell neighbors.  
  
  #### wind
  Our automaton has an element of wind with strength and direction. 
  Each cell, depending on its type, has a different wind strength between 0 and 1 randomly chosen corresponding to that type of cell.   
  For `land` and `city` the range is between 0 and 1 (Do not produce strong winds).   
  For a `forest`, the range is between 0.2 and 1 (A forest produces oxygen which creates a chance for strong wind).   
  For the `sea` the range is between 0.3 and 1 (the sea is an open area that produces a lot of wind).   
  For a `iceberg` the range is between 0.4 and 1 (a iceberg produces strong wind with a high probability).    
  
  Now the direction of the wind is determined by the clock-wise method, for each cell randomly choose a number between 0 and 11.99 representing its direction 
  and according to the number that came out the direction of the wind will be determined according to how this number is placed on a dial clock.  
  For each cell, we will scan all 8 of its neighbors in the cyclic form (if the cell is located at one end of the matrix, then its neighbor will  
  be at the other end respectively), a PIVOT axis will be determined that represents at a given moment the central pointing direction of each neighbor 
  in the matrix to our cell, if the wind direction chose for the neighbor is not In our direction we will not refer.  
  Otherwise, we calculate the distance of the direction from the center of the axis in percentages and multiply the result by the strength of the wind 
  and the strength of the air pollution and in addition by the temperature of the cell and accordingly we calculate for each neighbor how much it pollutes 
  us and how much it cools/heats us respectively. 
  
  #### clouds and rain
  In addition, our automaton has an element of clouds and rain.    
  Each cell, depending on its type, has a chance of cloud accumulation and depending on the degree of accumulation, the chance of rain increases and its intensity.    
  The rain was defined to be such that it lowers the degree of air pollution according to its intensity.    
  The degree of accumulation of clouds, like wind, will be randomly graded with ranges between 0 and 1 where 0 is 0% cloudiness and 1 is 100% cloudiness.    
  For `land`, the range is between 0 and 0.8 (low chance of rain).    
  For the `city`, the range is between 0.2 and 1 (reasonable chance of heavy rain).    
  For the `forest`, the range is between 0.3 and 1 (the humidity of the forest leads to a high chance of rain).    
  For the `sea`, the range is between 0.3 and 1 (the sea brings with it high humidity = high chance of rain).    
  For the `iceberg`, the range is between 0 and 0.6 (low chance of rain in glacier areas **read on Wikipedia**).    
  
  Accumulation of clouds of =< 0.9 will lead to dividing the future air pollution by 1.6 and a direct lowering of the temperature by 0.01 degrees.    
  An accumulation of =< 0.7 will lead to the division of future air pollution by 1.4 and a direct lowering of the temperature by 0.005 degrees.    
  An accumulation of =< 0.5 will lead to the division of future air pollution by 1.2 and a direct lowering of the temp by 0.002 degrees.    
  
  
  ### Daily update course:
  Every day our automaton will update its values in each and every cell.    
  If the air pollution in our cell is equal to or above **0.7**, we will raise the temperature gradually -    
  • If the current temperature is below 35 degrees, we will add to it the degree of pollution divided by 2.    
  • If the current temperature is above 35 and below 70, we will add the degree of contamination divided by 8.    
  • If the current temperature is 70 or higher, we will add to it the degree of pollution divided by 32.    
  This method of operation allows us to moderate the increase of raising temperatures because if a cell is already at a high temperature at the moment,
  the degree of contamination affects it less.    
  Otherwise, the degree of air pollution is lower than that the cell will balance itself and add/subtract 0.1 degrees to itself in striving for the stable    
  temperature defined for it. (-20 iceberg otherwise 25).    
  Cells that reach any temperature or air pollution level first change color (an indication that the cell is changing) and after the next level change their type.    
  • A Land will change its color to red, boiling soil, at 120 and beyond.    
  • A city will change its color above 55 degrees and also above pollution of above 0.5 and will turn into land above 80 degrees.    
  • A forest will change its color above 0.3 pollution level and will die and turn into land at pollution of 1 or above 60 degrees.    
  • Sea will change its color if the temperature is above 40 and also the pollution is above 0.4 and will evaporate to the land above 100 degrees.    
  • A iceberg will melt above 0 degrees and turn into a sea.    
  
  ## Data and conclusions
  After a number of experiments it was found that the value of the pollution factor (air pollution factor) for which the system was found to be stable
  but not static is **0.01**.    
  
  We will now present the data found after running the model for "365 days":    
  `TEMPERATURE STATUS -   Max= 64.13   Min= -25.00	AVG= 22.60   Std_dev= 10.93`    
  `AIR POLLUTION STATUS - Max= 1.00	   Min= 0.00	  AVG= 0.29    Std_dev= 0.23`    
  
  ### We will present a graph that tracks the values of the parameters throughout the year:
  #### Graph that tracks the average temperature for each day of the year    
  ![image](https://user-images.githubusercontent.com/84855441/201158787-3e5bbe0a-ab36-4631-ab11-67ff42bee67e.png)    
  
  #### Graph that tracks the average air pollution every day of the year:    
  ![image](https://user-images.githubusercontent.com/84855441/201160134-ce3a614d-4094-4fbc-8f59-678db09fc577.png)    
  
  ### We will now present a graph with standardized data when specifying the aforementioned standard for:    
  **Temperature -> 10.93**    
  **Air pollution -> 0.23**    
  ![image](https://user-images.githubusercontent.com/84855441/201160443-08814e15-12bb-4010-b453-826e276ad0d4.png)        
  
  ![image](https://user-images.githubusercontent.com/84855441/201160508-128f4ff1-b9e5-4064-b4e7-59b2fdc52dba.png)            
  
  There is a clear correlation (adjustment) between the air pollution and the effect on the other variables in the system throughout the year    
  because after running the system with an air pollution factor of 0 it was found that the data will be:    
  `TEMPERATURE STATUS -Max= 30.00	Min= -25.00	AVG= 19.13	Std_dev= 15.14`    
  `AIR POLLUTION STATUS -Max= 0.00	Min= 0.00	AVG= 0.00	Std_dev= 0.00`    
  
  And according to the data presented for a pollution factor of **0.01**, the average annual temperature was **22.6** compared to **19.13**, which is an increase
  of **18.139%** (percentages), which means that all the cells in the system heat up on average to some extent and this clearly indicates that there is a clear
  effect of air pollution on the entire system.    

  Now we will perform a test of the system's sensitivity to the air pollution parameter that we have, we will leave all the parameters the same and slightly
  increase our air pollution parameter and examine the results.
  As mentioned in the first experiment, the value of our air pollution parameter was **0.01** We will now increase to **0.011** and get the following data:
  
  `TEMPERATURE STATUS -Max= 62.48	Min= -25.00	AVG= 22.81	Std_dev= 10.66`    
  `AIR POLLUTION STATUS -Max= 1.00	Min= 0.00	AVG= 0.29	Std_dev= 0.23`    
  
  First we will prove that for a pollution factor of **0.01** the average annual temperature was **22.6** and now when we raised the pollution factor to **0.011**, which 
  is an increase of only **10%** (percent), our global average temperature is now **22.81** which is an increase of **0.93%** ( percent) which means almost an increase of
  **1%** in the average degrees, which is a significant increase in the average temp.    
  
  Below we will present the difference between the annual average temperatures with the differnt factors:    
  ![image](https://user-images.githubusercontent.com/84855441/201163504-c7673239-21ab-4c20-b697-8ec501fba172.png)

  It can be seen that the blue line representing the sample with a factor of **0.011** begins to go above the sample with a factor of **0.01** towards approximately day 
  80 and from there until the end of the year it remains above it.    
  
  For the annual average level of air pollution, it can be proven that:    
  ![image](https://user-images.githubusercontent.com/84855441/201164133-f93ca1b4-4db3-4853-9471-d26f1d478093.png)    
  
  The degree of air pollution decreases and increases gradually in both factors, but the annual average of the **0.011** pollution factor is **0.2917776661**, while the 
  annual average of the **0.01** pollution factor is **0.2888955695**, which is an increase of **0.997%**, which means almost a **1%** increase in the annual air pollution average.    
  
  ## Summary
  In conclusion, it can be clearly established that our system is sensitive to air pollution, which means that a slight change in the amount of pollution emitted causes significant
  changes in the other components of the system and raises its general temperature and ultimately causes its destruction.    
  
  # Final conclusion: we need to protect our planet, it is too fragile.    
  ![gif](https://media.giphy.com/media/xTiTnDtaiN5cD21tQY/giphy.gif)


  



  
  
  
  
  
  
  
  

 
