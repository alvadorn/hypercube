from ryu.base import app_manager
from ryu.lib.packet import packet, ethernet
from ryu.controller import dpset, handler, ofp_event


class HypercubeApp(app_manager.RyuApp):

    def __init__(self, *args, **kwargs):
        super(HypercubeApp, self).__init__(*args, **kwargs)

    @handler.set_ev_cls(dpset.EventDP, dpset.DPSET_EV_DISPATCHER)
    def handler_datapath(self, ev):
        print(ev)
        self.logger.debug(ev)
        if ev.enter == True:
            self.logger.debug(ev)

    @handler.set_ev_cls(ofp_event.EventOFPPacketIn, handler.MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        pass
