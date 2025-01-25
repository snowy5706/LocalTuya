"""Platform to locally control Tuya-based button devices."""

import json
import logging
from functools import partial

import voluptuous as vol
from homeassistant.components.button import DOMAIN, ButtonEntity
from homeassistant.const import CONF_DEVICE_CLASS, CONF_ENTITIES, CONF_ID

from .entity import LocalTuyaEntity, async_setup_entry, get_entity_config
from .const import CONF_IR_BUTTON_HEAD, CONF_IR_BUTTON_KEY1

CONTROL_MODE = "send_ir"
PRESS_DP = 201
DYNAMIC_DP = 1000

_LOGGER = logging.getLogger(__name__)


def flow_schema(dps):
    """Return schema used in config flow."""
    return {
        vol.Optional(CONF_IR_BUTTON_HEAD): str,
        vol.Optional(CONF_IR_BUTTON_KEY1): str,
    }


class LocalTuyaButton(LocalTuyaEntity, ButtonEntity):
    """Representation of a Tuya button."""

    def __init__(
        self,
        device,
        config_entry,
        buttonid,
        **kwargs,
    ):
        """Initialize the Tuya button."""
        # Hacky way to dynamically assign dps :)
        if int(buttonid) < DYNAMIC_DP:
            next_buttonid = str(max(max([ int(e[CONF_ID]) for e in config_entry[CONF_ENTITIES] ]) + 1, DYNAMIC_DP))
            get_entity_config(config_entry, buttonid)[CONF_ID] = next_buttonid
            buttonid = next_buttonid

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
            "control": CONTROL_MODE,
            "head": self._head,
            "key1": self._key1,
            "type": 0,
            "delay": 0
        }
        await self._device.set_dp(json.dumps(command), PRESS_DP)

    # Always availiable
    @property
    def available(self):
        return True

    # Update state when there is new data from the device
    def status_updated(self):
        state = self.state
        self._state = state
        self._last_state = state

    # No need to restore state for a button
    async def restore_state_when_connected(self):
        return

async_setup_entry = partial(async_setup_entry, DOMAIN, LocalTuyaButton, flow_schema)
