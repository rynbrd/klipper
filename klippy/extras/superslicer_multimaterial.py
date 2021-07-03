# Extras module for improving SuperSlicer's multimaterial handling in Klipper.
#
# Copyright (C) 2021 Google, authored by Ryan Bourgeois <bluedragonx@gmail.com>
#
# This file may be distributed under the terms of the GNU GPLv3 license.
import logging

class SuperslicerMultimaterial:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.printer.register_event_handler("gcode:command_exec", self._handle_gcode_command_exec)
        self.pressure_advance = 0

    def _get_pressure_advance(self):
        extruder = self.printer.lookup_object('toolhead').get_extruder()
        return extruder.pressure_advance

    def _handle_gcode_command_exec(self, commands):
        if 'CP TOOLCHANGE LOAD' in commands[0]:
            self.pressure_advance = self._get_pressure_advance()
            logging.info("Disable pressure advance for toolchange.")
            commands.append('SET_PRESSURE_ADVANCE ADVANCE=0')
        elif 'CP TOOLCHANGE WIPE' in commands[0]:
            logging.info("Restoring pressure advance {:.3f} after toolchange."
                .format(self.pressure_advance))
            commands.append('SET_PRESSURE_ADVANCE ADVANCE={:.3f}'
                .format(self.pressure_advance))

def load_config(config):
    return SuperslicerMultimaterial(config)
