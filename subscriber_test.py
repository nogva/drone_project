import time
import csv
import blueye.protocol as bp
from blueye.sdk import Drone

# Global variabel for å lagre data
telemetry_data = {
    'timestamp': None,
    'imu1_data': None,
    'imu2_data': None,
    'depth_data': None,
    'start_lat': None,
    'start_long': None,
}

def setup_csv():
    """Set up the CSV file and writer"""
    csv_file = open('telemetry_data.csv', mode='w', newline='')
    csv_writer = csv.writer(csv_file)
    # Write the header row
    csv_writer.writerow(['Timestamp', 'IMU1Data', 'IMU2Data', 'Depth', 'StartLat', 'StartLong'])
    return csv_file, csv_writer

def common_callback(msg_type: str, msg):
    """Common callback for handling telemetry messages"""
    global telemetry_data, csv_writer
    
    print(f"Received message of type: {msg_type}")
    
    telemetry_data['timestamp'] = time.time()
    
    if isinstance(msg, bp.Imu1Tel):
        telemetry_data['imu1_data'] = msg.imu
        print(f"IMU1 data: {telemetry_data['imu1_data']}")
    elif isinstance(msg, bp.Imu2Tel):
        telemetry_data['imu2_data'] = msg.imu
        print(f"IMU2 data: {telemetry_data['imu2_data']}")
    elif isinstance(msg, bp.DepthTel):
        telemetry_data['depth_data'] = msg.depth.value
        print(f"Depth data: {telemetry_data['depth_data']}")
    elif isinstance(msg, bp.PilotGPSPositionTel):
        telemetry_data['start_lat'] = msg.position.latitude
        telemetry_data['start_long'] = msg.position.longitude
        print(f"Pilot GPS Position: Lat {telemetry_data['start_lat']}, Long {telemetry_data['start_long']}")

    # Write to CSV if we have all necessary data
    if all(value is not None for value in telemetry_data.values()):
        csv_writer.writerow([
            telemetry_data['timestamp'],
            telemetry_data['imu1_data'],
            telemetry_data['imu2_data'],
            telemetry_data['depth_data'],
            telemetry_data['start_lat'],
            telemetry_data['start_long']
        ])
        print(f"Logged data: {telemetry_data}")
        # Reset data to avoid duplicate writes
        telemetry_data = {key: None for key in telemetry_data}

def live_mapping():
    

if __name__ == "__main__":
    # Set up the CSV file
    csv_file, csv_writer = setup_csv()
    print("CSV file set up")

    # Instantiate a drone object
    my_drone = Drone()
    print("Drone instantiated")

    # Add callbacks for the DepthTel, IMU1Tel, IMU2Tel, and PilotGPSPositionTel messages, using the common callback
    callback_id_depth = my_drone.telemetry.add_msg_callback([bp.DepthTel], common_callback)
    callback_id_imu1 = my_drone.telemetry.add_msg_callback([bp.Imu1Tel], common_callback)
    callback_id_imu2 = my_drone.telemetry.add_msg_callback([bp.Imu2Tel], common_callback)
    callback_id_gps = my_drone.telemetry.add_msg_callback([bp.PilotGPSPositionTel], common_callback)
    print("Callbacks added")

    # Adjust the publishing frequency for the messages
    my_drone.telemetry.set_msg_publish_frequency(bp.DepthTel, 10)
    my_drone.telemetry.set_msg_publish_frequency(bp.Imu1Tel, 10)
    my_drone.telemetry.set_msg_publish_frequency(bp.Imu2Tel, 10)
    my_drone.telemetry.set_msg_publish_frequency(bp.PilotGPSPositionTel, 10)
    print("Publishing frequency set")

    # Callback is triggered by a separate thread while we sleep here
    print("Starting to receive telemetry data...")
    time.sleep(20)
    print("Finished receiving telemetry data")

    # Remove the callbacks using the IDs we stored when they were created
    my_drone.telemetry.remove_msg_callback(callback_id_depth)
    my_drone.telemetry.remove_msg_callback(callback_id_imu1)
    my_drone.telemetry.remove_msg_callback(callback_id_imu2)
    my_drone.telemetry.remove_msg_callback(callback_id_gps)
    print("Callbacks removed")

    # Close the CSV file
    csv_file.close()
    print("CSV file closed")
