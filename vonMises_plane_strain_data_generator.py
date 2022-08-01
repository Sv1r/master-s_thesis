from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
from xyPlot import *
from regionToolset import *
import displayGroupMdbToolset as dgm
import displayGroupOdbToolset as dgo

import random
import string
from array import *
import math
import numpy as np
import os        # Operating system
import shutil    # copying or moving files

max_iterations = 4728 # Set number of iterations
letters = string.ascii_lowercase
path = 'S:/Abaqus_data/'
inclusion_list = []
radius_list = []

for q in range (1, max_iterations + 1):
    sample_name = result_str = ''.join(random.choice(letters) for i in range(6))

    # LET'S CREATE MODEL
    mdb.Model(modelType=STANDARD_EXPLICIT, name='Model-' + sample_name)
    
    # LET'S CREATE PART
    mdb.models['Model-' + sample_name].ConstrainedSketch(name='__profile__', sheetSize=20.)
    mdb.models['Model-' + sample_name].sketches['__profile__'].rectangle(point1=(-10., 10.), 
        point2=(10.0, -10.0))
    mdb.models['Model-' + sample_name].Part(dimensionality=TWO_D_PLANAR, name='Part-1', type=
        DEFORMABLE_BODY)
    mdb.models['Model-' + sample_name].parts['Part-1'].BaseShell(sketch=
        mdb.models['Model-' + sample_name].sketches['__profile__'])
    del mdb.models['Model-' + sample_name].sketches['__profile__']
    mdb.models['Model-' + sample_name].ConstrainedSketch(gridSpacing=1.8, name='__profile__', 
        sheetSize=20, transform=
        mdb.models['Model-' + sample_name].parts['Part-1'].MakeSketchTransform(
        sketchPlane=mdb.models['Model-' + sample_name].parts['Part-1'].faces[0], 
        sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(0.0, 0.0, 0.0)))
    mdb.models['Model-' + sample_name].parts['Part-1'].projectReferencesOntoSketch(filter=
        COPLANAR_EDGES, sketch=mdb.models['Model-' + sample_name].sketches['__profile__'])

    max_incl = random.randint(5, 25)
    result_dict = {}
    while (len(result_dict) < max_incl):
        radius = random.uniform(.5, 1.) # radius of inclusion
        random_x = random.uniform(-(10. - 3. * radius), (10. - 3. * radius))
        random_y = random.uniform(-(10. - 3. * radius), (10. - 3. * radius))

        if len(result_dict.keys()) == 0:
            result_dict[radius] = (random_x, random_y)
        else:
            isPointIntersecting = False
            # To check if new inclusion intersects with any existing inclusions
            for r in list(result_dict.keys()):
                x, y = result_dict[r]
                distance = np.sqrt((random_x - x) ** 2 + (random_y - y) ** 2)
                    
                if distance < (3. * radius):
                    isPointIntersecting = True
                    break

            if (isPointIntersecting == False):
                result_dict[radius] = (random_x, random_y)


    for r in list(result_dict.keys()):
        x_coordinate, y_coordinate = result_dict[r]
        is_ellipse = random.uniform(0, 1.)
        if is_ellipse > .5:
            mdb.models['Model-' + sample_name].sketches['__profile__'].CircleByCenterPerimeter(
                center=(x_coordinate, y_coordinate),
                 point1=((x_coordinate - r), y_coordinate)
                 )

            mdb.models['Model-' + sample_name].parts['Part-1'].PartitionFaceBySketch(faces=
            mdb.models['Model-' + sample_name].parts['Part-1'].faces.findAt(((9.9, 
            9.9, .0), (.0, .0, 1.)), ), sketch=mdb.models['Model-' + sample_name].sketches['__profile__'])
        else:
            angle_1 = random.uniform(0, 180)
            angle_1_in_radians = angle_1 * np.pi / 180
            cos_1 = np.cos(angle_1_in_radians)
            sin_1 = np.sin(angle_1_in_radians)
            k_1 = r * sin_1
            k_2 = r * cos_1
            x_1 = x_coordinate + k_2
            y_1 = y_coordinate + k_1

            angle_2 = angle_1 + 90
            angle_2_in_radians = angle_2 * np.pi / 180
            cos_2 = np.cos(angle_2_in_radians)
            sin_2 = np.sin(angle_2_in_radians)

            k_3 = (r * random.uniform(.5, .75)) * sin_2
            k_4 = (r * random.uniform(.5, .75)) * cos_2
            x_2 = x_coordinate + k_4
            y_2 = y_coordinate + k_3

            mdb.models['Model-' + sample_name].sketches['__profile__'].EllipseByCenterPerimeter(
                center=(x_coordinate, y_coordinate),
                axisPoint1=(x_2, y_2),
                axisPoint2=(x_1, y_1))

            mdb.models['Model-' + sample_name].parts['Part-1'].PartitionFaceBySketch(faces=
                mdb.models['Model-' + sample_name].parts['Part-1'].faces.findAt(((9.9, 
                9.9, 0.0), (0.0, 0.0, 1.0)), ), sketch=mdb.models['Model-' + sample_name].sketches['__profile__'])
                    

    # LET'S CREATE MATERIAL-1 (MATRIX POLYMER)
    mdb.models['Model-' + sample_name].Material(name='Matrix')
    mdb.models['Model-' + sample_name].materials['Matrix'].Elastic(table=
        ((1e2, 0.47), ))
    # LET'S CREATE MATERIAL-2 (ELASTIC INCLUSION)
    mdb.models['Model-' + sample_name].Material(name='Elastic')
    mdb.models['Model-' + sample_name].materials['Elastic'].Elastic(table=
        ((1e3, 0.35), ))
    # LET'S CREATE SECTIONS    
    mdb.models['Model-' + sample_name].HomogeneousSolidSection(material='Matrix', name='Matrix', 
        thickness=None)
    mdb.models['Model-' + sample_name].HomogeneousSolidSection(material='Elastic', name='Inclusion', 
        thickness=None)
    # LET'S ASSIGN SECTIONS
    mdb.models['Model-' + sample_name].parts['Part-1'].SectionAssignment(offset=0.0, 
        offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
        faces=mdb.models['Model-' + sample_name].parts['Part-1'].faces.findAt(((9.9, 
        9.9, 0.0), (0.0, 0.0, 1.0)), )), sectionName='Matrix', 
        thicknessAssignment=FROM_SECTION)

    for r in list(result_dict.keys()):
        x_coordinate, y_coordinate = result_dict[r]   
        mdb.models['Model-' + sample_name].parts['Part-1'].SectionAssignment(offset=0.2, 
            offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
            faces=mdb.models['Model-' + sample_name].parts['Part-1'].faces.findAt((((x_coordinate), 
            (y_coordinate), 0.0), (0.0, 0.0, 1.0)), )), sectionName='Inclusion', 
            thicknessAssignment=FROM_SECTION)    
  
    # LET'S CREATE INSTANCE
    mdb.models['Model-' + sample_name].rootAssembly.DatumCsysByDefault(CARTESIAN)
    mdb.models['Model-' + sample_name].rootAssembly.Instance(dependent=OFF, name='Part-1-1', 
        part=mdb.models['Model-' + sample_name].parts['Part-1'])
 
    # LET'S CREATE STEP
    mdb.models['Model-' + sample_name].StaticStep(initialInc=0.01, maxInc=0.1, maxNumInc=10000, 
        minInc=1e-12, name='Step-1', previous='Initial')
    
    # LET'S CREATE BOUNDARY CONDITIONS
    mdb.models['Model-' + sample_name].Pressure(amplitude=UNSET, createStepName='Step-1', 
        distributionType=UNIFORM, field='', magnitude=-100.0, name='Load-1', region=
        Region(
        side1Edges=mdb.models['Model-' + sample_name].rootAssembly.instances['Part-1-1'].edges.findAt(
        ((5.0, 10.0, 0.0), ), )))
    
    mdb.models['Model-' + sample_name].Pressure(amplitude=UNSET, createStepName='Step-1', 
        distributionType=UNIFORM, field='', magnitude=-100.0, name='Load-2', region=
        Region(
        side1Edges=mdb.models['Model-' + sample_name].rootAssembly.instances['Part-1-1'].edges.findAt(
        ((10.0, -5.0, 0.0), ), )))

    mdb.models['Model-' + sample_name].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
        distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
        'BC-1', region=Region(
        edges=mdb.models['Model-' + sample_name].rootAssembly.instances['Part-1-1'].edges.findAt(
        ((-5.0, -10.0, 0.0), ), )), u1=UNSET, u2=0.0, ur3=UNSET)
    mdb.models['Model-' + sample_name].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
        distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
        'BC-2', region=Region(
        edges=mdb.models['Model-' + sample_name].rootAssembly.instances['Part-1-1'].edges.findAt(
        ((-10.0, 5.0, 0.0), ), )), u1=0.0, u2=UNSET, ur3=UNSET)
    
    # LET'S SEED THE INSTANCE    
    mdb.models['Model-' + sample_name].rootAssembly.seedPartInstance(deviationFactor=0.1, 
        minSizeFactor=0.1, regions=(
        mdb.models['Model-' + sample_name].rootAssembly.instances['Part-1-1'], ), size=0.2)
    
    # LET'S SET ELEMENT TYPE
    for r in list(result_dict.keys()):
        x_coordinate, y_coordinate = result_dict[r] 
        mdb.models['Model-' + sample_name].rootAssembly.setElementType(elemTypes=(ElemType(
            elemCode=CPE4R, elemLibrary=STANDARD), ElemType(elemCode=CPE3, 
            elemLibrary=STANDARD)),regions=(
            mdb.models['Model-' + sample_name].rootAssembly.instances['Part-1-1'].faces.findAt(((
            (x_coordinate), (y_coordinate), 0.0), )), ))        
    
    mdb.models['Model-' + sample_name].rootAssembly.setElementType(elemTypes=(ElemType(
        elemCode=CPE4R, elemLibrary=STANDARD), ElemType(elemCode=CPE3, 
        elemLibrary=STANDARD)),  regions=(
        mdb.models['Model-' + sample_name].rootAssembly.instances['Part-1-1'].faces.findAt(((
        9.9, 9.9, 0.0), )), ))
    
    # LET'S GENERATE MESH
    mdb.models['Model-' + sample_name].rootAssembly.generateMesh(regions=(
        mdb.models['Model-' + sample_name].rootAssembly.instances['Part-1-1'], ))    

    # LET'S CREATE SETS FOR EDGES
    mdb.models['Model-' + sample_name].rootAssembly.Set(edges=
        mdb.models['Model-' + sample_name].rootAssembly.instances['Part-1-1'].edges.findAt(((
        -5.0, -10.0, 0.0), )), name='BottomEdge')
    mdb.models['Model-' + sample_name].rootAssembly.Set(edges=
        mdb.models['Model-' + sample_name].rootAssembly.instances['Part-1-1'].edges.findAt(((
        -5.0, 10.0, 0.0), )), name='TopEdge')

    # LET'S CREATE HISTORY OUTPUT REQUESTS
    mdb.models['Model-' + sample_name].HistoryOutputRequest(createStepName='Step-1', frequency=1
        , name='H-Output-2', rebar=EXCLUDE, region=
        mdb.models['Model-' + sample_name].rootAssembly.sets['BottomEdge'], sectionPoints=DEFAULT, 
        variables=('RF2',))
     
    #LET'S CREATE JOBS 
    mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
        explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
        memory=90, memoryUnits=PERCENTAGE, model='Model-' + sample_name, modelPrint=OFF, 
        multiprocessingMode=DEFAULT, name='Job-' + sample_name, nodalOutputPrecision=SINGLE, 
        numCpus=1, queue=None, scratch='', type=ANALYSIS, userSubroutine='', 
        waitHours=0, waitMinutes=0)
    mdb.jobs['Job-' + sample_name].writeInput()
    mdb.jobs['Job-' + sample_name].submit(consistencyChecking=OFF)    
    mdb.jobs['Job-' + sample_name].waitForCompletion()

    # IMPORT GEOMETRY
    a = mdb.models['Model-' + sample_name].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    p = mdb.models['Model-' + sample_name].parts['Part-1']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    cmap=session.viewports['Viewport: 1'].colorMappings['Material']
    session.viewports['Viewport: 1'].setColor(colorMapping=cmap)
    session.printToFile(fileName=path + 'data/' + sample_name + '_geom', format=PNG, 
        canvasObjects=(session.viewports['Viewport: 1'], ))
    del a

    # IMPORT RESULT PLOT
    a = mdb.models['Model-' + sample_name].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    o3 = session.openOdb(name=path + 'Job-' + sample_name + '.odb')
    session.viewports['Viewport: 1'].setValues(displayedObject=o3)
    a = mdb.models['Model-' + sample_name].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.mdbData.summary()

    session.viewports['Viewport: 1'].setValues(
        displayedObject=session.odbs[path + 'Job-' + sample_name + '.odb'])
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(
        optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
    session.viewports['Viewport: 1'].odbDisplay.commonOptions.setValues(
        visibleEdges=FEATURE)
    session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
        CONTOURS_ON_UNDEF, ))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=62.0656, 
        farPlane=97.9344, width=40.91, height=23.8275, viewOffsetX=-2.12656, 
        viewOffsetY=-0.672793)
    # Stress
    session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
        variableLabel='S', outputPosition=INTEGRATION_POINT, refinement=(
        INVARIANT, 'Mises'), )
    session.printOptions.setValues(rendition=GREYSCALE)
    session.printToFile(fileName=path + 'data/' + sample_name + '_mises', format=PNG, 
        canvasObjects=(session.viewports['Viewport: 1'], ))

    odbname = 'Job-' + sample_name# set odb name here
    # set odb path here (if in working dir no need to change!)
    myodbpath = path + odbname + '.odb'    
    odb = openOdb(myodbpath)

    all_points = odb.steps['Step-1'].frames[-1].fieldOutputs['S'].values

    # Stress
    mises_list = []
    for i in range (1, len(all_points)):
        mises_stress = all_points[i].mises
        mises_list.append(mises_stress)

    #stress
    max_mises = max(mises_list)
    min_mises = min(mises_list)

    np.savetxt(path + 'data/' + odbname + '.txt', np.array([min_mises, max_mises]))

