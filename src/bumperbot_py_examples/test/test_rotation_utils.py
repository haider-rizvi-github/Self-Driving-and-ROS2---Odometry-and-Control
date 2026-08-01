import math

from bumperbot_py_examples.rotation_utils import compute_rotation_matrix


def test_identity_rotation_matrix_for_zero_radians():
    matrix = compute_rotation_matrix(0.0)

    assert matrix == (1.0, 0.0, 0.0, 1.0)


def test_90_degree_rotation_matrix():
    matrix = compute_rotation_matrix(math.pi / 2)

    assert math.isclose(matrix[0], 0.0, abs_tol=1e-9)
    assert math.isclose(matrix[1], -1.0, abs_tol=1e-9)
    assert math.isclose(matrix[2], 1.0, abs_tol=1e-9)
    assert math.isclose(matrix[3], 0.0, abs_tol=1e-9)
