from ryu.base import app_manager
from ryu.lib.packet import packet, ethernet
from ryu.controller import dpset, handler, ofp_event
from ryu.topology import api as ryu_api

# first packet send libs
import threading
import time

# personal libs
import util
from algorithm import DataStructure

import inspect

SLEEP_SECS=2.0
nodes_count = 0

class FirstPacketSender(threading.Thread):
    def __init__(self, dp, count):
        threading.Thread.__init__(self)
        self.dp = dp
        self.count = count
        self.structure = DataStructure()
        print(dir(dp))

    def send_msg(self, data):
        actions = [self.dp.ofproto_parser.OFPActionOutput(self.dp.ofproto.OFPP_FLOOD)]
        out = self.dp.ofproto_parser.OFPPacketOut(datapath=self.dp, in_port=self.dp.ofproto.OFPP_CONTROLLER,
            buffer_id=0xffffffff, actions=actions, data=data)
        self.dp.send_msg(out)

    def run(self):
        global nodes_count
        time.sleep(SLEEP_SECS)
        util.number_bytes(self.count)
        pkt = packet.Packet(util.arr_from_bit_len(nodes_count))
        #print(pkt.data())
        self.send_msg(util.arr_from_bit_len(nodes_count))
        print("packet sent")





class HypercubeApp(app_manager.RyuApp):

    def __init__(self, *args, **kwargs):
        super(HypercubeApp, self).__init__(*args, **kwargs)
        self.firstNode = None
        self.dps_count = 0
        self.dps = {} # dpid -> bit id
        self.completed = False
        self.structure = DataStructure()

    @handler.set_ev_cls(dpset.EventDP, dpset.DPSET_EV_DISPATCHER)
    def handler_datapath(self, ev):
        global nodes_count
        if ev.enter:
            if self.firstNode is None:
                self.firstNode = ev.dp
                self.dps[ev.dp.id] = self.dps_count
                self.dps_count = self.dps_count + 1
                self.structure.add_node(self.dps[ev.dp.id], None)
                FirstPacketSender(ev.dp, 0).start()
            nodes_count = nodes_count + 1
            #self.logger.info(dir(ev.dp))
            print(ev.dp.id)


    @handler.set_ev_cls(ofp_event.EventOFPPacketIn, handler.MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        self.logger.info("packet arrived")
        if completed:
            return
        msg = ev.msg
        data = msg.data
        dp = msg.datapath
        dpid = dp.dpid
        bit_id = 0
        if dpid in self.dps:
            bit_id = self.dps[dp]
        else:
            self.dps[dpid] = self.dps_count
            bit_id = self.dps_count
            self.dps_count = self.dps_count + 1

        if self.dps.keys()[0] == dpid:
            if miss_only_one_bit():
                completed = true
                print(self.structure.find_path())
            else:
                return
                # finish algorithm
        if not bit_marked(data, bit_id):
            mark_bit(data, bit_id)
            parent_id = (data[-2] << 8) + data[-1]
            self.structure.add_node(bit_id, parent_id)
            data[-2] = (bit_id >> 8) & 0xFF
            data[-1] = bit_id & 0xFF
            send_msg(data, dp, msg)
            # mark bit and send and add to structure
        else:
            return

    def send_msg(self, data, dp, msg):
        actions = [dp.ofproto_parser.OFPActionOutput(dp.of_proto.OFPP_FLOOD)]
        out = dp.ofproto_parser.OFPPacketOut(datapath=dp, buffer_id=msg.buffer_id,
            in_port=msg.in_port, actions=actions, data=data)
        dp.send_msg(out)


    def miss_only_one_bit(self, data, dps_len):
        completed = data[0] == 0x7F
        if dps_len > 8:
            for i in range(1, dps_len // 8):
                completed = completed and 0xFF
        return completed

    def bit_marked(self, data, pos):
        byte = pos // 8
        offset = pos % 8
        return data[byte] & (1 << (7 - offset)) != 0

    def mark_bit(self, data, pos):
        byte = pos // 8
        offset = pos % 8
        data[byte] = data[byte] | (1 << (7 - offset))
        #pkt = packet.Packet(array.array('B', data))
