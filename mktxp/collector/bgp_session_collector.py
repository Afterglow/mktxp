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

        session_labels = ['established', 'remote_address', 'remote_as', 'remote_messages', 'remote_bytes', 'local_address', 'local_as', 'local_messages', 'local_bytes']
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

            session_labels.remove('established')
            bgp_session_metrics_gauge = BaseCollector.gauge_collector(
                'bgp_session_info',
                'BGP Sessions',
                session_records,
                'established',
                session_labels
            )
            yield bgp_session_metrics_gauge