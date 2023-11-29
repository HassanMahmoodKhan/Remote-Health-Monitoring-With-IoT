import math

def ypr(accel_data, gyro_data):
    accel_sens = 16384.0
    gyro_sens = 131.0
    
    ax, ay, az = accel_data['x'], accel_data['y'], accel_data['z']
    gx, gy, gz = gyro_data['x'], gyro_data['y'], gyro_data['z']
    
    # calculating accelerometer angles
    accel_x_angle = math.degrees(math.atan2(ay, math.sqrt(math.pow(ax, 2) + math.pow(az, 2)))) #roll
    accel_y_angle = math.degrees(math.atan2(ax, math.sqrt(math.pow(ay, 2) + math.pow(az, 2)))) #pitch
    
    # calculating gyroscope angles - Not Needed
    gyro_x_angle = gx / gyro_sens
    gyro_y_angle = gy / gyro_sens
    gyro_z_angle = gz / gyro_sens
    
    accel_mag = math.sqrt(math.pow(ax, 2) + math.pow(ay, 2) + math.pow(az, 2))
    
    return gyro_x_angle, accel_x_angle, accel_y_angle, accel_mag
    
def is_fall_detected(a_magnitude, pitch, roll, acc_threshold=11.0, pitch_threshold=30.0, roll_threshold=30.0):
    return (a_magnitude >= 11 or a_magnitude < 10) and (abs(pitch) > pitch_threshold or abs(roll) > roll_threshold)

    
