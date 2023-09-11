import argparse
import numpy as np
from csv import reader
import pickle
from flask import Flask, request, jsonify
import requests
import json
import datetime
from hashlib import sha256
from flask_cors import CORS


# from matplotlib import pyplot as plt
"""
*****************************BLOCKCHAIN CLASS********************************************************************************
"""


class Blockchain:
    difficulty = 2

    def __init__(self):
        self.chain = []
        self.unconfirmed_transactions = []
        self.genesis_block()

    def genesis_block(self):
        transactions = []
        genesis_block = Block(transactions, "0", str(datetime.datetime.now()))
        # genesis_block.generate_hash()
        self.chain.append(genesis_block)

    def add_block(self, transactions):
        previous_hash = (self.chain[len(self.chain) - 1]).hash
        new_block = Block(transactions, previous_hash, str(datetime.datetime.now()))
        # calculate nonce
        proof = self.proof_of_work(new_block)
        # new_block.hash = proof
        self.chain.append(new_block)
        return proof, new_block

    # when other node has already calculated nonce faster than other than no need for others to calculate proof
    def add_block2(self, transactions, proof):
        previous_hash = (self.chain[len(self.chain) - 1]).hash
        new_block = Block(transactions, previous_hash, str(datetime.datetime.now()))
        # calculate nonce
        # proof = self.proof_of_work(new_block)
        new_block.hash = proof
        self.chain.append(new_block)
        return proof, new_block

    def add_block3(self, block, proof):
        """
        A function that adds the block to the chain after verification.
        Verification includes:
        * Checking if the proof is valid.
        * The previous_hash referred in the block and the hash of a latest block
          in the chain match.
        """
        self.chain.append(block)

        return self.validate_chain()

    # to see whether the chain is broken or tampered with or not
    def validate_chain(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.hash != current.generate_hash():
                print(current.hash)
                print(current.generate_hash())
                print("Current hash does not equal generated hash")
                return False
            if current.previous_hash != previous.generate_hash():
                print("Previous block's hash got changed")
                return False
        return True

    # To calculate proof of work for a block
    def proof_of_work(self, block, difficulty=2):
        proof = block.generate_hash()
        while proof[:2] != "0" * difficulty:
            block.nonce += 1
            proof = block.generate_hash()
        block.nonce = 0
        # print(proof)
        return proof

    # for storing unconfirmed transactions
    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)
        print(self.mine())

    """
        This function serves as an interface to add the pending
        transactions to the blockchain by adding them to the block
        and figuring out proof of work.
    """

    def last_block(self):
        """
        A quick pythonic way to retrieve the most recent block in the chain. Note that
        the chain will always consist of at least one block (i.e., genesis block)
        """
        return self.chain[-1]

    def mine(self):

        if not self.unconfirmed_transactions:
            return "No transactions to mine"
        else:
            self.add_block(self.unconfirmed_transactions[0])
            # Making sure we have the longest chain before announcing to the network
            chain_length = len(self.chain)
            print(consensus())
            if chain_length == len(blockchain.chain):
                # announce the recently mined block to the network
                announce_new_block(blockchain.last_block())
                self.unconfirmed_transactions.pop(0)

            return "Block #{} is mined.".format(len(blockchain.chain) - 1)

    # (only for consensus() function) A helper method to check if the "given" blockchain is valid.
    def check_chain_validity(self, chain):
        for i in range(1, len(chain)):
            current = Block(
                chain[i]["transactions"],
                chain[i]["previous_hash"],
                chain[i]["time_stamp"],
            )
            previous = Block(
                chain[i - 1]["transactions"],
                chain[i - 1]["previous_hash"],
                chain[i - 1]["time_stamp"],
            )
            # print("current block in chech chain validity")

            if current.hash != current.generate_hash():

                print("Current hash does not equal generated hash")
                return False
            if current.previous_hash != previous.generate_hash():
                print("Previous block's hash got changed")
                return False
        return True

    def print_blocks(self):
        for i in range(len(self.chain)):
            current_block = self.chain[i]
            print("Block {} {}".format(i, current_block))
            current_block.print_contents()

    def get_transactions(self):
        temp = []
        for i in range(len(self.chain)):
            if not self.chain[i].__dict__[
                "transactions"
            ]:  # mean the transaction is empty
                continue
            else:
                temp.append(self.chain[i].__dict__["transactions"])
        return temp


"""
**************************BLOCK CLASS***************************************************************************************************
"""


class Block:
    def __init__(self, transactions, previous_hash, timestamp):
        self.time_stamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.generate_hash()

    def generate_hash(self):
        block_header = (
            str(self.time_stamp)
            + str(self.transactions)
            + str(self.previous_hash)
            + str(self.nonce)
        )

        block_hash = sha256(block_header.encode())
        return block_hash.hexdigest()

    def get_transaction(self):
        return self.transactions

    def print_contents(self):
        print("timestamp:", self.time_stamp)
        print("transactions:", self.transactions)
        print("current hash:", self.generate_hash())
        print("previous hash:", self.previous_hash)


"""
*******************************************************************************************************************************
"""

block_one_transactions = {
    "id": "1821881",
    "cgpa": "3.46",
    "sl_score": "bullshit",
    "mc_score": "4.0",
    "p_contest": "490",
    "cf_practice": "90",
    "kaggle_practice": "0",
    "sh_per_day": "3",
    "number_of_internship": "0",
    "job_role": "bullshit",
    "specialization": "sleeping",
    "completed_projects": "90",
}

app = Flask(__name__, template_folder="template")
# CORS(app)

blockchain = Blockchain()
# local_blockchain.print_blocks()
# Contains the host addresses of other participating members of the network
peers = []


def clean_data(value):
    if value == "Network engineer":
        value = "Network Engineer"
    if value == "Web developer":
        value = "Web Developer"

    if value[len(value) - 1] == " ":
        value = value[:-1]

    return value


# to add new transaction to the chain and then for mining
@app.route("/new_transaction", methods=["POST"])
def new_transaction():
    # required contents of the block
    id = request.get_json()["id"]
    cgpa = request.get_json()["cgpa"]
    sl_score = request.get_json()["sl_score"]
    mc_score = request.get_json()["mc_score"]
    p_contest = request.get_json()["p_contest"]
    cf_practice = request.get_json()["cf_practice"]
    kaggle_practice = request.get_json()["kaggle_practice"]
    sh_per_day = request.get_json()["sh_per_day"]
    number_of_internship = request.get_json()["number_of_internship"]
    job_role = clean_data(request.get_json()["job_role"])
    specialization = clean_data(request.get_json()["specialization"])
    completed_projects = request.get_json()["completed_projects"]

    if not (id):
        return "Invalid transaction data", 404

    blockchain.add_new_transaction(
        {
            "id": id,
            "cgpa": cgpa,
            "sl_score": sl_score,
            "mc_score": mc_score,
            "p_contest": p_contest,
            "cf_practice": cf_practice,
            "kaggle_practice": kaggle_practice,
            "sh_per_day": sh_per_day,
            "number_of_internship": number_of_internship,
            "job_role": job_role,
            "specialization": specialization,
            "completed_projects": completed_projects,
        }
    )

    return ("Success", 200)


# display all data in blockchain
@app.route("/chain", methods=["GET"])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"length": len(chain_data), "chain": chain_data})


@app.route("/get_student_data", methods=["POST"])
def get_student_data():
    student_id = request.get_json()["id"]
    chain_data = []
    n = 0
    for block in blockchain.chain:
        if n > 0:
            block_data = block.__dict__["transactions"]
            print(block_data)
            stud_id = block_data["id"]
            if student_id == stud_id:
                chain_data.append(block.__dict__)
        n += 1
    return json.dumps({"chain": chain_data})


# Endpoint to add new peers to the network
@app.route("/register_node", methods=["POST"])
def register_new_peers():
    # The host address to the peer node
    node_address = request.get_json()["node_address"]
    if not node_address:
        return "Invalid data", 400

    # Add the node to the peer list
    peers.append(node_address)
    print(peers)

    if len(peers) > 1:
        for i in range(len(peers) - 1):
            requests.post(
                peers[i] + "append_explicitly",
                data=json.dumps({"newP": peers[len(peers) - 1]}),
                headers={"Content-Type": "application/json"},
            )

    print("host:" + request.host)
    # Return the blockchain to the newly registered node so that it can sync
    return get_chain()


@app.route("/peers_list", methods=["GET"])
def peers_list():
    return json.dumps({"peers": peers})


def create_chain_from_dump(chain_dump):
    blockchain = Blockchain()
    blockchain.chain.pop()
    for idx, block_data in enumerate(chain_dump):
        print("idx" + str(idx) + "block_data" + str(block_data))
        block = Block(
            block_data["transactions"],
            block_data["previous_hash"],
            block_data["time_stamp"],
        )
        block.hash = block_data["hash"]
        if idx > 0:
            if not blockchain.add_block3(block, block_data["hash"]):
                raise Exception("The chain dump is tampered!!")
        else:
            # the block is a genesis block, no verification needed
            print("genesis block adding")
            blockchain.chain.append(block)
            print(block)
    return blockchain


@app.route("/append_explicitly", methods=["POST"])
def append_explicitly():
    res = request.get_json()["newP"]
    print(res)
    peers.append(res)
    print(peers)
    return "Done", 200


def create_chain_from_dump(chain_dump):
    blockchain = Blockchain()
    blockchain.chain.pop()
    for idx, block_data in enumerate(chain_dump):
        print("idx" + str(idx) + "block_data" + str(block_data))
        block = Block(
            block_data["transactions"],
            block_data["previous_hash"],
            block_data["time_stamp"],
        )
        block.hash = block_data["hash"]
        if idx > 0:
            if not blockchain.add_block3(block, block_data["hash"]):
                raise Exception("The chain dump is tampered!!")
        else:
            # the block is a genesis block, no verification needed
            print("genesis block adding")
            blockchain.chain.append(block)
            print(block)
    return blockchain


# endpoint to add a block mined by someone else to
# the node's chain. The node first verifies the block
# and then adds it to the chain.
@app.route("/add_block", methods=["POST"])
def verify_and_add_block():
    block_data = request.get_json()
    print("block_data")
    print(block_data)
    block = Block(
        block_data["transactions"],
        block_data["previous_hash"],
        block_data["time_stamp"],
    )
    proof = block_data["hash"]
    added = blockchain.add_block3(block, proof)

    if not added:
        return "The block was discarded by the node", 400
    return "Block added to the chain", 201


def announce_new_block(block):
    # block = Block(block['transactions'], block['previous_hash'], block['time_stamp'])
    for peer in peers:
        url = "{}add_block".format(peer)
        headers = {"Content-Type": "application/json"}

        print(block.__dict__)
        requests.post(url, data=json.dumps(block.__dict__), headers=headers)


# simple consensus algorithm. If a longer valid chain is found, our chain is replaced with it.
def consensus():
    global blockchain
    longest_chain = None
    current_len = len(blockchain.chain)
    print("peers")
    print(peers)
    for node in peers:
        response = requests.get("{}/chain".format(node))
        print(response.json())
        length = response.json()["length"]
        chain = response.json()["chain"]
        if length > current_len and blockchain.check_chain_validity(chain):
            # Longer valid chain found!
            current_len = length
            longest_chain = chain

    if longest_chain:
        blockchain = longest_chain
        return True

    return False


@app.route("/pending_tx")
def get_pending_tx():
    return json.dumps(blockchain.unconfirmed_transactions)


# manually add blocks
# blockchain.add_block(block_one_transactions)

# altering data to test integrity of the chain
# blockchain.chain[2].transactions = block_fake_transactions
print(blockchain.validate_chain())


@app.route("/get_data", methods=["POST"])
def retrieve():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"length": len(chain_data), "chain": chain_data})


@app.route("/get_all_data", methods=["GET"])
def get_all():
    return json.dumps(blockchain.get_transactions())


@app.route("/init", methods=["POST"])
def read_data():

    with open(request.get_json()["file_name"], "r") as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        # Iterate over each row in the csv using reader object
        for column in csv_reader:
            # row variable is a list that represents a row in csv
            data = {
                "id": column[1],
                "cgpa": column[2],
                "sl_score": column[3],
                "mc_score": column[4],
                "p_contest": column[5],
                "cf_practice": column[6],
                "kaggle_practice": column[7],
                "sh_per_day": column[8],
                "number_of_internship": column[9],
                "job_role": column[10],
                "specialization": column[11],
                "completed_projects": column[12],
            }
            # requests.post(json=data, url=request.get_json()["url"])
            requests.post(json=data, url="http://localhost:5000/new_transaction")
    return "success"


@app.route("/predict", methods=["POST"])
def predict():
    id = request.get_json()["id"]
    cgpa = request.get_json()["cgpa"]
    sl_score = request.get_json()["sl_score"]
    mc_score = request.get_json()["mc_score"]
    p_contest = request.get_json()["p_contest"]
    cf_practice = request.get_json()["cf_practice"]
    kaggle_practice = request.get_json()["kaggle_practice"]
    sh_per_day = request.get_json()["sh_per_day"]
    number_of_internship = request.get_json()["number_of_internship"]
    specialization = request.get_json()["specialization"]
    completed_projects = request.get_json()["completed_projects"]
    umodel = request.get_json()["model"]

    """ jobs_tostring = [
        "No job",
        "Data Scientist",
        "App Developer",
        "ML engineer",
        "Software Engineer",
        "Data Analyst",
        "Network Engineer",
        "Web Designer",
        "Data Engineer",
        "Web Developer",
        "Cyber Security Analyst",
        "UI Designer",
        "Backend Engineer",
        "DevOps Engineer",
        "QA Engineer",
        "MlOps Engineer",
        "FullStack Engineer",
        "Frontend Developer",
        "Security Engineer",
        "Data Architect",
    ]"""
    input_query = np.array(
        [
            [
                cgpa,
                sl_score,
                mc_score,
                p_contest,
                cf_practice,
                kaggle_practice,
                sh_per_day,
                number_of_internship,
                specialization,
                completed_projects,
            ]
        ]
    )

    model = pickle.load(open(f"../models/{umodel}.pkl", "rb"))
    result = model.predict(input_query)
    print(result)
    return jsonify({'Job Role':str(result)})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=str, default=5000)
    port = parser.parse_args()
    port = vars(port)["port"]
    app.run(debug=True, port=port)
