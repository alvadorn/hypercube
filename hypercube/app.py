from ryu.base import app_manager
from ryu.lib.packet import packet, ethernet, ether_types, ipv4, udp
from ryu.controller import dpset, handler, ofp_event
from ryu.topology import api as ryu_api
from ryu.lib.packet import in_proto as inet
from ryu.ofproto import ofproto_v1_0

# first packet send libs
import threading
import time

# personal libs
import util
from algorithm import DataStructure

import inspect

SLEEP_SECS=2.0
nodes_count = 0
fst_unique_id = 0
DST_PORT = 54321
SRC_PORT = 65500

def prepare_packet(data):
    pkt = packet.Packet()
    eth = ethernet.ethernet("ff:ff:ff:ff:ff:ff", "ff:ff:ff:ff:ff:ff")
    ip = ipv4.ipv4(src="255.255.255.255", dst="255.255.255.255", proto=inet.IPPROTO_UDP)
    udp1 = udp.udp(dst_port=DST_PORT, src_port=SRC_PORT)
    pkt.add_protocol(eth)
    pkt.add_protocol(ip)
    pkt.add_protocol(udp1)
    pkt.add_protocol(data)
    pkt.serialize()
    return pkt.data


class FirstPacketSender(threading.Thread):
    def __init__(self, dp, count):
        threading.Thread.__init__(self)
        self.dp = dp
        self.count = count
        self.structure = DataStructure()
        #print(dir(dp))
        #print(dp.ports)

    def send_msg(self, data):
        actions = [self.dp.ofproto_parser.OFPActionOutput(self.dp.ofproto.OFPP_FLOOD)]
        out = self.dp.ofproto_parser.OFPPacketOut(datapath=self.dp, in_port=self.dp.ofproto.OFPP_CONTROLLER,
            buffer_id=0xffffffff, actions=actions, data=data)
        self.dp.send_msg(out)

    def run(self):
        global nodes_count
        global fst_unique_id
        time.sleep(SLEEP_SECS)
        util.number_bytes(self.count)
        #pkt = packet.Packet((util.arr_from_bit_len(nodes_count))))

        data = prepare_packet(util.arr_from_bit_len(nodes_count, fst_unique_id))
        self.send_msg(data)
        print("packet sent")





class HypercubeApp(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]
    def __init__(self, *args, **kwargs):
        super(HypercubeApp, self).__init__(*args, **kwargs)
        self.first_node = None
        self.first_node_dp_id = None
        self.dps_count = 0
        self.dps = {} # dpid -> bit id
        self.completed = False
        self.structure = DataStructure()
        self.packets = 0

    @handler.set_ev_cls(dpset.EventDP, dpset.DPSET_EV_DISPATCHER)
    def handler_datapath(self, ev):
        global nodes_count
        global fst_unique_id
        if ev.enter:
            if self.first_node is None:
                self.first_node = ev.dp
                self.first_node_dp_id = ev.dp.id
                self.dps[ev.dp.id] = self.dps_count
                self.dps_count = self.dps_count + 1
                fst_unique_id = self.structure.add_node(self.dps[ev.dp.id], None)
                self.logger.info(ev.dp.id)
                FirstPacketSender(ev.dp, 0).start()
            nodes_count = nodes_count + 1
            #self.logger.info(dir(ev.dp))
            print(ev.dp.id)


    @handler.set_ev_cls(ofp_event.EventOFPPacketIn, handler.MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        self.packets = self.packets + 1
        global nodes_count
        self.logger.info("packet arrived")
        if self.completed:
            return
        msg = ev.msg
        data = msg.data
        dp = msg.datapath
        dpid = dp.id
        bit_id = 0

        pkt = packet.Packet(data)
        udp1 = pkt.get_protocol(udp.udp)
        self.logger.info("src pt: %s dst pst: %s dpid: %s", udp1.src_port, udp1.dst_port,dpid)


        udpdata = None

        for prot in pkt:
            if type(prot) is str:
                udpdata = prot

        print("udp data is: %s",udpdata)
        data = [ord(ob) for ob in udpdata]
        print("class:%s data: %s", data.__class__, data)
        #return

        if dpid in self.dps:
            print("enter 1")
            bit_id = self.dps[dpid]
        else:
            print("enter 2")
            self.dps[dpid] = self.dps_count
            bit_id = self.dps_count
            self.dps_count = self.dps_count + 1

        print("bit id: %s", bit_id)

        print("fst: %s atual: %s", self.first_node_dp_id, dpid)

        if self.first_node_dp_id == dpid:
            print("enter 3")
            self.logger.info(self.dps)

            if self.miss_only_one_bit(data, nodes_count):
                self.completed = True
                print("COMPLETED!!!!!! %s", self.packets)
                father = (data[-2] << 8) + data[-1]
                print(self.translate_result(self.structure.find_path(father)))
                for s in ryu_api.get_all_switch(self):
                    print(s.to_dict())
                return
            else:
                print("discarding")
                return
                # finish algorithm

        if not self.bit_marked(data, bit_id):
            print("enter 4")
            self.mark_bit(data, bit_id)
            parent_id = (data[-2] << 8) + data[-1]
            unique_id = self.structure.add_node(bit_id, parent_id)
            data[-2] = (unique_id >> 8) & 0xFF
            data[-1] = unique_id & 0xFF
            print("the data is: %s and unique_id: %s", data, unique_id)
            self.send_msg(prepare_packet(bytearray(data)), dp, msg)
            # mark bit and send and add to structure
        else:
            print("enter 5")
            return

    def translate_result(self, switch_list):
        values = self.dps.values()
        keys = self.dps.keys()
        path = []
        for s in switch_list[::-1]:
            i = values.index(s)
            path.append(keys[i])

        return path

    def send_msg(self, data, dp, msg):
        actions = [dp.ofproto_parser.OFPActionOutput(dp.ofproto.OFPP_FLOOD)]
        out = dp.ofproto_parser.OFPPacketOut(datapath=dp, buffer_id=0xffffffff,
            in_port=dp.ofproto.OFPP_CONTROLLER, actions=actions, data=data)
        dp.send_msg(out)

    def miss_only_one_bit(self, data, dps_len):
        completed = (data[0] == 0x7F)
        print("complet_d is: %s", completed)
        if dps_len > 8:
            for i in range(1, dps_len // 8):
                completed = completed and 0xFF
        print("final complet_d is: %s", completed)
        return completed

    def bit_marked(self, data, pos):
        byte = pos // 8
        offset = pos % 8
        return (data[byte] & (1 << (7 - offset))) != 0

    def mark_bit(self, data, pos):
        byte = pos // 8
        offset = pos % 8
        data[byte] = data[byte] | (1 << (7 - offset))
        #pkt = packet.Packet(array.array('B', data))
