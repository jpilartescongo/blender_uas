import os
import csv
import numpy as np
import bpy
import math
import mathutils
# ==================================================================================================

context = bpy.context
scene = context.scene
render = scene.render
layer = bpy.context.view_layer
render.image_settings.color_mode ='RGB'
pi = math.pi

# ==================================================================================================

data_path = 'F:/Blender Generated Datasets/Set 3/Camera_Pose_Blender.csv'

# ==================================================================================================
scene.render.resolution_x = 7952 # 5472
scene.render.resolution_y = 5304 # 3648
# ==================================================================================================


def camRemove():
    camcount = len(bpy.data.cameras)
    print(camcount)
    
    for obj in bpy.context.scene.objects:
        if obj.type == 'CAMERA':
            obj.select_set(True)
        else:
            obj.select_set(False)
    
    bpy.ops.object.delete()
    
    for block in bpy.data.cameras:
        if block.users == 0:
            bpy.data.cameras.remove(block)

            
def readCamPose():
    
    with open(data_path, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        headers = next(reader)
        camPose = np.array(list(reader))
        pose = (camPose[:, 1:7]).astype(float)
        camName = camPose[:,0]
        print(headers)
        #print(poses.shape)
        #print(poses[:3])
        #numPoses = poses.shape[0]
        return pose, camName

def camGeneration(camPose, name, sensorHeight, sensorWidth, focalLength):
    
    camNumber = 0
    for pose in camPose:
        camNumber += 1
        
        camName = "{}_{}".format('Cam', f"{camNumber:04d}")
        #camName = name[camNumber]
        cam = bpy.data.cameras.new(camName)
        cam.lens = focalLength
        cam.sensor_height = sensorHeight
        cam.sensor_width = sensorWidth
        
        cam_obj = bpy.data.objects.new(camName, cam)
        
        # scene.collection.objects.link(cam_obj)
        # bpy.data.collections['myCameras'].objects.link(cam_obj)
        bpy.data.collections['Collection'].objects.link(cam_obj)

        cam_obj.data.lens = focalLength # or bpy.data.cameras[camName].lens = 28
        cam_obj.data.sensor_height = sensorHeight  # or: bpy.data.cameras[camName].sensor_height = 8.80
        cam_obj.data.sensor_width = sensorWidth  # or: bpy.data.cameras[camName].sensor_width = 13.20
        
        
        setupCamera(cam_obj, pose)
        # cam_obj.location = (pose[0], pose[1], pose[2])
        # cam_obj.rotation_euler = (pose[3]*pi/180.0, pose[4]*pi/180, pose[5]*pi/180)
        # Update view layer
        layer.update()
    camcount = len(bpy.data.cameras)
    print('Number of Generated Cameras = ', camcount)


def setupCamera(cam_obj, pose):
    
    cam_obj.location = (pose[0], pose[1], pose[2])
    
    omega = math.radians(pose[3])  # CCW rotation around X axis of the sensor
    phi = math.radians(pose[4])  # CCW rotation around Y axis of the sensor
    kappa = math.radians(pose[5])  # CW rotation around Z axis from +Y (Real North)
    
    cam_obj.rotation_euler = (omega, phi, kappa)
    
    return cam_obj

def setupCamera1(scene, c):
    pi = math.pi

    scene.camera.rotation_euler[0] = c[0] * (pi / 180.0)
    scene.camera.rotation_euler[1] = c[1] * (pi / 180.0)
    scene.camera.rotation_euler[2] = c[2] * (pi / 180.0)

    scene.camera.location.x = c[3]
    scene.camera.location.y = c[4]
    scene.camera.location.z = c[5]
    return
# ======================================================================================================================

camcount = len(bpy.data.cameras)
print('Numer of Cameras in the Scene = ', camcount)

camRemove()

camcount = len(bpy.data.cameras)
print('Numer of Cameras in the Scene After Camera Removal = ', camcount)

camPose, camName = readCamPose()

sensorHeight = 24.0  # mm
sensorWidth = 36.0  # mm
focalLength = 35 # mm

camGeneration(camPose, camName, sensorHeight, sensorWidth, focalLength)

# ==================================================================================================
# Render Multiple Cameras at Once

# path_dir = bpy.context.scene.render.filepath  # save for restore
bpy.context.scene.render.filepath = 'F:/Blender Generated Datasets/Set 3/images'
bpy.context.scene.render.image_settings.file_format = 'JPEG'
path_dir = bpy.context.scene.render.filepath
print(path_dir)

for cam in [obj for obj in bpy.data.objects if obj.type == 'CAMERA']:
    bpy.context.scene.camera = cam
    bpy.context.scene.render.filepath = os.path.join(path_dir, cam.name)
    bpy.ops.render.render(write_still=True)

# ======================================================================================================================
