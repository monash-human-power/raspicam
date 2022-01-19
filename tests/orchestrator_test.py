""" Test Script For Orchestrator Class """
from config import read_configs
import orchestrator


class TestOrchestrator:
    """Orchestrator test class"""

    @staticmethod
    def test_class_instantiation():
        """Test out class instantiation"""
        broker_ip = "localhost"
        port = 1883
        test_orchestrator = orchestrator.Orchestrator(broker_ip, port)

        # Ensure broker ip and port are assigned
        assert (
            test_orchestrator.broker_ip == broker_ip
        ), "failed - broker ip not assigned"
        assert test_orchestrator.port == port, "failed - port not assigned"

        # Ensure MQTT client has not started
        assert (
            test_orchestrator.mqtt_client is None
        ), "failed - MQTT client has started"


class TestGetArgs:
    """get_args test class"""

    @staticmethod
    def test_valid_arguments():
        """get_args valid arguments
        Test the arguments parser for the file
        """
        test_input = vars(orchestrator.get_args())
        expected_result = {
            "host": read_configs()["broker_ip"],
            "username": None,
        }
        assert (
            test_input == expected_result
        ), "failed - default ip in function get_args is incorrect"

        test_input = ["--host", "localhost"]
        expected_result = {"host": "localhost", "username": None}
        assert (
            vars(orchestrator.get_args(test_input)) == expected_result
        ), "failed - ip of local host is incorrect"

        test_input = ["--host", "192.168.100.100"]
        expected_result = {"host": "192.168.100.100", "username": None}
        assert (
            vars(orchestrator.get_args(test_input)) == expected_result
        ), "failed - Broker ip not same as default"

        test_input = ["--host", "192.168.100.100", "--username", "username"]
        expected_result = {"host": "192.168.100.100", "username": "username"}
        assert (
            vars(orchestrator.get_args(test_input)) == expected_result
        ), "failed - username not same as default"
