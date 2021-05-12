try:
    import sys, arcpy, traceback, math
    arcpy.env.overwriteOutput = True
    print "A Two-Bit Algorithms product\n\nCopyright\
    2011 Gerry Gabrisch\n\ngerry@gabrisch.us"
    
    #infc = arcpy.GetParameterAsText(0)
    #divide_distance = arcpy.GetParameterAsText(1)
    #number_of_graduations = arcpy.GetParameterAsText(1)
    #output_file = arcpy.GetParameterAsText(2)
    
    infc = r"Z:\GISpublic\GerryG\GISDefault.gdb\TestData"
    number_of_graduations = 3
    output_file = r"Z:\GISpublic\GerryG\GISDefault.gdb\TestPoints"
    point_at_zero = False
    
    number_of_graduations = float(number_of_graduations)
    
    arcpy.env.outputCoordinateSystem = infc
    
    
    def Distance(x1, y1, x2, y2):
        '''Cartesian distance formula'''
        return float(math.pow(((math.pow((x2-x1),2)) + (math.pow((y2 - y1),2))),.5))
    def CartesianToPolar(xy1, xy2):
        '''Given coordinate pairs as two lists or tuples, return the polar
        coordinates with theta in radians. Values are in true radians along the
        unit-circle, for example, 3.14 and not -0 like a regular python
        return.'''
        try:
            x1, y1, x2, y2 = float(xy1[0]), float(xy1[1]), float(xy2[0]), float(xy2[1])
            xdistance, ydistance = x2 - x1, y2 - y1
            distance = math.pow(((math.pow((x2 - x1),2)) + (math.pow((y2 - y1),2))),.5)
            if xdistance == 0:
                if y2 > y1:
                    theta = math.pi/2
                else:
                    theta = (3*math.pi)/2
            elif ydistance == 0:
                if x2 > x1:
                    theta = 0
                else:
                    theta = math.pi
            else:
                theta = math.atan(ydistance/xdistance)
                if xdistance > 0 and ydistance < 0:
                    theta = 2*math.pi + theta
                if xdistance < 0 and ydistance > 0:
                    theta = math.pi + theta
                if xdistance < 0 and ydistance < 0:
                    theta = math.pi + theta
            return [distance, theta]
        except:
            print"Error in CartesianToPolar()" 
    def PolarToCartesian(polarcoords):
        '''A tuple, or list, of polar values(distance, theta in radians)are
        converted to cartesian coords'''
        r = polarcoords[0]
        theta = polarcoords[1]
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        return [x, y]
    def gPrint(string):
        #print string
        arcpy.AddMessage(string)
 
 
 
 
  
  
  
  
    list_of_distance_values = []
    gPrint("Cracking Features")
    #Convert the dividing distance to a float for safety
    
    #Get the input line files geometry as a python list.
    desc = arcpy.Describe(infc)
    shapefieldname = desc.ShapeFieldName
    rows = arcpy.SearchCursor(infc)
    #A list to hold the coordinate geometry of the line
    listofpointgeometry = []
   
   
   
   
   
    for row in rows:
        counter = 0
        feet_remaining_list = []
        gPrint("Working on record " + str(counter))
        feat = row.getValue(shapefieldname)
        
        
        shape_length = row.getValue("Shape_Length")
        
        divide_distance = shape_length/number_of_graduations
        
        gPrint("Feature " + str(row.getValue(desc.OIDFieldName)) + ":")
        partnum = 0
        partcount = feat.partCount
        thisrecordsgeometry = []
        while partnum < partcount:
            part = feat.getPart(partnum)
            pnt = part.next()
            pntcount = 0
            while pnt:
                thetuple = [pnt.X, pnt.Y]
                thisrecordsgeometry.append(thetuple)
                pnt = part.next()
                pntcount += 1
            partnum += 1
            #Create a counter to track the position
            tuple2 = 1
            
            ##Point at 0???
            #if point_at_zero:
            #    listofpointgeometry.append(thisrecordsgeometry[0])
            #    point_counter = 0
            #else:
            #    point_counter = 1
                
    
            listofpointgeometry.append(thisrecordsgeometry[0])
            point_counter = 0 
                
            list_of_distance_values.append(point_counter * divide_distance)
            #Keep track of the distance use for each line segment
            running_distance = 0
            #Get the starting coordinate pairs...
            x1 = thisrecordsgeometry[0][0]
            y1 = thisrecordsgeometry[0][1]
            x2 = thisrecordsgeometry[tuple2][0]
            y2 = thisrecordsgeometry[tuple2][1]
            #Start adding points along the line.
            for item in thisrecordsgeometry:
                #gPrint("Working on Nodes " +  str(tuple2 - 1) + " to " + str(tuple2))
                try:
                    line_distance = Distance(x1, y1, x2, y2) + feet_remaining_list[counter-1]
                except:
                    line_distance = Distance(x1, y1, x2, y2)
                    
                #The line segment and the division are the same length...
                if line_distance == divide_distance:
                    listofpointgeometry.append([x2,y2])
                    point_counter += 1
                    list_of_distance_values.append(point_counter * divide_distance)
                    x1, y1 = x2, y2
                    tuple2 += 1
                    feet_remaining_list.append(0)
                    try:
                        x2 = thisrecordsgeometry[tuple2][0]
                        y2 = thisrecordsgeometry[tuple2][1]
                    except:
                        break
                    
                    
                #If there will be more than one division along this line or some remaining line   
                if line_distance > divide_distance:
                    #Calculate the number of nodes inserted on this line.
                    number_of_divisions = int(line_distance/divide_distance)
                    feet_remaining = (line_distance - (number_of_divisions * divide_distance))
                    #print feet_remaining
                    feet_remaining_list.append(feet_remaining)
                    polarcoord = CartesianToPolar((x1, y1), (x2, y2))
                    counter2 = 1
                    while counter2 <= number_of_divisions:
                        if len(feet_remaining_list) > 1:
                            newpolarcoord = [((divide_distance * counter2) - feet_remaining_list[counter-1]),polarcoord[1]]
                        else:
                            newpolarcoord = [((divide_distance * counter2)),polarcoord[1]]
                        adjustvalue = PolarToCartesian(newpolarcoord)
                        point_counter += 1
                        list_of_distance_values.append(point_counter * divide_distance)
                        listofpointgeometry.append([x1 + adjustvalue[0],y1 + adjustvalue[1]])
                        counter2 += 1
                    x1, y1 = x2, y2
                    tuple2 += 1
                    try:
                        x2 = thisrecordsgeometry[tuple2][0]
                        y2 = thisrecordsgeometry[tuple2][1]
                    except:
                        break   
                #If the line segment is less than the division value...    
                if line_distance < divide_distance:
                    if len(feet_remaining_list) < 1:
                        feet_remaining_list.append(line_distance)
                    else:    
                        feet_remaining_list.append(line_distance) 
                    x1, y1 = x2, y2
                    tuple2 += 1
                    try:
                        x2 = thisrecordsgeometry[tuple2][0]
                        y2 = thisrecordsgeometry[tuple2][1]
                    except:
                        break
                counter += 1
                
                
                
                
    gPrint("Writing New Geometry")
    point = arcpy.Point()
    pointGeometryList = [] 
    # For each coordinate pair, populate the Point object and create
    #  a new PointGeometry
    for pt in listofpointgeometry:
        point.X = pt[0]
        point.Y = pt[1]
        pointGeometry = arcpy.PointGeometry(point)
        pointGeometryList.append(pointGeometry)
    gPrint("Creating New Feature Class.")
    arcpy.CopyFeatures_management(pointGeometryList, output_file)
    arcpy.AddField_management(output_file, "distance", "DOUBLE")
    counter = 0
    rows = arcpy.UpdateCursor(output_file)
    for row in rows:
        row.distance = list_of_distance_values[counter]
        rows.updateRow(row)
        counter += 1
    gPrint("Done.")       
except arcpy.ExecuteError: 
    msgs = arcpy.GetMessages(2) 
    arcpy.AddError(msgs)  
    print msgs
except:
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
    arcpy.AddError(pymsg)
    arcpy.AddError(msgs)
    print pymsg + "\n"
    print msgs
    