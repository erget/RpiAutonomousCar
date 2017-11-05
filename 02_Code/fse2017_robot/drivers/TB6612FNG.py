#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of FSE 2017.
#
# FSE 2017 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# FSE 2017 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with FSE 2017.  If not, see <http://www.gnu.org/licenses/>.

import sys
import time

import wiringpi
from gpio_manager import GPIO_Manager


class TB6612FNG(GPIO_Manager):
    """Interface with a TB6612FNG DC Motor driver."""
   # Motor1 configuration
    _m1_dir1_pin = 6
    _m1_dir2_pin = 12
    _m1_pwm_pin_annex = 5  # solve error mapping (Vers.01)
    _m1_pwm_pin = 18

    # Motor2 configuration
    _m2_dir1_pin = 19
    _m2_dir2_pin = 16
    _m2_pwm_pin_annex = 26  # solve error mapping (Vers.01)
    _m2_pwm_pin = 13

    _standby_pin = 20

    PWM_OUTPUTS = [_m1_pwm_pin, _m2_pwm_pin]

    INPUT_PINS = [_m1_pwm_pin_annex, _m2_pwm_pin_annex]

    OUTPUT_PINS = [_m1_dir1_pin, _m1_dir2_pin,
                   _m2_dir1_pin, _m2_dir2_pin,
                   _standby_pin]
    pins = PWM_OUTPUTS + INPUT_PINS + OUTPUT_PINS

    @staticmethod
    def to_dc(dc):
        return (1023 * dc) / 100

    def __init__(self):
        super(TB6612FNG, self).__init__()
        for pin in self.OUTPUT_PINS:
            wiringpi.pinMode(pin, wiringpi.OUTPUT)

        for pin in self.PWM_OUTPUTS:
            wiringpi.pinMode(pin, wiringpi.PWM_OUTPUT)

        for pin in self.INPUT_PINS:
            wiringpi.pinMode(pin, wiringpi.INPUT)
            wiringpi.pullUpDnControl(pin,wiringpi.PUD_DOWN) # make sure all annex_pin are set LOW

    def right_forward(self):
        """Drive right motor forward."""
        wiringpi.digitalWrite(self._m1_dir1_pin, wiringpi.LOW)
        wiringpi.digitalWrite(self._m1_dir2_pin, wiringpi.HIGH)

    def right_back(self):
        """Drive right motor back."""
        wiringpi.digitalWrite(self._m1_dir1_pin, wiringpi.HIGH)
        wiringpi.digitalWrite(self._m1_dir2_pin, wiringpi.LOW)

    def left_forward(self):
        """Drive left motor forward."""
        wiringpi.digitalWrite(self._m2_dir1_pin, wiringpi.HIGH)
        wiringpi.digitalWrite(self._m2_dir2_pin, wiringpi.LOW)

    def left_back(self):
        """Drive left motor back."""
        wiringpi.digitalWrite(self._m2_dir1_pin, wiringpi.LOW)
        wiringpi.digitalWrite(self._m2_dir2_pin, wiringpi.HIGH)

    def forward(self, duty_cycle=25):
        """Drive chassis forward."""
        self.right_forward()
        self.left_forward()
        wiringpi.pwmWrite(self._m1_pwm_pin, self.to_dc(duty_cycle))
        wiringpi.pwmWrite(self._m2_pwm_pin, self.to_dc(duty_cycle))
        wiringpi.digitalWrite(self._standby_pin, wiringpi.HIGH)

    def reverse(self, duty_cycle=25):
        """Drive chassis back."""
        self.right_back()
        self.left_back()
        wiringpi.pwmWrite(self._m1_pwm_pin, self.to_dc(duty_cycle))
        wiringpi.pwmWrite(self._m2_pwm_pin, self.to_dc(duty_cycle))
        wiringpi.digitalWrite(self._standby_pin, wiringpi.HIGH)

    def right(self, duty_cycle=25):
        """Turn chassis clockwise."""
        self.right_forward()
        self.left_back()
        wiringpi.pwmWrite(self._m1_pwm_pin, self.to_dc(duty_cycle))
        wiringpi.pwmWrite(self._m2_pwm_pin, self.to_dc(duty_cycle))
        wiringpi.digitalWrite(self._standby_pin, wiringpi.HIGH)

    def left(self, duty_cycle=25):
        """Turn chassis counterclockwise."""
        self.right_back()
        self.left_forward()
        wiringpi.pwmWrite(self._m1_pwm_pin, self.to_dc(duty_cycle))
        wiringpi.pwmWrite(self._m2_pwm_pin, self.to_dc(duty_cycle))
        wiringpi.digitalWrite(self._standby_pin, wiringpi.HIGH)

    def stop(self):
        """Stop chassis."""
        for pin in self.PWM_OUTPUTS:
            wiringpi.pwmWrite(pin, 0)
        for pin in self.OUTPUT_PINS:
            wiringpi.digitalWrite(pin, wiringpi.LOW)

    def __exit__(self, *args):
        wiringpi.pwmWrite(self._m1_pwm_pin, 0)
        wiringpi.pwmWrite(self._m2_pwm_pin, 0)
        super(TB6612FNG, self).__exit__()


if __name__ == '__main__':
    with TB6612FNG() as tb6612fng:
        while True:
            print "forward"
            tb6612fng.forward()
            time.sleep(3)

            tb6612fng.stop()
            time.sleep(3)

            print "reverse"
            tb6612fng.reverse()
            time.sleep(3)

            tb6612fng.stop()
            time.sleep(3)

            print "left"
            tb6612fng.left()
            time.sleep(3)

            tb6612fng.stop()
            time.sleep(3)

            print "right"
            tb6612fng.right()
            time.sleep(3)

            tb6612fng.stop()
            time.sleep(3)

            print "Done!"


