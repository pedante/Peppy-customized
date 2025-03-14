# Copyright 2021 Peppy Player peppy.player@gmail.com
#
# This file is part of Peppy Player.
#
# Peppy Player is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Peppy Player is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Peppy Player. If not, see <http://www.gnu.org/licenses/>.

import os
import logging

from subprocess import Popen, PIPE
from util.config import DISK_MOUNT, MOUNT_POINT, MOUNT_READ_ONLY
from util.keys import KEY_MOUNT_OPTIONS, KEY_NAS, KEY_MOUNTED, KEY_FOLDER, KEY_IP_ADDRESS, KEY_NAME, \
    KEY_PASSWORD, KEY_FILESYSTEM, KEY_USERNAME

UTF8 = "utf-8"
UTF_8 = "utf-8-sig"
EOL = "\n"

class NasManager(object):
    """ NAS manager utility class """

    def __init__(self, peppy):
        """ Initializer. 
        
        :param peppy: main player class
        """
        self.peppy = peppy
        self.config = peppy.util.config
        self.read_only = self.config[DISK_MOUNT][MOUNT_READ_ONLY]
        self.mount_point_base = self.config[DISK_MOUNT][MOUNT_POINT].strip()
        if not self.mount_point_base.endswith(os.sep):
            self.mount_point_base += os.sep

    def get_nases(self):
        """ Get the list of dictionaries representing each configured NAS

        :return: list of configured NASes
        """
        self.peppy.util.config_class.load_nas_config(self.config)
        nases = []

        for nas in self.config[KEY_NAS]:
            nas[KEY_MOUNTED] = self.is_nas_mounted(nas)
            nases.append(nas)

        return nases

    def is_nas_mounted(self, nas):
        """ Check if NAS is mounted
        
        :param nas: NAS to check

        :return: True - NAS mounted, False - NAS unmounted
        """
        device_name = "//" + nas[KEY_IP_ADDRESS] + "/" + nas[KEY_FOLDER]
        filesystem = nas[KEY_FILESYSTEM]
        command = ("mount -t " + filesystem).split()

        subp = Popen(command, shell=False, stdout=PIPE)
        result = subp.stdout.read()
        decoded = result.decode(UTF_8)
        lines = decoded.split("\n")
        for line in lines:
            if line.strip().startswith(device_name):
                return True
        return False

    def mount(self, nas):
        """ Mount NAS

        :param nas: NAS to mount

        :return: True - disk mount was successful, False - otherwise
        """
        
        name = nas[KEY_NAME]
        filesystem = nas[KEY_FILESYSTEM]
        ip_address = nas[KEY_IP_ADDRESS]
        username = nas[KEY_USERNAME]
        password = nas[KEY_PASSWORD]
        folder = nas[KEY_FOLDER]
        mount_options = nas[KEY_MOUNT_OPTIONS]
        base = self.config[DISK_MOUNT][MOUNT_POINT].strip()
        if not base.endswith(os.sep):
            base += os.sep
        mount_point = base + name
        mounted = self.is_nas_mounted(nas)

        if mounted:
            logging.debug(f"Device {name} mounted already to {self.mount_point_base}")
            return True

        mount_point = self.mount_point_base + name

        if os.path.ismount(mount_point):
            logging.debug(f"The mount point {mount_point} is in use already")
            return False

        if os.path.exists(mount_point):
            logging.debug(f"The mount point {mount_point} exists")
        else:
            try:
                os.makedirs(mount_point)
            except Exception as e:
                logging.debug(e)
                return False

        command = ("sudo mount -t " + filesystem).split()
        credentials = "username=" + username + ",password=" + password

        if self.read_only:
            command.append("-o")
            command.append("ro")

        command.append("-o")
        if mount_options:
            command.append(mount_options + "," + credentials)
        else:
            command.append(credentials)

        command.append("//" + ip_address + "/" + folder)
        command.append(mount_point)
        logging.debug(command)

        p = Popen(command, stdout=PIPE, stderr=PIPE)
        _, error = p.communicate()
        if p.returncode != 0:
            logging.debug(f"NAS mount failed with error: {error.decode(UTF8).rstrip(EOL)}")
            logging.debug(f"Failed NAS mount command: {command}")
            return False
        else:
            logging.debug(f"Successfully mounted {name} to {mount_point}")
            return True

    def unmount(self, nas):
        """ Unmount NAS

        :param nas: NAS to unmount

        :return: True - disk unmount was successful, False - otherwise
        """
        ip_address = nas[KEY_IP_ADDRESS]
        folder = nas[KEY_FOLDER]
        device_name = "//" + ip_address + "/" + folder
        p = Popen(["sudo", "umount", device_name], stdout=PIPE, stderr=PIPE)
        _, error = p.communicate()
        if p.returncode != 0:
            logging.debug(f"Unmount failed with error: {error.decode(UTF8).rstrip(EOL)}")
            return False
        else:
            logging.debug(f"Successfully unmounted {device_name}")
            return True

    def poweroff(self, nas):
        """ Poweroff provided NAS. 
        If device is busy switch off player, go to Home and umnount

        :param nas: the NAS to handle

        :return: True - poweroff procedure was successful, False - otherwise
        """
        if self.is_nas_mounted(nas):
            unmounted = self.unmount(nas)    
            if not unmounted:
                self.peppy.player.stop()
                self.peppy.go_home(None)
                self.unmount(nas)

    def mount_all_nases(self):
        """ Mount all NASes """

        nases = self.get_nases()
        for n in nases:
            self.mount(n)

    def poweroff_all_nases(self):
        """ Poweroff all configured NASes """

        nases = self.get_nases()
        for nas in nases:
            self.poweroff(nas)
