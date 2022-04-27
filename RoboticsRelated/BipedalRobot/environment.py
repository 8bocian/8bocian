#  Copyright (c) 2022. Oskar "Bocian" Możdżeń
#  All rights reserved.

import numpy as np
from gym import Env
from gym.spaces import Box
import pybullet as p
import pybullet_data as pd


class WalkerEnv(Env):
    def __init__(self, render=False, max_reward=2000, ttl=1000):
        self.position = None
        self.max_reward = max_reward
        # time to live for our agent
        self.ttl = ttl

        if not render:
            method = p.GUI
        else:
            method = p.DIRECT

        # connect to the physics server, set our parameters and load models
        client_id = p.connect(method)
        p.setAdditionalSearchPath(pd.getDataPath())
        p.setGravity(0, 0, -9.8)

        # time needs a small adjustment
        p.setTimeStep(0.0001)
        plane_id = p.loadURDF('plane.urdf')
        self.start_position = [0, 0, -0.4]
        self.start_rotation = [0, 0, 0, 1]
        self.joints_angles = np.array([0 for _ in range(4)], dtype=np.float32)
        self.object_id = p.loadURDF('robot.urdf', self.start_position, self.start_rotation)

        self.n_joints = p.getNumJoints(self.object_id)

        joint_constraints = [[p.getJointInfo(self.object_id, idx)[8] for idx in range(self.n_joints)],
                             [p.getJointInfo(self.object_id, idx)[9] for idx in range(self.n_joints)]]

        # this section will be refactored and corrected
        ###############################################

        # rotation values for each joint
        self.action_space = Box(low=np.array(joint_constraints[0]),
                                high=np.array(joint_constraints[1]))

        # joint rotations, xyz position of body
        self.observation_space = Box(low=np.concatenate([joint_constraints[0], [-10, -10, 0]]),
                                     high=np.concatenate([joint_constraints[1], [10, 10, 1]]))

        self.multi_dof_joints = [idx for idx in range(self.n_joints) if p.getJointInfo(self.object_id, idx)[2] != 0]
        self.single_dof_joints = [idx for idx in range(self.n_joints) if p.getJointInfo(self.object_id, idx)[2] == 0]

        ###############################################

    def step(self, action=None):
        # apply action
        if action is not None:
            p.setJointMotorControlArray(self.object_id, [i for i in range(self.n_joints)], p.POSITION_CONTROL, action)
        p.stepSimulation()

        # generate observation
        multi_joints_or = np.array(
            [p.getJointStateMultiDof(self.object_id, idx)[0] for idx in self.multi_dof_joints]).flatten()
        rev_joints_or = np.array([p.getJointState(self.object_id, idx)[0] for idx in self.single_dof_joints])

        self.position = p.getBasePositionAndOrientation(self.object_id)[0]

        observation = np.concatenate([multi_joints_or, rev_joints_or, self.position], dtype=np.float32)

        # calculate reward
        # this will be changed to better suit our environment
        reward = -(self.position[0] ** 2) + (2 * self.position[1]) ** 2 - ((self.position[2] - 0.4) ** 2)
        if reward >= self.max_reward:
            done = True
        else:
            done = False

        # gym environment returns observation, reward, True if terminal state is reached and false instead, info about environment
        return observation, reward, done, {}

    def reset(self):
        p.removeBody(self.object_id)
        self.object_id = p.loadURDF('robot/walker.urdf', self.start_position, self.start_rotation)

    def close(self):
        p.disconnect()

    def render(self, mode="human"):
        # we do nothing here because we pass render argument when creating an instance of environment
        pass
