from client.entry import main
import json
from unittest.mock import mock_open, call, ANY

class TestClient:

    def test_run(self):
        main()

    def test_main(self, mocker):
        mocker.patch("os.path.dirname", return_value="")
        mocker.patch("os.path.join", side_effect=lambda *args: "/".join(args))
        
        mock_input_data = {"key": "value"}
        mock_response = {"statusCode": 200, "body": "success"}

        m_open = mock_open(read_data=json.dumps(mock_input_data))
        mocker.patch("builtins.open", m_open)
        
        mock_handler = mocker.patch("client.entry.handler", return_value=mock_response)
        
        main()
        
        m_open.assert_has_calls([
            call("/input.json", "r"),
            call("/output.json", "w")
        ], any_order=True)

        handle = m_open()
        handle.write.assert_any_call(ANY)

        mock_handler.assert_called_once_with({"body": mock_input_data}, {})
        