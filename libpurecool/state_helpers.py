from libpurecool.const import (
    DYSON_PURE_HOT_COOL_LINK_TOUR,
    DYSON_PURE_COOL,
    DYSON_PURE_COOL_DESKTOP,
    DYSON_PURE_HOT_COOL,
    DYSON_PURE_COOL_HUMIDIFY
)
from libpurecool.dyson_pure_state import DysonPureHotCoolState, DysonPureCoolState, DysonEnvironmentalSensorState
from libpurecool.dyson_pure_state_v2 import DysonPureHotCoolV2State, DysonPureCoolV2State, DysonEnvironmentalSensorV2State


def get_state_msg(product_type, payload):
    if support_heating(product_type):
        return DysonPureHotCoolState(payload)
    elif support_heating_v2(product_type):
        return DysonPureHotCoolV2State(payload)
    elif is_pure_cool_v2(product_type):
        return DysonPureCoolV2State(payload)
    else:
        return DysonPureCoolState(payload)


def get_environmental_sensor_msg(product_type, payload):
    if is_pure_cool_v2(product_type):
        return DysonEnvironmentalSensorV2State(payload)
    else:
        return DysonEnvironmentalSensorState(payload)


def support_heating(product_type):
    """Return True if device_model support heating mode, else False.

    :param product_type Dyson device model
    """
    return product_type in [DYSON_PURE_HOT_COOL_LINK_TOUR]


def support_heating_v2(product_type):
    """Return True if v2 device_model support heating mode, else False.

    :param product_type Dyson device model
    """
    return product_type in [DYSON_PURE_HOT_COOL]


def is_pure_cool_v2(product_type):
    """Return True if it is a v2 dyson pure cool device.

    :param product_type Dyson device model
    """
    return product_type in [DYSON_PURE_COOL, DYSON_PURE_COOL_DESKTOP,
                            DYSON_PURE_HOT_COOL, DYSON_PURE_COOL_HUMIDIFY]
