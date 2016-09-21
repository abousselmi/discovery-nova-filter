# Copyright (c) 2016 Orange
# All Rights Reserved.
##    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
##         http://www.apache.org/licenses/LICENSE-2.0
##    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo_config import cfg
from oslo_log import log as logging
from nova.scheduler import filters 
from nova.scheduler.filters import utils

LOG = logging.getLogger(__name__)
CONF = cfg.CONF

discovery_locality_opts = [
    cfg.StrOpt('discovery_locality', default='RegionOne', 
               help='Default discovery locality'),
    cfg.BoolOpt('enable_discovery_locality', default=False,
                help='Enable the discovery filter. Defaults to False.'),
]

CONF.register_opts(discovery_locality_opts)

class DiscoveryLucosFilter(filters.BaseHostFilter):
    """Filters Hosts by dicovery_lucos locality.

    This is a dump filter that just compares region name with
    the host name prefix. May be conceived in an other way in the 
    future. Works with host names, using the key 'discovery_locality'
    Note: a host is a part of a single discovery locality
    """

    # Nodes locality do not change within a request
    run_filter_once_per_request = True

    def host_passes(self, host_state, filter_properties):

        # Node passes by default. The filter plays a pass through if not
        # enabled.
        host_passes = True

        if CONF.enable_discovery_locality:
            LOG.debug("DISCOVERY locality filter is enabled.")

            # Node does not pass by default when the filter is enabled
            host_passes = False

            discovery_locality = CONF.discovery_locality
            LOG.debug("DISCOVERY locality '%(loc)s' found. ",
                      {'loc': discovery_locality})
    
            discovery_node = host_state.host
            LOG.debug("DISCOVERY node '%(node)s' found. ",
                      {'node': discovery_node})
    
            if discovery_node.lower().startswith(
                discovery_locality.lower()):
                host_passes = True

            if not host_passes:
                LOG.debug("DISCOVERY locality '%(loc)s' requested. Node "
                          "'%(node)s' does not belong to this locality.",
                          {'loc': discovery_locality, 
                           'node': discovery_node})

        return host_passes
