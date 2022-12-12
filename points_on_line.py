try:
    import sys
    import traceback
    import math
    import arcpy
    
    
    
    arcpy.overwriteOutput = True
    arcpy.AddMessage("Create Points at User Defined Intervals Along a Line...")
    arcpy.AddMessage("Developed by the Lummi Nation GIS Division.  Gerry Gabrisch, geraldg@lummi-nsn.gov")
    
    
    def Distance(x1, y1, x2, y2):
        '''Cartisian distance formula'''
        return math.pow(((math.pow((x2-x1),2)) + (math.pow((y2 - y1),2))),.5)
    def CartetesianToPolar(xy1, xy2):
        '''Given coordinate pairs as two lists or tuples, return the polar coordinates with theta in radians'''
        x1 = xy1[0] * 1.0
        y1 = xy1[1] * 1.0
        x2 = xy2[0] * 1.0
        y2 = xy2[1] * 1.0
        xdistance = x2 - x1
        ydistance = y2 - y1
        distance = math.pow(((math.pow((x2 - x1),2)) + (math.pow((y2 - y1),2))),.5)
        theta = math.atan(ydistance/xdistance)
        return [distance, theta]
    def PolarToCartesian(polarcoords):
        'give a tuple or list of (distance, theta in radians) convert to cartesion coords'
        r = polarcoords[0]
        theta = polarcoords[1]
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        return [x, y]

    
    
    infc = arcpy.GetParameterAsText(0)
    divide_distance = float(arcpy.GetParameterAsText(1))
    outFC = arcpy.GetParameterAsText(2)
    
    
    
     
    ########################Read the current geometry....
    
    # Identify the geometry field
    desc = arcpy.Describe(infc)
    shapefieldname = desc.ShapeFieldName
    
    # Create search cursor
    rows = arcpy.SearchCursor(infc)
    
    # Write coordinate geometry to a list
    for row in rows:
        feat = row.getValue(shapefieldname)
        arcpy.AddMessage("Feature " + str(row.getValue(desc.OIDFieldName)) + ":")
        partnum = 0
        partcount = feat.partCount
        thisrecordsgeometry = [] 
        while partnum < partcount:
            arcpy.AddMessage("Part " + str(partnum) + ":")
            part = feat.getPart(partnum)
            pnt = part.next()
            pntcount = 0
            while pnt:
                thetuple = [pnt.X, pnt.Y]
                thisrecordsgeometry.append(thetuple)
                pnt = part.next()
                pntcount += 1
            partnum += 1
            arcpy.AddMessage(thisrecordsgeometry)
            #A list to hold the coordinate geometry of the line
            listofpointgeometry = []
            tuple1 = 0
            tuple2 = 1
            #Put a point at the start of the line
            listofpointgeometry.append(thisrecordsgeometry[0])
            running_distance = 0
            while tuple2 <= len(thisrecordsgeometry):
                x1 = thisrecordsgeometry[tuple1][0]
                y1 = thisrecordsgeometry[tuple1][1]
                x2 = thisrecordsgeometry[tuple2][0]
                y2 = thisrecordsgeometry[tuple2][1]
                distance = Distance(x1, y1, x2, y2)
                if distance >= divide_distance:
                    polarcoord = CartetesianToPolar(thisrecordsgeometry[tuple1], thisrecordsgeometry[tuple2])
                    newpolarcoord = [polarcoord[0] + divide_distance,polarcoord[1]]
                    adjustvalue = PolarToCartesian(newpolarcoord)
                    x = x1 + adjustvalue[0]
                    y = y1 + adjustvalue[1]
                    listofpointgeometry.append([x,y])
                if distance < divide_distance:
                    running_distance = running_distance + distance
                    tuple1 += 1
                    tuple2 += 1
   
    ##########      Now Write the Geometry
    # A list of features and coordinate pairs
    coordList = listofpointgeometry
    # Create empty Point and Array objects
    point = arcpy.Point()
    array = arcpy.Array()
    # A list that will hold each of the Polyline objects 
    featureList = []
    for feature in coordList:
        # For each coordinate pair, set the x,y properties and add to the Array object
        for coordPair in feature:
            point.X = coordPair[0]
            point.Y = coordPair[1]
            array.add(point)
    
        # Create a Polyline object based on the array of points
        polyline = arcpy.Polyline(array)
    
        # Clear the array for future use
        array.removeAll()
    
        # Append to the list of Polyline objects
        featureList.append(polyline)
    
    arcpy.CopyFeatures_management(featureList, "tempoutFC")
    arcpy.SplitLineAtPoint_management(infc,"tempoutFC",outFC)
        

    arcpy.AddMessage("Create Points Along Line - finished without error")       
   
except:
    # Get the traceback object
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]

    # Concatenate information together concerning the error into a message string
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"

    # Return Python error messages for use in script tool or Python window
    arcpy.AddError(pymsg)
    arcpy.AddError(msgs)

    # Print Python error messages for use in Python / Python window
    print(pymsg)
    print(msgs)











    
