from typing import Any, Dict, Optional

import voluptuous as vol

from solaxev.inverter import Inverter
from solaxev.units import DailyTotal, Total, Units
from solaxev.utils import div10, div100, pack_u16, to_signed, to_signed32


class EVHBI7(Inverter):
    # pylint: disable=duplicate-code
    _schema = vol.Schema(
        {
            vol.Required("type"): vol.All(int, 19),
            vol.Required(
                "sn",
            ): str,
            vol.Required("ver"): str,
            vol.Required("data"): vol.Schema(
                vol.All(
                    [vol.Coerce(float)],
                    vol.Length(min=296, max=296),
                )
            ),
            vol.Required("information"): vol.Schema(vol.All(vol.Length(min=10, max=10))),
        },
        extra=vol.REMOVE_EXTRA,
    )

    @classmethod
    def _decode_run_mode(cls, run_mode):
        return {
            1: "Self Use",
            2: "TOU",
            3: "Backup Mode",
            4: "Feed-in Priority",
            5: "Demand Mode",
            6: "ConstPower Mode",
            7: "Enhanced TOU",
        }.get(run_mode)

    @classmethod
    def build_all_variants(cls, host, port, pwd=""):
        versions = [cls._build(host, port, pwd, False)]
        return versions

    @classmethod
    def response_decoder(cls):
        return {
            "Run mode": (3, Units.NONE, EVHBI7._decode_run_mode),
            "AC voltage R": (4, Units.V, div10),
            "AC current": (5, Units.A, div10),
            "AC power": (6, Units.W, to_signed),
            "Grid frequency": (7, Units.HZ, div100),
            "PV1 voltage": (11, Units.V, div10),
            "PV2 voltage": (12, Units.V, div10),
            "PV3 voltage": (13, Units.V, div10),
            "PV1 current": (15, Units.A, div10),
            "PV2 current": (16, Units.A, div10),
            "PV3 current": (17, Units.A, div10),
            "PV1 power": (19, Units.W),
            "PV2 power": (20, Units.W),
            "PV3 power": (21, Units.W),
            "Total DC generation": (pack_u16(44, 45), Total(Units.KWH), div10),
            "On-grid total yield": (pack_u16(41, 42), Total(Units.KWH), div10),
            "On-grid daily yield": (43, DailyTotal(Units.KWH), div10),
            "On-grid daily export": (37, DailyTotal(Units.KWH), div10),
            "On-grid daily import": (39, DailyTotal(Units.KWH), div10),
            "Battery voltage": (89, Units.V, div100),
            "Battery current": (90, Units.A, div100),
            "Battery power": (91, Units.W, to_signed),
            "Battery temperature": (92, Units.C),
            "Battery SoC": (93, Units.PERCENT),
            "Battery capacity": (99, Units.KWH, div10),
            "Inverter Temperature": (75, Units.C),
            "Grid power": (32, Units.W, to_signed),
            "Total feed-in energy": (pack_u16(33, 34), Total(Units.KWH), div10),
            "Total consumption": (pack_u16(35, 36), Total(Units.KWH), div10),
            "PV Today": (46, DailyTotal(Units.KWH), div10),
            "Current consumption": (30, Units.W, to_signed),
            "Current export": (pack_u16(28, 29), Units.W, to_signed32),
            "Current SCH1 consumption": (255, Units.W),
            "Current SCH2 consumption": (261, Units.W),
            "Current SCH3 consumption": (267, Units.W),
        }

    @classmethod
    def inverter_serial_number_getter(cls, response: Dict[str, Any]) -> Optional[str]:
        return response["information"][2]
