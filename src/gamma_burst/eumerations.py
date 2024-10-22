"""Enumerations."""

from enum import StrEnum


class ObservationMode(StrEnum):
    WT_Mode = 'WT'
    WT_Hard_Mode = 'WTHard'
    WT_Soft_Mode = 'WTSoft'
    PC_Mode = 'PC'
    PC_Hard_Mode = 'PCHard'
    PC_Soft_Mode = 'PCSoft'


class Instrument(StrEnum):
    BAT_Sensor = 'BAT' #15 - 150kev 
    BAT_Sensor_NoEvolution = 'BAT_NoEvolution' #15 - 150kev 
    XRT_Sensor = 'XRT' #0.3 - 10kev