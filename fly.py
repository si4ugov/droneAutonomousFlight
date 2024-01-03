import rospy
import math
import random
from clover import srv
from std_srvs.srv import Trigger

rospy.init_node('flight')

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_altitude = rospy.ServiceProxy('set_altitude', srv.SetAltitude)
set_yaw = rospy.ServiceProxy('set_yaw', srv.SetYaw)
set_yaw_rate = rospy.ServiceProxy('set_yaw_rate', srv.SetYawRate)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)

def goto(x=0, y=0, z=1.5, yaw=float('nan'), speed=1.5, frame_id='aruco_map', auto_arm=True, tolerance=0.2):
    navigate(x=x, y=y, z=z, yaw=yaw, speed=speed, frame_id=frame_id, auto_arm=auto_arm)

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            break
        rospy.sleep(0.2)

goto(frame_id='body')

coords = []
count = random.randint(3, 8)

for i in range(count):
    x = random.randint(0, 9)
    y = random.randint(0, 9)
    coords.append([x,y])

print(coords)

for coord in coords:
    coord_x = coord[0]
    coord_y = coord[1]
    
    print('Move to x: ', coord_x, 'Move to y: ', coord_y)

    goto(x = coord_x, y = coord_y)
    # func()

print('Flying to the base')
goto()
land()

