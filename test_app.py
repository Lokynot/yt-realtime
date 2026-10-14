import unittest
from app import AppHandler
from http.server import HTTPServer
from threading import Thread
from urllib.request import urlopen


class TestApplication(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), AppHandler)
        cls.port = cls.server.server_address[1]

        cls.thread = Thread(
            target=cls.server.serve_forever,
            daemon=True
        )
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def test_home_page(self):
        with urlopen(f"http://127.0.0.1:{self.port}/") as response:
            self.assertEqual(response.status, 200)
            self.assertIn(
                b"Real-Time CI/CD Pipeline",
                response.read()
            )

    def test_health_endpoint(self):
        with urlopen(
            f"http://127.0.0.1:{self.port}/health"
        ) as response:
            self.assertEqual(response.status, 200)
            self.assertIn(b"healthy", response.read())


if __name__ == "__main__":
    unittest.main()
