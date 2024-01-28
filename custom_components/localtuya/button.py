"""Platform to present any Tuya DP as a button."""
import logging
from functools import partial
import json
import voluptuous as vol
from homeassistant.components.button import DOMAIN, ButtonEntity
from homeassistant.const import CONF_DEVICE_CLASS

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


class LocaltuyaButton(LocalTuyaEntity, ButtonEntity):
    """Representation of a Tuya button."""

    def __init__(
        self,
        device,
        config_entry,
        buttonid,
        **kwargs,
    ):
        """Initialize the Tuya button."""
        super().__init__(device, config_entry, buttonid, _LOGGER, **kwargs)
        self._head = self._config.get(CONF_IR_BUTTON_HEAD)
        self._key1 = self._config.get(CONF_IR_BUTTON_KEY1)
        _LOGGER.debug("Initialized IR Button [%s]", self.name)

    @property
    def device_class(self):
        """Return the class of this device."""
        return self._config.get(CONF_DEVICE_CLASS)

    async def async_press(self) -> None:
        """Press the button."""
        command = {
            "control": "send_ir",
            "head": self._head,
            "key1": self._key1,
            "type": 0,
            "delay": 300
        }
        await self._device.set_dp(json.dumps(command), PRESS_DP)

    @property
    def available(self):
        return True

    def status_updated(self):
        state = "generic"
        self._state = state
        self._last_state = state


async_setup_entry = partial(async_setup_entry, DOMAIN, LocaltuyaButton, flow_schema)
