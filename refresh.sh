mv /home/ubuntu/Development/DelugeExecute/buffer/* /home/ubuntu/Development/DelugeExecute/buffer_temp

sleep 1

mv /home/ubuntu/Development/DelugeExecute/buffer_temp/* /home/ubuntu/Development/DelugeExecute/buffer

tail -f /home/ubuntu/Development/DelugeExecute/nohup.out
