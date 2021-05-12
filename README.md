# Create_Points_Along_A_Line_Feature_Class
ArcGIS 10.x and Python 2.7
An ArcGIS 10.7 Toolbox tool is included with this script for easy use in ArcGIS.
Takes a line feature class in a Cartesian CRS and creates a new feature class of points at user defined intervals.  The points are distributed along the input lines at equal interval distances.
Starting with the first node of a line record, a point is created at the start node position with a distance value of 0. Using the user-defined interval distance, a point is added at each graduation along the line. Each point is attributed with the total cumulative distance from the start node. Points are only created at interval distances so if a line segment is greater than the interval distance that portion of the line is not given a point. After completing the first record, the above process is repeated for the next record.

The division values are based on the lines projection, not the projection of the data frame.

This tool does not work with multi-part geometries, or geographically projected data. It was tested using WaSPN and UTM 10N projections.

![image](https://user-images.githubusercontent.com/68295520/118010141-96ba5600-b303-11eb-8a66-cffd7e7dcd6a.png)

