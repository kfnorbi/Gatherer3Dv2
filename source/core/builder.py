#!/usr/bin/env python

from typing import List
from core.config_constants import *
import core.config_types as g3d_cfg
import inputs as g3d_in
import outputs as g3d_out

from core.process_loop import ProcessLoop
import sys


class G3DBuilder():
    def __init__(self, cfg: g3d_cfg.Config):
        self._cfg = cfg

    def build_loop(self) -> ProcessLoop:
        return ProcessLoop(self.build_input(), self.build_outputs())

    def build_outputs(self) -> List:
        result = []

        if OutputMode.VIDEO in self._cfg.output_mode:
            result.append(g3d_out.G3DVidoOut(self._cfg.output_path + self._cfg.output_file,
                                             self._cfg.resolution[0], self._cfg.resolution[1]))

        if OutputMode.IMAGES in self._cfg.output_mode:
            result.append(g3d_out.G3DImagesOut(self._cfg.output_path + self._cfg.output_file))

        if OutputMode.STREAM in self._cfg.output_mode:
            result.append(g3d_out.G3DStreamOut(self._cfg.streaner_path,
                                               self._cfg.streamer_res[0], self._cfg.streamer_res[1],
                                               self._cfg.streamer_fps))

        if OutputMode.CALIB_BOARD in self._cfg.output_mode:
            temp = g3d_out.G3DCalibration(self._cfg)
            temp.generateChArucoPlane()

            print("Calibration Data exported!")
            sys.exit(0)

        if OutputMode.CALIBRATION in self._cfg.output_mode:
            result.append(g3d_out.G3DCalibration(self._cfg))

        if OutputMode.MESH in self._cfg.output_mode:
            result.append(g3d_out.G3dMesh(self._cfg))

        return result

    def build_input(self) -> g3d_in.G3DInput:
        result = None

        if self._cfg.input_mode == InputMode.CAMERA:
            result = g3d_in.G3DCameraIn(self._cfg.input_name,
                                        self._cfg.resolution[0], self._cfg.resolution[1],
                                        self._cfg.input_exposure, self._cfg.input_fps,
                                        self._cfg.laser_gpio, True)
        elif self._cfg.input_mode == InputMode.IMAGES:
            result = g3d_in.G3DImagesIn(self._cfg.input_folder + self._cfg.input_name)
        elif self._cfg.input_mode == InputMode.VIDEO:
            result = g3d_in.G3DVideoIn(self._cfg.input_folder + self._cfg.input_name)

        return result
