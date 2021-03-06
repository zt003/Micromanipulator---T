'''
This file contains the the submethods for the I2C Stages.
#####################DO NOT EDIT BELOW INFORMATION##################################
Originating Branch: MergeStageClasses
Originally Created: Zheng Tian 05/2018
Last Edited By: Zheng Tian 07/2018
'''
import Stage
import smbus
import time
import binascii
from Stage import Stage
from helper import *


class StageI2C(Stage):
    def __init__(self, address, position, bus):
        Stage.__init__(self, position)
        self.position = position
        self.address = address
        self.bus = smbus.SMBus(bus)  # Initialize the SMBus(I2C, lookup the differences)
        self.home = 6000

    def zMove(self, direction, encoder_counts):
        """
        :param direction: The direction for Z to move. 1= up 0 = down
        :param encoder_counts: number of encoder counts to move
        :return: NA
        """
        command = '06 ' + str(direction)
        self.sendCommand(command, encodeToCommand(encoder_counts))

    def write(self, command):
        """
        The command to write to the stages in I2C.
        :param command: Command in the form of a list of decimal integers, each of which represents an ascii character
        in the command to be sent to the stage.
        :return:
        """
        print(commandToString(command))  # print the command in  a user readable format.
        self.bus.write_i2c_block_data(self.address, 0, command)

    def read(self):
        """
        Reads from the output register of the stage. I think that there may be a limit to the number of bits that can
        be read back but I am not entirely sure. This should be checked.
        :return: List of signed values that represent what is on the output register of the stage
        """
        temp = self.bus.read_i2c_block_data(self.address, 0)
        print('temp', temp)
        return_buffer = []
        for i in temp:
            return_buffer += str(chr(int(i)))

        return return_buffer

    def getstatus(self):
        self.sendCommandNoVars('10')  # send query asking about motor status and position
        temp = self.read()  # store incoming data from motor in list
        #return temp

        rcvEncodedStatus = ''
        for element in range(6):
            rcvEncodedStatus += str(temp[4 + element])
        #print(rcvEncodedStatus)

        status = ''
        for element in range(len(rcvEncodedStatus)):
            # binary_string = binascii.unhexlify(rcvEncodedStatus[element])
            # status += binary_string
            binary_string = format(int(rcvEncodedStatus[element]),'04b')
            status += binary_string

        return status

    # def MotorDirection(self,status):
    #     if status[1] == '0':
    #         print('Running Reverse')
    #     else:
    #         print('Running Forward')
    #
    # def Running (self, status):
    #     if status[1] == '0':
    #         print('Motor is not running')
    #     else:
    #         print('Motor is running')
