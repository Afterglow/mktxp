# coding=utf8
## Copyright (c) 2023 Paul Thomas
##
## This program is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License
## as published by the Free Software Foundation; either version 2
## of the License, or (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

from mktxp.cli.config.config import MKTXPConfigKeys
from mktxp.collector.base_collector import BaseCollector
from mktxp.datasource.bgp_session_ds import BGPSessionMetricsDataSource

class BGPSessionCollector(BaseCollector):
    ''' BGP Session Metrics collector
    '''

    @staticmethod
    def collect(router_entry):
        if not router_entry.config_entry.bgp_session:
            return

        session_labels = ['established', 'remote.address', 'remote.as', 'remote.messages', 'remote.bytes', 'local.address', 'local.as', 'local.messages', 'local.bytes']
        session_records = BGPSessionMetricsDataSource.metric_records(router_entry, metric_labels = session_labels)
        if session_records:
            # Compile total sessions records
            total_bgp_sessions = len(session_records)
            total_bgp_sessions_records = [{
                MKTXPConfigKeys.ROUTERBOARD_NAME: router_entry.router_id[MKTXPConfigKeys.ROUTERBOARD_NAME],
                MKTXPConfigKeys.ROUTERBOARD_ADDRESS: router_entry.router_id[MKTXPConfigKeys.ROUTERBOARD_ADDRESS],
                'count': total_bgp_sessions
            }]
            total_sessions_metrics = BaseCollector.gauge_collector(
                'bgp_sessions_total_sessions',
                'Total number of BGP sessions',
                total_bgp_sessions_records,
                'count'
            )
            yield total_sessions_metrics

            session_labels.remove('remote.bytes')
            bgp_session_metrics_gauge = BaseCollector.gauge_collector(
                'bgp_session_info',
                'BGP Established Sessions',
                session_records,
                'remote_bytes',
                session_labels
            )
            yield bgp_session_metrics_gauge