"""
This example program demonstrates how one can add a callback function to a telemetry message, as
well as how to adjust the frequency of that telemetry message, and how to remove the callback.
"""
import time
import blueye.protocol as bp
from blueye.sdk import Drone


def callback_depth(msg_type: str, msg: bp.Imu2Tel):
    """Callback for the depth telemetry message

    This function is called once for every PositionEstimate message received by the telemetry watcher
    """
    print(f"Got a {msg_type} message with IMU data: {msg.imu}")


if __name__ == "__main__":
    # Instantiate a drone object
    my_drone = Drone()

    # Add a callback for the PositionEstimate message, storing the ID for later use
    callback_id = my_drone.telemetry.add_msg_callback([bp.Imu1Tel], callback_depth)

    # Adjust the publishing frequency to 5 Hz
    my_drone.telemetry.set_msg_publish_frequency(bp.Imu1Tel, 2)

    # Callback is triggered by a separate thread while we sleep here
    time.sleep(5)

    # Remove the callback using the ID we stored when it was created (not really necessary here
    # since the my_drone object goes out of scope immediately afterwards)
    my_drone.telemetry.remove_msg_callback(callback_id)