from ryu.base import app_manager
from ryu.lib.packet import packet, ethernet
from ryu.controller import dpset, handler, ofp_event

# first packet send libs
import threading
import time

# personal libs
import util

SLEEP_SECS=2.0
nodes_count = 0

class FirstPacketSender(threading.Thread):
    def __init__(self, dp, count):
        threading.Thread.__init__(self)
        self.dp = dp
        self.count = count

    def run(self):
        time.sleep(SLEEP_SECS)
        util.number_bytes(self.count)
        pkt = packet.Packet(util.bytes_array())



class HypercubeApp(app_manager.RyuApp):

    def __init__(self, *args, **kwargs):
        super(HypercubeApp, self).__init__(*args, **kwargs)
        self.firstNode = None
        self.dps_count = 0
        self.dps = {} # dpid -> bit id

    @handler.set_ev_cls(dpset.EventDP, dpset.DPSET_EV_DISPATCHER)
    def handler_datapath(self, ev):
        if ev.enter:
            if self.firstNode is None:
                self.firstNode = ev.dp
                self.dps[ev.dp.id] = self.dps_count
                self.dps_count = self.dps_count + 1
            nodes_count = nodes_count + 1
            print(ev.dp.id)


    @handler.set_ev_cls(ofp_event.EventOFPPacketIn, handler.MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        data = msg.data
        dp = msg.datapath
        dpid = dp.dpid
        bit_id = 0
        if dp in self.dps:
            bit_id = self.dps[dp]
        else:
            self.dps[dp] = self.dps_count
            bit_id = self.dps_count
            self.dps_count = self.dps_count + 1

        if self.dps.keys()[0] == dpid:
            if miss_only_one_bit():
                pass
            else:
                return
                # finish algorithm
        if not bit_marked(data, bit_id):
            pass
            # mark bit and send and add to structure
        else:
            return

    def miss_only_one_bit(self, data, dps_len):
        completed = data[0] == 0x7F
        if dps_len > 8:
            for i in range(1,dps_len / 8):
                completed = completed and 0xFF
        return completed

    def bit_marked(self, data, pos):
        byte = (int) (pos / 8)
        offset = pos % 8
        return data[byte] & (1 << (7 - offset)) != 0

        #pkt = packet.Packet(array.array('B', data))
