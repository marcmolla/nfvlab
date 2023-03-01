#!/usr/bin/env python3
# Copyright 2023 Student
# See LICENSE file for licensing details.

"""Charm the application."""

import logging

from subprocess import check_call, CalledProcessError

from ops.charm import CharmBase
from ops.main import main
from ops.model import ActiveStatus, MaintenanceStatus, BlockedStatus

logger = logging.getLogger(__name__)


class CaptiveCharm(CharmBase):
    """Charm the application."""

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.install, self._on_install)
        self.framework.observe(self.on.config_changed, self._on_config_changed)
        self.framework.observe(self.on.start, self._on_start)
        self.framework.observe(self.on.website_relation_joined, self._on_website_relation_joined)
        self.framework.observe(self.on.start_service_action, self._on_start_service_action)
        self.framework.observe(self.on.stop_service_action, self._on_stop_service_action)
        self.framework.observe(self.on.upgrade_charm, self._on_upgrade_charm)

    def _on_upgrade_charm(self, event):
        self.unit.status = ActiveStatus("Upgraded")

    def _on_install(self, event):
        """ Install is the first hook called when deploying"""
        logger.info("Step 1/3: INSTALL")
        self.unit.status = MaintenanceStatus("Step: 1/3")
        try:
            check_call(["apt-get", "install", "-y", "nginx"])
        except CalledProcessError as err:
            logger.error("package install failed with error code: %d", err.returncode)
            self.unit.status = BlockedStatus("Failed to install package nginx")

    def _on_config_changed(self, event):
        """ config_changed os the second hook"""
        logger.info("Step 2/3: CONFIG_CHANGED")
        brand = self.model.config["brand"]
        unit_name = self.unit.name

        landing_page = """<!DOCTYPE html> <html lang="en">
        <head>
            <meta charset="UTF-8">
                <title>{brand} captive portal</title>
        </head>
        <body>
            <h1>Served from {unit_name}</h1> </body>
        </html>
         """.format(brand=brand, unit_name=unit_name)

        with open('/var/www/html/index.nginx-debian.html', 'w+', encoding="utf-8") as fd:
            fd.write(landing_page)
            fd.flush()

    def _on_start(self, event):
        """start is the last hook"""
        logger.info("Step 3/3: START")
        self.unit.status = ActiveStatus("Step: 3/3")
        try:
            check_call(["systemctl", "restart", "nginx"])
        except CalledProcessError as err:
            logger.error("error starting nginx with error code: %d", err.returncode)
            self.unit.status = BlockedStatus("Failed to start nginx")

    def _on_website_relation_joined(self, event):
        # Gets the model for website relation
        relation = self.model.get_relation("website")
        # Gets the binding for the relation
        binding = self.model.get_binding(event.relation)
        if binding:
            relation.data[self.unit].update(
                {
                    "hostname": str(binding.network.ingress_address),
                    "port": "80"
                }
        )
            
    def _on_start_service_action(self, event):
        logger.info("Starting service")
        try:
            check_call(["systemctl", "restart", "nginx"])
        except CalledProcessError as err:
            logger.error("error starting nginx with error code: %d", err.returncode)
            self.unit.status = BlockedStatus("Failed to start nginx")

    def _on_stop_service_action(self, event):
        logger.info("Stopping service")
        try:
            check_call(["systemctl", "stop", "nginx"])
        except CalledProcessError as err:
            logger.error("error starting nginx with error code: %d", err.returncode)
            self.unit.status = BlockedStatus("Failed to start nginx")

if __name__ == "__main__":  # pragma: nocover
    main(CaptiveCharm)
