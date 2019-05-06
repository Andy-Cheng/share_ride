# Share-ride routes
## Steps
Assume there're 8 cars appearing on the map at the same moment.

For **each car**:
1. Randomly choose a origin as a starting point.
2. If the number of passengers on the car is 3:
pick the nearst destination of passengers on the car.
3. If the number of passengers on the car is 0:
pick the nearst passengers in the region of the map.
4. Otherwise, pick a destination or a passenger with the minimum distance.

For **all the users**:
1. Cluster passengers on the map by the vectors(origin to destination).
2. For each groupe determined by the clustering described above, run the procedure for **each car**.

## Output
Eeach sheet in Excel is a route, including:
1. Each way point
2. Distances of each segment
3. Number of pasengers in each segment

## Routes on the map inex.html)
Ex.1
![](https://i.imgur.com/5KvKjVF.jpg)

Ex.2
![](https://i.imgur.com/e9nypm7.jpg)

## Improvement
1. Cluster passengers, and run the simulation afterwards.
2. Using random variables to model the total number of paris of (origin, destination) that served by a driver. (Possion distribution, Gamma distribution, etc.)

