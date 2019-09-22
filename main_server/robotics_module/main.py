import numpy as np
import matplotlib.pyplot as plt

class Robot:

    def __init__(self, length, initial_pos):
        self.length = length
        self.position = initial_pos


    def inverse_kinematic(self, goal_loc, max_iter=1000):
        assert len(goal_loc) == 3
        xd, yd, zd = goal_loc
        L1, L2, L3, L4 = self.length
        theta_1, theta_2, theta_3, theta_4 = self.position

        # For convenience, define sin and cos function which take the inputs in degree.
        sind = lambda x: np.sin(x * np.pi / 180)
        cosd = lambda x: np.cos(x * np.pi / 180)

        # Loop starts
        epoch = 0
        max_err = 9999
        success = False
        while epoch < max_iter and not success:

            T1 = [[-sind(theta_1), 0, cosd(theta_1), 0],
                  [cosd(theta_1), 0, sind(theta_1), 0],
                  [0, 1, 0, L1],
                  [0, 0, 0, 1]]
            T2 = [[cosd(theta_2), -sind(theta_2), 0, L2*cosd(theta_2)],
                  [sind(theta_2), cosd(theta_2), 0, L2*sind(theta_2)],
                  [0, 0, 1, 0],
                  [0, 0, 0, 1]]
            T3 = [[cosd(theta_3), 0, -sind(theta_3), L3*cosd(theta_3)],
                  [sind(theta_3), 0, cosd(theta_3), L3*sind(theta_3)],
                  [0, -1, 0, 0],
                  [0, 0, 0, 1]]
            T4 = [[sind(theta_4), cosd(theta_4), 0, L4*cosd(theta_4)],
                  [-cosd(theta_4), sind(theta_4), 0, L4*sind(theta_4)],
                  [0, 0, 1, 0],
                  [0, 0, 0, 1]]

            T1, T2, T3, T4 = map(np.array, [T1, T2, T3, T4])

            T12 = T1 @ T2;
            T123 = T1 @ T2 @ T3;
            T1234 = T1 @ T2 @ T3 @ T4;

            w = np.stack([
                [0, 0, 1],
                T1[:3, 2],
                T12[:3, 2],
                T123[:3, 2]
            ]).T

            q1 = T123[:3, 3] - 0
            q2 = T123[:3, 3] - T1[:3, 3]
            q3 = T123[:3, 3] - T12[:3, 3]
            q4 = T123[:3, 3] - T123[:3, 3]

            v1 = np.cross(w[:3, 0], q1)
            v2 = np.cross(w[:3, 1], q2)
            v3 = np.cross(w[:3, 2], q3)
            v4 = np.cross(w[:3, 3], q4)

            J = np.vstack([np.stack([v1, v2, v3, v4]).T, w])

            xr, yr, zr, _ = T1234[:,3]

            # Inverse Kinematics _ Damped Least Square method

            x_dot = [xd-xr,yd-yr,zd-zr,1,0,0]
            lmbd = 1 #lambda
            cof = J @ J.T + lmbd**2 * np.eye(6)
            theta_dot = J.T @ np.linalg.inv(cof) @ x_dot

            theta_1 = theta_1 + theta_dot[0];
            theta_2 = theta_2 + theta_dot[1];
            theta_3 = theta_3 + theta_dot[2];
            theta_4 = theta_4 + theta_dot[3];

            max_err = np.abs(x_dot[:3]).max()

            if max_err < 1:
                success = True

            epoch+=1

        return {
            'theta': [theta_1, theta_2, theta_3, theta_4],
            'num_iter': epoch,
            'success': success,
            'err': max_err
        }
