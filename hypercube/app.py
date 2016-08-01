from ryu.base import app_manager
from ryu.lib.packet import packet, ethernet, ether_types, udp, ipv4, arp
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.topology import api as ryu_api
from ryu.ofproto import ofproto_v1_0


import array
# first packet send libs
import threading
import time

# personal libs
import util
from algorithm import DataStructure

import inspect

SLEEP_SECS=2.0
nodes_count = 0

"""
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



"""

class HypercubeApp(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(HypercubeApp, self).__init__(*args, **kwargs)
        self.firstNode = None
        self.dps_count = 0
        self.dps = {} # dpid -> bit id
        self.completed = False
        self.structure = DataStructure()
        self.mac_to_port = {}
        self.logger.info("Iniciando")
        self.doing = False

    def add_flow(self, datapath, in_port, dst, actions):
        ofproto = datapath.ofproto

        match = datapath.ofproto_parser.OFPMatch(
            in_port=in_port, dl_dst=haddr_to_bin(dst))

        mod = datapath.ofproto_parser.OFPFlowMod(
            datapath=datapath, match=match, cookie=0,
            command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
            priority=ofproto.OFP_DEFAULT_PRIORITY,
            flags=ofproto.OFPFF_SEND_FLOW_REM, actions=actions)
        datapath.send_msg(mod)

    def start_packet(self, datapath, msg):
        cube_length = len(ryu_api.get_all_switch(self))
        arr = util.arr_from_bit_len(cube_length)
        pkt = packet.Packet()
        pkt_begin = packet.Packet(data=msg.data)
        eth = pkt_begin.get_protocol(ethernet.ethernet)
        pkt.add_protocol(ethernet.ethernet(src=eth.src))
        pkt.add_protocol(bytearray(arr))
        pkt.serialize()
        print(array.array('B', pkt.data))
        actions = [datapath.ofproto_parser.OFPActionOutput(datapath.ofproto.OFPP_FLOOD)]
        self.send_msg(pkt.data, datapath, msg, actions)


    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        self.logger.info("packet arrived")
        msg = ev.msg
        data = msg.data
        datapath = msg.datapath
        pkt = packet.Packet(data=data)
        eth = pkt.get_protocol(ethernet.ethernet)
        ar = pkt.get_protocol(arp.arp)
        if eth.ethertype == ether_types.ETH_TYPE_ARP:
            self.logger.info("ARP")
            actions = [datapath.ofproto_parser.OFPActionOutput(msg.in_port)]
            pkt2 = packet.Packet()
            pkt2.add_protocol(ethernet.ethernet(dst=eth.src, src=eth.dst, ethertype=ether_types.ETH_TYPE_ARP))
            pkt2.add_protocol(arp.arp(opcode=2,src_mac=eth.dst, dst_mac=eth.src,src_ip=ar.dst_ip, dst_ip=ar.src_ip))
            pkt2.serialize()
            self.send_msg(pkt2.data, datapath, msg, actions)
            if not self.completed and not self.doing:
                self.start_packet(datapath, msg)
                self.doing = True
            #self.treat_arp_request(datapath, eth, msg)
        #dpid = dp.dpid
        #if completed:
        #    return
        """bit_id = 0
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
        """

    def treat_arp_request(self, datapath, eth, msg):
        data = msg.data
        dst = eth.dst
        src = eth.src
        ofproto = datapath.ofproto

        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        self.logger.info("packet in %s %s %s %s", dpid, src, dst, msg.in_port)

        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][src] = msg.in_port

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            self.add_flow(datapath, msg.in_port, dst, actions)

        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = datapath.ofproto_parser.OFPPacketOut(
            datapath=datapath, buffer_id=msg.buffer_id, in_port=msg.in_port,
            actions=actions, data=data)
        datapath.send_msg(out)

    def send_msg(self, data, dp, msg, actions):
        """out = dp.ofproto_parser.OFPPacketOut(datapath=dp, buffer_id=msg.buffer_id,
            in_port=msg.in_port, actions=actions, data=data)"""
        self.logger.info(msg.buffer_id)
        out = dp.ofproto_parser.OFPPacketOut(
            datapath=dp, buffer_id=dp.ofproto.OFP_NO_BUFFER, in_port=msg.in_port,
            actions=actions, data=data)
        dp.send_msg(out)
        print("sent")

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
