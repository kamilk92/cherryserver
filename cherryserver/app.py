import cherrypy

from aijinmlplatform.core.endpoint.estimate.estimate_endpoint import EstimateEndpoint
from aijinmlplatform.core.endpoint.health.health_endpoint import HealthEndpoint
from aijinmlplatform.core.server.cherrypy.cherrypy_server import CherrypyServer

from aijinmlplatform.util import log_util


def main():
    cherrypy.config.update({'log.screen': False,
                            'log.access_file': '',
                            'log.error_file': ''})
    log_util.setup_logging("cherrypy-logging.yaml")
    server_config = CherrypyServer.CherrypyServerConfig(CherrypyServer.DEFAULT_ADDR, 5000, "/app")
    server = CherrypyServer(server_config)

    health_endpoint = HealthEndpoint()
    server.register_endpoint(health_endpoint)

    estimate_endpoint = EstimateEndpoint()
    server.register_endpoint(estimate_endpoint)

    server.start()


if __name__ == "__main__":
    main()
