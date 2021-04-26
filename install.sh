#don't forget subfinder api and knock wordlist and massdns shuffledns wordlist and gitdorker github apis
#install go
sudo apt-get update
wget https://golang.org/dl/go1.16.3.linux-amd64.tar.gz
sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.16.3.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
apt-get install build-essential
sudo apt-get update
sudo rm go1.16.3.linux-amd64.tar.gz
sudo apt install python3-pip
sudo apt install python-pip
sudo python3 -m pip install -U pip
sudo python3 -m pip install -U setuptools
sudo apt-get update
#need to install go and nodejs v14
#nstall node
curl -fsSL https://deb.nodesource.com/setup_14.x | sudo -E bash -
sudo apt-get update && sudo apt-get install yarn
sudo apt-get install -y nodejs
mkdir webtool
#clickjacking
mkdir webtool/clickjack
mv clickjack.py webtool/clickjack/
cd webtool
#install wappalyzer
mkdir technology
cd technology
git clone https://github.com/AliasIO/wappalyzer.git
cd wappalyzer
yarn install
yarn run link
sudo apt-get install gconf-service libasound2 libatk1.0-0 libc6 \
    libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 \
    libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 \
    libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 \
    libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 \
    libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates \
    fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget

cd ../../
#knockpy
git clone https://github.com/guelfoweb/knock.git
cd knock/
sudo pip install -r requirements.txt
sudo python3 setup.py install
cd ..
sudo knockpy --set apikey-virustotal=89d6092ffcd7b9638ee19601509c9ff7c4b05ce789fcb68124213c05f361377c
#shuffledns
GO111MODULE=on go get -v github.com/projectdiscovery/shuffledns/cmd/shuffledns
sudo mv ~/go/bin/shuffledns /usr/bin/
#massdns
git clone https://github.com/blechschmidt/massdns.git
cd massdns
make
cd ..
#subfinder
GO111MODULE=on go get -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder
sudo mv ~/go/bin/subfinder /usr/bin/
subfinder
sudo rm ~/.config/subfinder/config.yaml
sudo mv ../config.yaml ~/.config/subfinder/
#assetfinder
go get -u github.com/tomnomnom/assetfinder
sudo mv ~/go/bin/assetfinder /usr/bin/
#httpx
GO111MODULE=on go get -v github.com/projectdiscovery/httpx/cmd/httpx
sudo mv ~/go/bin/httpx /usr/bin/
#dirsearch
git clone https://github.com/maurosoria/dirsearch.git
cd dirsearch/
pip install -r requirements.txt
cd ..
#gitdorker you need to add github token here
git clone https://github.com/obheda12/GitDorker.git
pip install -r GitDorker/requirements.txt
mv ../tokens GitDorker/
#naabu
sudo apt install -y libpcap-dev
GO111MODULE=on go get -v github.com/projectdiscovery/naabu/v2/cmd/naabu
sudo mv ~/go/bin/naabu /usr/bin/
#subover
go get github.com/Ice3man543/SubOver
sudo mv ~/go/bin/SubOver /usr/bin/
#gau
GO111MODULE=on go get -u -v github.com/lc/gau
sudo mv ~/go/bin/gau /usr/bin/
#brutespray
git clone https://github.com/x90skysn3k/brutespray.git
pip install -r brutespray/requirements.txt
#Gxss
go get -u github.com/KathanP19/Gxss
sudo mv ~/go/bin/Gxss /usr/bin/
#gf
go get -u github.com/tomnomnom/gf
sudo mv ~/go/bin/gf /usr/bin/
cp -r gf/examples ~/.gf
git clone https://github.com/1ndianl33t/Gf-Patterns.git
cp -r Gf-Patterns/*.json ~/.gf
#dalfox
GO111MODULE=on go get -v github.com/hahwul/dalfox/v2
sudo mv ~/go/bin/dalfox /usr/bin/
#smuggler
git clone https://github.com/defparam/smuggler.git
#s3brute
git clone https://github.com/ghostlulzhacks/s3brute.git
#subjs
GO111MODULE=on go get -u -v github.com/lc/subjs
sudo mv ~/go/bin/subjs /usr/bin/
#qsreplace
go get -u github.com/tomnomnom/qsreplace
sudo mv ~/go/bin/qsreplace /usr/bin/
#nmap
sudo apt-get update
sudo snap install nmap
#nuclei
GO111MODULE=on go get -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei
sudo mv ~/go/bin/nuclei /usr/bin/
#nuclei templates
nuclei -update-templates
mv ../top-xss-params-omar.yaml ~/nuclei-templates/vulnerabilities/generic/
#jaeles
GO111MODULE=on go get github.com/jaeles-project/jaeles
sudo mv ~/go/bin/jaeles /usr/bin/
#jaeles signtures and then need to edit signtures
jaeles config init
rm ~/.jaeles/base-signatures/fuzz/ -r -d
cp fuzz/ ~/.jaeles/base-signatures/ -r
