from typing import Any, Dict, Optional

import voluptuous as vol

from solaxev.inverter import Inverter
from solaxev.units import DailyTotal, Measurement, Total, Units
from solaxev.utils import (
    div10,
    div100,
    pack_u16,
    to_signed,
    to_signed32,
    twoway_div10,
    twoway_div100,
)


class X3Ultra(Inverter):
    """X3 Ultra v1.001.20"""

    # pylint: disable=duplicate-code
    _schema = vol.Schema(
        {
            vol.Required("type"): vol.All(int, 25),
            vol.Required("sn"): str,
            vol.Required("ver"): str,
            vol.Required("data"): vol.Schema(
                vol.All(
                    [vol.Coerce(float)],
                    vol.Length(min=300, max=300),
                )
            ),
            vol.Required("information"): vol.Schema(
                vol.All(vol.Length(min=10, max=10))
            ),
        },
        extra=vol.REMOVE_EXTRA,
    )

    @classmethod
    def build_all_variants(cls, host, port, pwd=""):
        return [cls._build(host, port, pwd, False)]

    @classmethod
    def _decode_run_mode(cls, run_mode):
        return {
            0: "Waiting",
            1: "Checking",
            2: "Normal",
            3: "Fault",
            4: "Permanent Fault",
            5: "Updating",
            6: "EPS Check",
            7: "EPS Mode",
            8: "Self Test",
            9: "Idle",
            10: "Standby",
        }.get(run_mode)

    @classmethod
    def response_decoder(cls):
        return {
            "Grid 1 Voltage": (0, Units.V, div10),
            "Grid 2 Voltage": (1, Units.V, div10),
            "Grid 3 Voltage": (2, Units.V, div10),
            "Grid 1 Current": (3, Units.A, twoway_div10),
            "Grid 2 Current": (4, Units.A, twoway_div10),
            "Grid 3 Current": (5, Units.A, twoway_div10),
            "Grid 1 Power": (6, Units.W, to_signed),
            "Grid 2 Power": (7, Units.W, to_signed),
            "Grid 3 Power": (8, Units.W, to_signed),
            "PV1 Voltage": (10, Units.V, div10),
            "PV2 Voltage": (11, Units.V, div10),
            "PV3 Voltage": (129, Units.V, div10),
            "PV1 Current": (12, Units.A, div10),
            "PV2 Current": (13, Units.A, div10),
            "PV3 Current": (130, Units.A, div10),
            "PV1 Power": (14, Units.W),
            "PV2 Power": (15, Units.W),
            "PV3 Power": (131, Units.W),
            "Grid 1 Frequency": (16, Units.HZ, div100),
            "Grid 2 Frequency": (17, Units.HZ, div100),
            "Grid 3 Frequency": (18, Units.HZ, div100),
            # "Run mode": (19, Units.NONE), # Only use the index once due to HA uids
            "Run mode text": (19, Units.NONE, X3Ultra._decode_run_mode),
            "EPS 1 Voltage": (23, Units.V, div10),
            "EPS 2 Voltage": (24, Units.V, div10),
            "EPS 3 Voltage": (25, Units.V, div10),
            "EPS 1 Current": (26, Units.A, twoway_div10),
            "EPS 2 Current": (27, Units.A, twoway_div10),
            "EPS 3 Current": (28, Units.A, twoway_div10),
            "EPS 1 Power": (29, Units.W, to_signed),
            "EPS 2 Power": (30, Units.W, to_signed),
            "EPS 3 Power": (31, Units.W, to_signed),
            "Grid Power": (pack_u16(34, 35), Units.W, to_signed32),
            "Battery 1 Voltage": (39, Units.V, div10),
            "Battery 2 Voltage": (132, Units.V, div10),
            "Battery 1 Current": (40, Units.A, twoway_div100),
            "Battery 2 Current": (133, Units.A, twoway_div100),
            "Battery 1 Power": (41, Units.W, to_signed),
            "Battery 2 Power": (134, Units.W, to_signed),
            "Battery 1 Remaining Capacity": (103, Units.PERCENT),
            "Battery 2 Remaining Capacity": (140, Units.PERCENT),
            "Battery 1 Temperature": (105, Units.C, to_signed),
            "Battery 2 Temperature": (142, Units.C, to_signed),
            "Load/Generator Power": (47, Units.W, to_signed),
            "Radiator Temperature": (54, Units.C, to_signed),
            "Yield total": (pack_u16(58, 59), Total(Units.KWH), div10),
            "Yield today": (70, DailyTotal(Units.KWH), div10),
            "Battery Discharge Energy total": (
                pack_u16(74, 75),
                Total(Units.KWH),
                div10,
            ),
            "Battery Charge Energy total": (pack_u16(76, 77), Total(Units.KWH), div10),
            "Battery Discharge Energy today": (78, DailyTotal(Units.KWH), div10),
            "Battery Charge Energy today": (79, DailyTotal(Units.KWH), div10),
            "PV Energy total": (pack_u16(80, 81), Total(Units.KWH), div10),
            "EPS Energy total": (pack_u16(83, 84), Total(Units.KWH), div10),
            "EPS Energy today": (85, DailyTotal(Units.KWH), div10),
            "Feed-in Energy total": (pack_u16(86, 87), Total(Units.KWH), div100),
            "Grid Consumed Energy total": (pack_u16(88, 89), Total(Units.KWH), div100),
            "Feed-in Energy today": (pack_u16(90, 91), DailyTotal(Units.KWH), div100),
            "Grid Consumed Energy today": (
                pack_u16(92, 93),
                DailyTotal(Units.KWH),
                div100,
            ),
            "Battery Remaining Capacity": (158, Units.PERCENT),
            "Battery Remaining Energy": (
                106,
                Measurement(Units.KWH, storage=True),
                div10,
            ),
            "Inverter Power": (159, Units.W, div10),
        }

    # pylint: enable=duplicate-code

    @classmethod
    def inverter_serial_number_getter(cls, response: Dict[str, Any]) -> Optional[str]:
        return response["information"][2]
