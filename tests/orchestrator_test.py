""" Test Script For Orchestrator Class """
import orchestrator


class TestOrchestrator:
    """ Orchestrator test class """

    @staticmethod
    def test_class_instantiation():
        """ Test out class instantiation """
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
    """ get_args test class """

    @staticmethod
    def test_valid_arguments():
        """ get_args valid arguments
        Test the arguments parser for the file
        """
        test_input = vars(orchestrator.get_args())
        expected_result = {"host": "192.168.100.100"}
        assert (
            test_input == expected_result
        ), "failed - default ip in function get_args is incorrect"

        test_input = ["--host", "localhost"]
        expected_result = {"host": "localhost"}
        assert (
            vars(orchestrator.get_args(test_input)) == expected_result
        ), "failed - ip of local host is incorrect"

        test_input = ["--host", "192.168.100.100"]
        expected_result = {"host": "192.168.100.100"}
        assert (
            vars(orchestrator.get_args(test_input)) == expected_result
        ), "failed - Broker ip not same as default"
