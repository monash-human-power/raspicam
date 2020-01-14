"""Test Script For Orchestrator Class"""
import orchestrator

class TestOrchestrator:
    """Orchestrator test class"""
    @staticmethod
    def test_class_instantiation():
        """Test out class instantiation"""
        test_broker_ip = 'localhost'
        test_port = 1883
        test_orchestrator = orchestrator.Orchestrator(test_broker_ip, test_port)
        
        #Ensure broker ip and port are assigned
        assert test_orchestrator.broker_ip == test_broker_ip, "failed - broker ip not assigned"
        assert test_orchestrator.port == test_port, "failed - port not assigned"

        #Ensure MQTT client has not started
        assert test_orchestrator.mqtt_client is None, "failed - MQTT client has started"


class TestGetArgs:
    """get_args test class"""
    @staticmethod
    def test_valid_arguments():
        """get_args valid arguments
        Test the arguments parser for the file 
        """
        test_input = ['--host', 'localhost']
        expected_result = {
            "host": "localhost"
        }
        assert vars(orchestrator.get_args(test_input)) == expected_result, "failed"

        test_input = ['--host', '192.168.100.100']
        expected_result = {
            "host": "192.168.100.100"
        }
        assert vars(orchestrator.get_args(test_input)) == expected_result, "failed - Broker ip not same as default"
