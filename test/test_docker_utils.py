import unittest
import docker_utils


class TestDockerUtils(unittest.TestCase):
    def test_possible_labels(self):
        possible_labels_expected = {
            'com.docker.swarm.execron.exec': 'exec',
            'com.docker.swarm.execron.webhook': 'webhook',
            'com.docker.swarm.execron.interval': 'interval',
            'com.docker.swarm.execron.number': 'number',
        }
        possible_labels = docker_utils.get_possible_labels()
        self.assertEqual(possible_labels, possible_labels_expected)

    def test_labels(self):
        possible_labels = docker_utils.get_possible_labels()

        # Test case without numbers in keys labels
        labels1 = {
            'com.docker.swarm.execron.exec': 'nginx -s reload',
            'com.docker.swarm.execron.webhook': 'http://receiver:7080',
            'com.docker.swarm.execron.interval': '123',
            'com.docker.swarm.execron.number': '4',
        }
        execs_expected1 = {
            'default': {
                'id': '123qwe',
                'exec': 'nginx -s reload',
                'webhook': 'http://receiver:7080',
                'interval': 123,
                'number': 4,
            }
        }
        execs = docker_utils.get_execs(labels1, possible_labels, '123qwe')
        self.assertEqual(execs, execs_expected1)

        # Test case numbers in keys labels
        labels2 = {
            'com.docker.swarm.execron.1.exec': 'nginx -s reload',
            'com.docker.swarm.execron.1.webhook': 'http://receiver:7080',
            'com.docker.swarm.execron.1.interval': '123',
            'com.docker.swarm.execron.1.number': '4',
        }
        execs_expected2 = {
            1: {
                'id': '123qwe',
                'exec': 'nginx -s reload',
                'webhook': 'http://receiver:7080',
                'interval': 123,
                'number': 4,
            }
        }
        execs = docker_utils.get_execs(labels2, possible_labels, '123qwe')
        self.assertEqual(execs, execs_expected2)

        # Test case numbers in keys and without numbers in labels keys
        labels3 = {**labels1, **labels2}
        execs_expected3 = {**execs_expected1, **execs_expected2}
        execs = docker_utils.get_execs(labels3, possible_labels, '123qwe')
        self.assertEqual(execs, execs_expected3)

        labels4 = {
            'com.docker.swarm.execron.somestring.exec': 'nginx -s reload',
            'com.docker.swarm.execron.somestring.webhook': 'http://receiver:7080',
            'com.docker.swarm.execron.somestring.interval': '123',
            'com.docker.swarm.execron.somestring.number': '4',
            'com.docker.swarm.execron.1somestring.exec': 'somestring',
            'com.docker.swarm.execron.somestring1.exec': '',
            'com.docker.swarm.execron.1somestring1.exec': '',
            'com.docker.swarm.execron.1some13string1.exec': '',
        }
        execs = docker_utils.get_execs(labels4, possible_labels, '123qwe')
        self.assertEqual(execs, {})

        labels5 = {**labels3, **labels4}
        execs = docker_utils.get_execs(labels5, possible_labels, '123qwe')
        self.assertEqual(execs, execs_expected3)

        labels6 = {**labels5, 'com.docker.swarm.execron.42.exec': 'somexec'}
        execs_expected6 = {**execs_expected3, 42: {'exec': 'somexec', 'id': '123qwe'}}
        execs = docker_utils.get_execs(labels6, possible_labels, '123qwe')
        self.assertEqual(execs, execs_expected6)


if __name__ == '__main__':
    unittest.main()
