import argparse
from concurrent import futures

import grpc

import raft_pb2 as pb2
import raft_pb2_grpc as pb2_grpc

NODE_ID = None
SERVERS_INFO = {}
SUSPEND = None

class Handler(pb2_grpc.RaftNodeServicer):
    def __init__(self):
        super().__init__()

    def AppendEntries(self, request, context):
        if SUSPEND:
            context.set_details("Server suspended")
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            return pb2.AppendEntriesResponse()

        return pb2.AppendEntriesResponse(**{"term": None, "heartbeat_result": None})


    def RequestVote(self, request, context):
        if SUSPEND:
            context.set_details("Server suspended")
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            return pb2.RequestVoteResponse()
        print(f'RPC[RequestVote] Invoked')
        print(f'\tArgs:')
        print(f'\t\tcandidate_id: {request.candidate_id}')
        print(f'\t\tcandidate_term: {request.candidate_term}')

        return pb2.RequestVoteResponse(**{"term": None, "vote_result": None})

    def GetLeader(self, request, context):
        if SUSPEND:
            context.set_details("Server suspended")
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            return pb2.GetLeaderResponse()
        print(f'RPC[GetLeader] Invoked')
        return pb2.GetLeaderResponse(**{"leader_id": None})
        
    def AddValue(self, request, context):
        if SUSPEND:
            context.set_details("Server suspended")
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            return pb2.AddValueResponse()
        print(f'RPC[AddValue] Invoked')
        print(f'\tArgs:')
        print(f'\t\tvalue_to_add: {request.value_to_add}')
        return pb2.AddValueResponse(**{})
    
    def GetValue(self, request, context):
        if SUSPEND:
            context.set_details("Server suspended")
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            return pb2.GetValueResponse()
        print(f'RPC[GetValue] Invoked')
        return pb2.GetValueResponse(**{"value": None})

    def Suspend(self, request, context):
        print(f'RPC[Suspend] Invoked')
        return pb2.SuspendResponse(**{})
    
    def Resume(self, request, context):
        print(f'RPC[Resume] Invoked')
        return pb2.ResumeResponse(**{})


# ----------------------------- Do not change ----------------------------- 
def serve():
    print(f'NODE {NODE_ID} | {SERVERS_INFO[NODE_ID]}')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_RaftNodeServicer_to_server(Handler(), server)
    server.add_insecure_port(SERVERS_INFO[NODE_ID])
    try:
        server.start()
        while True:
            server.wait_for_termination()
    except grpc.RpcError as e:
        print(f"Unexpected Error: {e}")
    except KeyboardInterrupt:
        server.stop(grace=10)
        print("Shutting Down...")


def init(node_id):
    global NODE_ID
    NODE_ID = node_id

    with open("config.conf") as f:
        global SERVERS_INFO
        lines = f.readlines()
        for line in lines:
            parts = line.split()
            id, address = parts[0], parts[1]
            SERVERS_INFO[int(id)] = str(address)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("node_id", type=int)
    args = parser.parse_args()

    init(args.node_id)

    serve()
# ----------------------------- Do not change -----------------------------
