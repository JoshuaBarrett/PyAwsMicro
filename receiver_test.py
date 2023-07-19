from ir_remote import AirConRemoteSender

receiver = AirConRemoteReceiver(1, True)
while True:
    cmd = receiver.readCommandSignal()    
    print(cmd)
    