# coding=utf-8
""" Algorithms for the surgery evaluation application """

from numpy import inf
def point_in_locator(point, point_locators, radius=1.0):
    """ 
    Tests whether a point is within a set distance of any of a 
    list of point locators.

    :param point: the point to test, in 3D (x,y,z)
    :param point_locators: a list of vtkPointLocators
    :param radius: optional search radius in mm (default=1.0)
    :return locator: the index of the nearest point locator, (-1 if no locators within radius)
    :return distance: distance to nearest point_locator

    :raises: delegates to vtk
    	
    """

    minumum_distance = numpy.inf
    locator_index = -1
    for index, locator in enumerate(point_locators):
        
	distance = vtk.mutable(0.0)
	if locator.FindClosestPointWithinRadius(radius,point,distance) == -1:
	    continue
       
    	if distance > mimumum_distance:
	    continue

    	minumum_distance = distance
	locator_index = index

    return locator_index, minumum_distance


           inside=pl.FindClosestPointWithinRadius(5.0,(0.0,0.0,0.0),distance)
    reader = vtk.vtkSTLReader()
    reader.SetFileName('phantom_patch_00.stl')

    reader.Update()
    source = reader.GetOutput()
    pl = vtk.vtkPointLocator()
    #this builds the point locator, which could be time consuming for a large set, 
    #we want to pass it
    pl.SetDataSet(source)

    #This isn't very useful, it returns the ID of the closest point
    pl.FindClosestPoint(0,0,0)


    #this gives us -1 if no points are within the radius 
    #otherwise gives the point id

    return input_x + input_y
