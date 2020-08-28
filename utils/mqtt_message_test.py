""" Test Script That Sends A Message To the Camera Overlay """
import argparse
import paho.mqtt.client as mqtt
import time

from mhp.topics import DAShboard


def get_args(argv=None):
    """Get arguments passed into Python script"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--host", type=str, default="localhost", help="ip address of the host"
    )
    parser.add_argument(
        "--wait-time",
        type=int,
        default=8,
        help="Number of seconds until next message is sent",
    )
    return parser.parse_args(argv)


class MessageTest:
    def __init__(self, host_ip, wait_time):
        self.host_ip = host_ip
        self.wait_time = wait_time
        self.mqtt_client = None
        self.message_topic = DAShboard.overlay_message

    def on_log(self, client, userdata, level, buf):
        """ The callback to log all MQTT information """
        print("log: " + buf)

    def on_connect(self, client, userdata, flags, rc):
        """Callback for when the client receives a CONNACK response."""
        if rc == 0:
            print("Connected OK")
        else:
            print("Bad connection Returned code=", rc)

    def on_disconnect(self, client, userdata, flags, rc=0):
        """Callback that is called when user is disconnected from broker."""
        print("Disconnected result code " + str(rc))

    def start(self):
        """ start Message Test """
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_log = self.on_log
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.mqtt_client.connect_async(self.host_ip)

        self.mqtt_client.loop_start()
        while True:
            self.mqtt_client.publish(self.message_topic, "Test Message")

            # Send a second message to ensure most recent message is displayed
            time.sleep(2)
            self.mqtt_client.publish(self.message_topic, "Second Test Message")
            time.sleep(self.wait_time)


if __name__ == "__main__":
    # Get command line arguments
    ARGS = get_args()
    HOST_IP = ARGS.host
    WAIT_TIME = ARGS.wait_time
    messagetest = MessageTest(HOST_IP, WAIT_TIME)

    # Start
    messagetest.start()
