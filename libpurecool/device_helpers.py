from libpurecool.const import (
    DYSON_PURE_HOT_COOL_LINK_TOUR,
    DYSON_PURE_COOL,
    DYSON_PURE_COOL_DESKTOP,
    DYSON_PURE_HOT_COOL,
    DYSON_PURE_COOL_HUMIDIFY
)
from libpurecool.dyson_pure_cool import DysonPureCool
from libpurecool.dyson_pure_hotcool import DysonPureHotCool
from libpurecool.dyson_pure_hotcool_link import DysonPureHotCoolLink
from libpurecool.dyson_pure_cool_link import DysonPureCoolLink


def get_dyson_device(json_data):
    if is_heating_device(json_data['ProductType']):
        return DysonPureHotCoolLink(json_data)
    elif is_dyson_pure_cool_device(json_data['ProductType']):
        return DysonPureCool(json_data)
    elif is_heating_device_v2(json_data['ProductType']):
        return DysonPureHotCool(json_data)
    else:
        return DysonPureCoolLink(json_data)


def is_heating_device(product_type):
    """Return true if this json payload is a hot+cool device."""
    return product_type in [DYSON_PURE_HOT_COOL_LINK_TOUR]


def is_heating_device_v2(product_type):
    """Return true if this json payload is a v2 hot+cool device."""
    return product_type in [DYSON_PURE_HOT_COOL]


def is_dyson_pure_cool_device(product_type):
    """Return true if this json payload is a v2 dyson pure cool device."""
    return product_type in [DYSON_PURE_COOL,
                            DYSON_PURE_COOL_DESKTOP,
                            DYSON_PURE_COOL_HUMIDIFY]
