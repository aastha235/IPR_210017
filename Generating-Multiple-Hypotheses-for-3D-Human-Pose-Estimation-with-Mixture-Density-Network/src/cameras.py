import json
import numpy as np

def project_point_radial(P, R, T, f, c, k, p):
    """
    Project points from 3d to 2d using camera parameters
    including radial and tangential distortion

    Args
      P: Nx3 points in world coordinates
      R: 3x3 Camera rotation matrix
      T: 3x1 Camera translation parameters
      f: (scalar) Camera focal length
      c: 2x1 Camera center
      k: 3x1 Camera radial distortion coefficients
      p: 2x1 Camera tangential distortion coefficients
    Returns
      Proj: Nx2 points in pixel space
      D: 1xN depth of each point in camera space
      radial: 1xN radial distortion per point
      tan: 1xN tangential distortion per point
      r2: 1xN squared radius of the projected points before distortion
    """

    assert len(P.shape) == 2
    assert P.shape[1] == 3

    N = P.shape[0]
    X = R.dot(P.T - T)  # rotate and translate
    XX = X[:2, :] / X[2, :]
    r2 = XX[0, :]**2 + XX[1, :]**2

    radial = 1 + np.einsum('ij,ij->j', np.tile(k, (1, N)), np.array([r2, r2**2, r2**3]))
    tan = p[0]*XX[1, :] + p[1]*XX[0, :]

    XXX = XX * np.tile(radial + tan, (2, 1)) + np.outer(np.array([p[1], p[0]]).reshape(-1), r2)

    Proj = (f * XXX) + c
    Proj = Proj.T

    D = X[2, :]

    return Proj, D, radial, tan, r2


def world_to_camera_frame(P, R, T):
    """
    Convert points from world to camera coordinates

    Args
      P: Nx3 3d points in world coordinates
      R: 3x3 Camera rotation matrix
      T: 3x1 Camera translation parameters
    Returns
      X_cam: Nx3 3d points in camera coordinates
    """

    assert len(P.shape) == 2
    assert P.shape[1] == 3

    X_cam = R.dot(P.T - T)  # rotate and translate

    return X_cam.T


def camera_to_world_frame(P, R, T):
    """Inverse of world_to_camera_frame

    Args
      P: Nx3 points in camera coordinates
      R: 3x3 Camera rotation matrix
      T: 3x1 Camera translation parameters
    Returns
      X_cam: Nx3 points in world coordinates
    """

    assert len(P.shape) == 2
    assert P.shape[1] == 3

    X_cam = R.T.dot(P.T) + T  # rotate and translate

    return X_cam.T


def load_camera_params(camera_data):
    """Load camera parameters from JSON data
    
    Args
      camera_data: dictionary containing the camera parameters for a specific camera
    Returns
      R: 3x3 Camera rotation matrix
      T: 3x1 Camera translation parameters
      f: (scalar) Camera focal length
      c: 2x1 Camera center
      k: 3x1 Camera radial distortion coefficients (set to zeros as not in JSON)
      p: 2x1 Camera tangential distortion coefficients (set to zeros as not in JSON)
    """

    R = np.array(camera_data['R'])
    T = np.array(camera_data['t']).reshape(3, 1)
    f = np.array(camera_data['f']).reshape(2, 1)
    c = np.array(camera_data['c']).reshape(2, 1)

    # Set radial and tangential distortion to zeros since they're not in the JSON
    k = np.zeros((3, 1))
    p = np.zeros((2, 1))

    name = 'Camera parameters from JSON'

    return R, T, f, c, k, p, name


def load_cameras(subjects=[1, 5, 6, 7, 8, 9, 11]):
    """Loads the cameras from multiple JSON files

    Args
      subjects: List of ints representing the subject IDs for which cameras are requested
    Returns
      rcams: dictionary of 4 tuples per subject ID containing its camera parameters for the 4 cameras
    """

    rcams = {}
    for s in subjects:
        json_path = f'Human36M_subject{s}_camera.json'
        with open(json_path, 'r') as f:
            camera_data = json.load(f)

        for c in range(4):  # There are 4 cameras in Human3.6M
            cam_key = str(c+1)
            rcams[(s, c+1)] = load_camera_params(camera_data[cam_key])

    return rcams
