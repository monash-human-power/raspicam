""" Test Script That Sends A Message To the Camera Overlay """
import argparse
import paho.mqtt.client as mqtt
import time

def get_args(argv=None):
    """Get arguments passed into Python script"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="localhost", help="ip address of the host")
    parser.add_argument("--waitTime", type=int, default=8, help="Number of seconds until next message is sent")
    return parser.parse_args(argv)