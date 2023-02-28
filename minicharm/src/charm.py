#!/usr/bin/env python3
# Copyright 2023 Student
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

import logging

from ops.charm import CharmBase
from ops.main import main
from ops.model import ActiveStatus, WaitingStatus

# Log messages can be retrieved using juju debug-log
logger = logging.getLogger(__name__)



class MinicharmCharm(CharmBase):
    """Mini charm"""

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.install, self._on_install)
        self.framework.observe(self.on.config_changed, self._on_config_changed)
        self.framework.observe(self.on.start, self._on_start)

    def _on_install(self, event):
        """ Install is the first hook called when deploying"""
        logger.info("Step 1/3: INSTALL")
        self.unit.status = MaintenanceStatus("Step: 1/3")

    def _on_config_changed(self, event):
        """ config_changed os the second hook"""
        logger.info("Step 2/3: CONFIG_CHANGED")
        self.unit.status = MaintenanceStatus("Step: 2/3")

    def _on_start(self, event):
        """start is the last hook"""
        logger.info("Step 3/3: START")
        self.unit.status = ActiveStatus("Step: 3/3")

if __name__ == "__main__":  # pragma: nocover
    main(MinicharmCharm)
