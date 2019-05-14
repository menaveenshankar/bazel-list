echo "Installing tqdm (python package)"
sudo -H pip3 install tqdm

chmod +x bzlst
echo "export PATH=$(pwd):\$PATH" >> ~/.bashrc
echo -e '\e[92msetup done!\e[39m';
