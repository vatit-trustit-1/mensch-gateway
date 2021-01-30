ssh -i "~/Downloads/maximKEY.pem" ubuntu@ec2-54-87-240-215.compute-1.amazonaws.com

# Let's setup an env to work quickly
sudo apt install golang-go
git clone https://github.com/muesli/gitomatic.git

# Get the code 
ssh-keygen
git clone git@github.com:vatit-trustit-1/mensch-gateway.git

# Setup poor man's CD flow
./gitomatic/gitomatic -push=false -author "Max" -email "max@trustit.com" -interval "20s" mensch-gateway
