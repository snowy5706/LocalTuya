"""Platform to present any Tuya DP as an enumeration."""
import logging
from functools import partial
import json
import voluptuous as vol
from homeassistant.components.button import DOMAIN, ButtonEntity

from .common import LocalTuyaEntity, async_setup_entry
from .const import (
    CONF_IR_BUTTON_HEAD,
    CONF_IR_BUTTON_KEY1
)

_LOGGER = logging.getLogger(__name__)

PRESS_DP = 201


def flow_schema(dps):
    """Return schema used in config flow."""
    return {
        vol.Required(CONF_IR_BUTTON_HEAD): str,
        vol.Required(CONF_IR_BUTTON_KEY1): str,
    }


class LocaltuyaIRButton(LocalTuyaEntity, ButtonEntity):
    """Representation of a Tuya IR Button."""

    def __init__(
        self,
        device,
        config_entry,
        sensorid,
        **kwargs,
    ):
        """Initialize the Tuya IR Button."""
        super().__init__(device, config_entry, sensorid, _LOGGER, **kwargs)
        self._head = self._config.get(CONF_IR_BUTTON_HEAD)
        self._key1 = self._config.get(CONF_IR_BUTTON_KEY1)
        _LOGGER.debug("Initialized IR Button [%s]", self.name)

    async def async_press(self) -> None:
        """Press the button."""
        command = {
            "control": "send_ir",
            "type": 0,
            "head": self._head,
            "key1": self._key1
        }
        await self._device.set_dp(json.dumps(command), PRESS_DP)


async_setup_entry = partial(async_setup_entry, DOMAIN, LocaltuyaIRButton, flow_schema)
