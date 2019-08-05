"""
Application Note: Calculating Angles Between Two YOST LABS 3-Space Sensor Devices using Two Vectors
on a Human Body
Description: Calculates the hinge angle between two YOST LABS 3-Space Sensor devices in Python3
"""
import api.threespace_api as tss
import time
import math

def main():
    display_devices()

    dongles = tss.getComPorts(tss.TSS_FIND_DNG)
    
    # make sure there is only one dongle
    if len(dongles) is not 1:
        print("Please use exactly one Dongle with this application")
        return
    
    # connect the dongle and make sure there is exaclty two wireless sensors
    true_dongle = tss.TSDongle(dongles[0].com_port)
    count_wireless_sensor = 0
    for sensor in true_dongle:
        if sensor:
            count_wireless_sensor += 1
    if count_wireless_sensor != 2:
        print("please use exaclty two wireless sensors with the dongle")
        return
    del count_wireless_sensor

    # get the two devices
    sensor0 = true_dongle[0]
    sensor1 = true_dongle[1]

    print("Get into the starting position.")
    time.sleep(3)
    print("Please hold for 10 seconds to compensate for device positioning.")
    time.sleep(5)


    ## Calculate the rotational offset of the compensation for the the first device
    offset0 = sensor0.getUntaredTwoVectorInSensorFrame()
    ## Calculate the rotational offset of the compensation for the the second device
    offset1 = sensor1.getUntaredTwoVectorInSensorFrame()
    
    time.sleep(2)
    while True:
        ## Calculate the forward vector of the first device
        ## The initial forward vector to use depends on the orientation and axis direction of the device
        ## The resultant vector must be heading up the arm
        forward0 = calculateDeviceVector(sensor0, [0.0, 0.0, 1.0], offset0)
        ## Calculate the forward vector of the second device
        ## The initial forward vector to use depends on the orientation and axis direction of the device
        ## The resultant vector must be heading up the arm
        forward1 = calculateDeviceVector(sensor1, [0.0, 0.0, 1.0], offset1)

        ## Calculate a vector perpendicular to the forward vectors and parallel to the axis
        ## of rotation to use for determining the sign of the angle
        ## Using the first device's orientation will give the best results
        ## The initial vector to use depends on the initial forward vector
        up0 = calculateDeviceVector(sensor0, [0.0, 1.0, 0.0], offset0)

        ## Calculate the angle between the two devices
        angle = calculateAngle(forward1, forward0, up0)
        
        ## Print as radians and degrees
        print("Hinge")
        print("Radians: %0.4f" % angle)
        print("Degrees: %0.4f" % math.degrees(angle))
        print("============================================")


def display_devices():
    devices = tss.getComPorts()
    print("%d device(s) found" % len(devices))
    if not len(devices): return

    for i, device in enumerate(devices):
            print("device #{}:".format(i + 1))
            print("type: {}".format(device.dev_type))
            print("port: {}".format(device.com_port))

def calculateDeviceVector(sensor, vec, offset):
    """ Calculates a vector in a 3-Space Sensor device's reference frame.

    Args:
    serial_port: A Serial object that is communicating with a 3-Space Sensor device.
    vec: A unit vector.
    offset: A unit quaternion that denotes the offset of the 3-Space Sensor device.
    """
    ## Get the filtered tared orientation of the device
    data = sensor.getTaredOrientationAsQuaternion()

    ## Apply the offset for the device
    quat = quaternionMultiplication(data, offset)

    ## Calculate a vector for the device with its orientation
    vector = quaternionVectorMultiplication(quat, vec)

    return vector

def quaternionMultiplication(quat0, quat1):
    """ Performs quaternion multiplication on the two given quaternions.

    Args:
    quat0: A unit quaternion.
    quat1: A unit quaternion.
    """
    x0, y0, z0, w0 = quat0
    x1, y1, z1, w1 = quat1

    x_cross, y_cross, z_cross = vectorCross([x0, y0, z0], [x1, y1, z1])
    w_new = w0 * w1 - vectorDot([x0, y0, z0], [x1, y1, z1])
    x_new = x1 * w0 + x0 * w1 + x_cross
    y_new = y1 * w0 + y0 * w1 + y_cross
    z_new = z1 * w0 + z0 * w1 + z_cross

    return [x_new, y_new, z_new, w_new]

def quaternionVectorMultiplication(quat, vec):
    """ Rotates the given vector by the given quaternion.

    Args:
    quat: A unit quaternion.
    vec: A unit vector.
    """
    ## Procedure: quat * vec_quat * -quat
    qx, qy, qz, qw = quat
    vx, vy, vz = vec
    vw = 0.0
    neg_qx = -qx
    neg_qy = -qy
    neg_qz = -qz
    neg_qw = qw

    ## First Multiply
    x_cross, y_cross, z_cross = vectorCross([qx, qy, qz], vec)
    w_new = qw * vw - vectorDot([qx, qy, qz], vec)
    x_new = vx * qw + qx * vw + x_cross
    y_new = vy * qw + qy * vw + y_cross
    z_new = vz * qw + qz * vw + z_cross

    ## Second Multiply
    x_cross, y_cross, z_cross = vectorCross([x_new, y_new, z_new], [neg_qx, neg_qy, neg_qz])
    w = w_new * neg_qw - vectorDot([x_new, y_new, z_new], [neg_qx, neg_qy, neg_qz])
    x = neg_qx * w_new + x_new * neg_qw + x_cross
    y = neg_qy * w_new + y_new * neg_qw + y_cross
    z = neg_qz * w_new + z_new * neg_qw + z_cross

    return [x, y, z]

def calculateAngle(vec0, vec1, vec2=None):
    """ Calculates the angle between the two given vectors using the dot product.

    Args:
    vec0: A unit vector.
    vec1: A unit vector.
    vec2: A unit vector perpendicular to vec0 and vec1.
    """
    ## The max and min is used to account for possible floating point error
    dot_product = max(min(vectorDot(vec0, vec1), 1.0), -1.0)
    angle = math.acos(dot_product)

    if vec2 is not None:
        axis = vectorNormalize(vectorCross(vec0, vec1))
        angle = math.copysign(angle, vectorDot(vec2, axis))

    return angle

def vectorDot(vec0, vec1):
    """ Performs the dot product on the two given vectors.

    Args:
    vec0: A unit vector.
    vec1: A unit vector.
    """
    x0, y0, z0 = vec0
    x1, y1, z1 = vec1

    return x0 * x1 + y0 * y1 + z0 * z1

def vectorCross(vec0, vec1):
    """ Performs the cross product on the two given vectors.

    Args:
    vec0: A unit vector.
    vec1: A unit vector.
    """
    x0, y0, z0 = vec0
    x1, y1, z1 = vec1

    return [y0 * z1 - z0 * y1, z0 * x1 - x0 * z1, x0 * y1 - y0 * x1]

def vectorNormalize(vec):
    """ Normalizes the vector given.

    Args:
    vec: A vector.
    """
    length = vectorLength(vec)
    x, y, z = vec

    return [x / length, y / length, z / length]

if __name__ == "__main__": main()