import time
import csv
import blueye.protocol as bp
from blueye.sdk import Drone
from google.protobuf.json_format import MessageToDict

# Global variabel for å lagre CSV skriveren
csv_writer = None
csv_file = None

def setup_csv(fields):
    """Set up the CSV file and writer"""
    global csv_writer, csv_file
    csv_file = open('telemetry_data.csv', mode='w', newline='')
    csv_writer = csv.DictWriter(csv_file, fieldnames=fields)
    csv_writer.writeheader()

def common_callback(msg_type: str, msg):
    """Common callback for handling telemetry messages"""
    global csv_writer
    
    # Konverter protobuf-meldingen til en dictionary
    msg_dict = MessageToDict(msg, preserving_proto_field_name=True)

    # Legg til tidsstempel og meldingstype
    msg_dict['timestamp'] = time.time()
    msg_dict['message_type'] = msg_type

    # Skriv data til CSV-fil
    csv_writer.writerow(msg_dict)
    print(f"Logged data: {msg_dict}")

if __name__ == "__main__":
    # Sett opp de tilgjengelige feltene fra protokollen for CSV-filen
    initial_fields = ['timestamp', 'message_type']
    setup_csv(initial_fields)

    # Instantiate a drone object
    my_drone = Drone()

    # Liste over alle meldingstyper vi vil abonnere på
    message_types = [
        bp.DepthTel,
        bp.Imu1Tel,
        bp.Imu2Tel,
        bp.BatteryTel,
        bp.AttitudeTel,
        # Legg til andre relevante meldingstyper her
    ]

    # Legg til callbacks for alle meldingstyper
    callback_ids = []
    for msg_type in message_types:
        callback_id = my_drone.telemetry.add_msg_callback([msg_type], common_callback)
        callback_ids.append(callback_id)

    # Juster publiseringsfrekvens for meldinger (kan tilpasses)
    for msg_type in message_types:
        my_drone.telemetry.set_msg_publish_frequency(msg_type, 2)

    try:
        # Callback er utløst av en separat tråd mens vi sover her
        time.sleep(10)
    finally:
        # Fjern callbacker ved hjelp av IDene vi lagret da de ble opprettet
        for callback_id in callback_ids:
            my_drone.telemetry.remove_msg_callback(callback_id)

        # Lukk CSV-filen
        csv_file.close()