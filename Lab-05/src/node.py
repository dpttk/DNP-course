import grpc
import sys
import zlib
from concurrent import futures
import chord_pb2_grpc as pb2_grpc
import chord_pb2 as pb2

node_id = sys.argv[1]

CHORD = [2, 16, 24, 25, 26, 31]
CHANNELS = [
    "127.0.0.1:5000",
    "127.0.0.1:5001",
    "127.0.0.1:5002",
    "127.0.0.1:5003",
    "127.0.0.1:5004",
    "127.0.0.1:5005",
]

data = {}
finger_table = []

M = 5
id = -1
succ = -1
pred = -1


def populate_finger_table(id):
    def find_sucssessor(target):
        return

    def find_predecessor(target):
        return
    
    return


def get_stub(channel):
    channel = grpc.insecure_channel(channel)
    return pb2_grpc.ChordStub(channel)


def get_target_id(key):
    hash_value = zlib.adler32(key.encode())
    return hash_value % (2**M)



def save(key, text):
    return


def remove(key):
    return


def find(key):
    return


class NodeHandler(pb2_grpc.ChordServicer):
    def SaveData(self, request, context):
        reply = {}
        return pb2.SaveDataResponse(**reply)

    def RemoveData(self, request, context):
        reply = {}
        return pb2.RemoveDataResponse(**reply)

    def FindData(self, request, context):
        reply = {}
        return pb2.FindDataResponse(**reply)

    def GetFingerTable(self, request, context):
        reply = {}
        return pb2.GetFingerTableResponse(**reply)


if __name__ == "__main__":

    node_port = str(5000 + int(node_id))
    node = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_ChordServicer_to_server(NodeHandler(), node)
    node.add_insecure_port("127.0.0.1:" + node_port)
    node.start()

    try:
        node.wait_for_termination()
    except KeyboardInterrupt:
        print("Shutting down")
