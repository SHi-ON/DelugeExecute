mv /home/ubuntu/Development/DelugeExecute/buffer/* /home/ubuntu/Development/DelugeExecute/tmp

sleep 1

mv /home/ubuntu/Development/DelugeExecute/tmp/* /home/ubuntu/Development/DelugeExecute/buffer

tail -f /home/ubuntu/Development/DelugeExecute/nohup.out
