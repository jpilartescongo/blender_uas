# Generating Camera Pose Data for Simulation

import numpy as np
import csv
import math
import random
# ======================================================================================================================
Pe = 80             # requested endlap (%)
Ps = 70            # requested sidelap (%)

sensorDimX = 36.0# 13.2    # Sensor dimension across flight line (mm)
sensorDimY = 24.0# 8.8     # Sensor dimension along flight line (mm)
focalLength = 35.0# 8.8     # Camera focal length (mm)    
FlightHeight = 70    # Flight altitude (m)

B = math.floor((100-Pe)/100*FlightHeight/focalLength*sensorDimY)    #  Distance between successive exposure station (m)
L = math.floor((100-Ps)/100*FlightHeight/focalLength*sensorDimX)    #  Distance between adjacent flight strips (m)
print('Endlab = ', B)
print('Sidelap = ', L)
# Simulated Camera Poses
# X = np.arange(-25, 26, L)
# Y = np.arange(0, 121, B)

# Study area for overlapping imagery
# X = np.arange(-30, 25, L)
# Y = np.arange(0, 160, B)

# Study area for oblique imagery
X = np.arange(-210, 510, L)
Y = np.arange(-150, 600, B)

z = FlightHeight

omega = 0 # degrees
phi = 0 # degrees

camPose = np.zeros((X.shape[0]*Y.shape[0], 6))
camPoseMetashape = np.zeros((X.shape[0]*Y.shape[0], 6))
# =============================================================================

save_path_camPose_Blender = 'F:/Blender Generated Datasets/Set 3/Camera_Pose_Blender.csv'
save_path_camPose_Metashape = 'F:/Blender Generated Datasets/Set 3/CameraPose_Metashape.csv'

# =============================================================================
#                 Creating Flight Plan for Simulation in Blender
# =============================================================================
CamID = []
pose = 0
turn = 0


for x in X:
    for y in Y:
        # camPose = [X  Y   Z   Omega   Phi   Kappa]
        camPose[pose, :] = [x + random.random() * pow(-1, random.randrange(0,2)), 
                            y + random.random() * pow(-1, random.randrange(0,2)), 
                            z + random.random() * pow(-1, random.randrange(0,2)), 
                            omega + random.random() + random.randrange(-5,5) , 
                            phi + random.random() + random.randrange(-5,5), 
                            (1-pow(-1, turn))/2*180 + random.random() + random.randrange(-5,5)]
        camName = "{}_{}{}".format('Cam', f"{pose+1:04d}", '.jpg')
        CamID.append(camName)
        #CamID.append(f'Cam-{pose+1}'+'.jpg')
        
        camPoseMetashape[pose, :] = camPose[pose, :]
        camPoseMetashape[pose, 3] = pow(-1, turn) * camPose[pose, 3]
        camPoseMetashape[pose, 4] = pow(-1, turn) * camPose[pose, 4]
        
        pose += 1
    turn += 1
    Y = np.flip(Y, 0)

# =============================================================================
# Writing Camera Pose for Simulation in Blender and Importing in Metashape
# =============================================================================

f1 = open(save_path_camPose_Blender, 'w')

with f1:
    fieldNames = ['Camera ID', 'X', 'Y', 'Z', 'Omega', 'Phi', 'Kappa']
    writer = csv.DictWriter(f1, fieldnames=fieldNames, delimiter=',', lineterminator='\n')
    writer.writeheader()
    for pose in range(len(CamID)):
        writer.writerow({'Camera ID': CamID[pose], 'X': camPose[pose, 0], 'Y': camPose[pose, 1], 'Z': camPose[pose, 2],
                         'Omega': camPose[pose, 3], 'Phi': camPose[pose, 4], 'Kappa': camPose[pose, 5]})

f2 = open(save_path_camPose_Metashape, 'w')                         
with f2:
    fieldNames = ['Camera ID', 'X', 'Y', 'Z', 'Omega', 'Phi', 'Kappa']
    writer = csv.DictWriter(f2, fieldnames=fieldNames, delimiter=',', lineterminator='\n')
    writer.writeheader()
    for pose in range(len(CamID)):
        writer.writerow({'Camera ID': CamID[pose], 'X': camPoseMetashape[pose, 0], 'Y': camPoseMetashape[pose, 1], 'Z': camPoseMetashape[pose, 2],
                         'Omega': camPoseMetashape[pose, 3], 'Phi': camPoseMetashape[pose, 4], 'Kappa': camPoseMetashape[pose, 5]})

#==============================================================================
# add uncertainty to XYZ locations of the cameras
#==============================================================================
# mu = 0
# sigma = 0.05

# for i in range(1,21,1):
#     camPose = np.random.normal(mu, sigma, size=(X.shape[0]*Y.shape[0], 6)).round(3)
#     camPose[:,3:] = 0
#     camPose = camPose_No + camPose
    
#     # Writing Camera Poses into a CSV File.
#     filename = 'CameraPose' + '_' + str(i) + '.csv'
#     f = open(filename, 'w')
#     with f:
#         fieldNames = ['Camera ID', 'X', 'Y', 'Z', 'Omega', 'Phi', 'Kappa']
#         writer = csv.DictWriter(f, fieldnames=fieldNames, delimiter=',', lineterminator='\n')
#         writer.writeheader()
#         for pose in range(len(CamID)):
#             writer.writerow({'Camera ID': CamID[pose], 'X': camPose[pose, 0], 'Y': camPose[pose, 1], 'Z': camPose[pose, 2],
#                              'Omega': camPose[pose, 3], 'Phi': camPose[pose, 4], 'Kappa': camPose[pose, 5]})
# ======================================================================================================================










        

