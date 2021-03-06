from math import sqrt

import tensorflow as tf

from .neighborhood_assembly import neighborhoods_weights_to_root,\
                                   neighborhoods_grid_spiral


class NeighborhoodAssemblyTest(tf.test.TestCase):

    def test_neighborhoods_by_weight(self):
        sequence = tf.constant([0, 2, 5, -1])

        adjacency = tf.constant([
            [0, 1, 4, 0, 0, 0, 0],
            [1, 0, 2, 0, 5, 0, 0],
            [4, 2, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 9, 2],
            [0, 5, 0, 0, 0, 3, 0],
            [0, 0, 0, 9, 3, 0, 0],
            [0, 0, 0, 2, 0, 0, 0],
        ])

        size = 3

        expected = [
            [0, 1, 2],
            [2, 3, 1],
            [5, 4, 1],
            [-1, -1, -1],
        ]

        with self.test_session() as sess:
            neighborhoods = neighborhoods_weights_to_root(
                adjacency, sequence, size)
            self.assertAllEqual(neighborhoods.eval(), expected)

        sequence = tf.constant([0, 1, 2, 3])

        adjacency = tf.constant([
            [0, 1, 3, 0],
            [1, 0, 0, 11],
            [3, 0, 0, 5],
            [0, 11, 5, 0],
        ])

        size = 5

        expected = [
            [0, 1, 2, 3, -1],
            [1, 0, 2, 3, -1],
            [2, 0, 1, 3, -1],
            [3, 2, 0, 1, -1],
        ]

        with self.test_session() as sess:
            neighborhoods = neighborhoods_weights_to_root(
                adjacency, sequence, size)
            self.assertAllEqual(neighborhoods.eval(), expected)

    def test_grid_spiral(self):
        sequence = tf.constant([5, 6])

        # 3x4 Grid
        adjacency = tf.constant([
            [0, 1, 0, 0, 1, sqrt(2), 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, sqrt(2), 1, sqrt(2), 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, sqrt(2), 1, sqrt(2), 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, sqrt(2), 1, 0, 0, 0, 0],
            [1, sqrt(2), 0, 0, 0, 1, 0, 0, 1, sqrt(2), 0, 0],
            [sqrt(2), 1, sqrt(2), 0, 1, 0, 1, 0, sqrt(2), 1, sqrt(2), 0],
            [0, sqrt(2), 1, sqrt(2), 0, 1, 0, 1, 0, sqrt(2), 1, sqrt(2)],
            [0, 0, sqrt(2), 1, 0, 0, 1, 0, 0, 0, sqrt(2), 1],
            [0, 0, 0, 0, 1, sqrt(2), 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, sqrt(2), 1, sqrt(2), 0, 1, 0, 1, 0],
            [0, 0, 0, 0, 0, sqrt(2), 1, sqrt(2), 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, sqrt(2), 1, 0, 0, 1, 0]
        ])

        size = 13

        expected = [
            [5, 1, 0, 4, 8, 9, 10, 6, 2, 3, 7, 11, -1],
            [6, 2, 1, 5, 9, 10, 11, 7, 3, -1, -1, -1, -1],
        ]

        with self.test_session() as sess:
            neighborhoods = neighborhoods_grid_spiral(
                adjacency, sequence, size)
            self.assertAllEqual(neighborhoods.eval(), expected)
