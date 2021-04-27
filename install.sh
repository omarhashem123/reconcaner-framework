#don't forget subfinder api and knock wordlist and massdns shuffledns wordlist and gitdorker github apis
#install go
apt-get update
wget https://golang.org/dl/go1.16.3.linux-amd64.tar.gz
rm -rf /usr/local/go && tar -C /usr/local -xzf go1.16.3.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
apt-get install build-essential
apt-get update
rm go1.16.3.linux-amd64.tar.gz
apt install python3-pip
apt install python-pip
python3 -m pip install -U pip
python3 -m pip install -U setuptools
apt-get update
#need to install go and nodejs v14
#nstall node
curl -fsSL https://deb.nodesource.com/setup_14.x | -E bash -
apt-get update && apt-get install yarn
apt-get install -y nodejs
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
apt-get install gconf-service libasound2 libatk1.0-0 libc6 \
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
pip install -r requirements.txt
python3 setup.py install
cd ..
knockpy --set apikey-virustotal=89d6092ffcd7b9638ee19601509c9ff7c4b05ce789fcb68124213c05f361377c
#shuffledns
GO111MODULE=on go get -v github.com/projectdiscovery/shuffledns/cmd/shuffledns
mv ~/go/bin/shuffledns /usr/bin/
#massdns
git clone https://github.com/blechschmidt/massdns.git
cd massdns
make
cd ..
#subfinder
GO111MODULE=on go get -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder
mv ~/go/bin/subfinder /usr/bin/
subfinder
rm ~/.config/subfinder/config.yaml
mv ../config.yaml ~/.config/subfinder/
#assetfinder
go get -u github.com/tomnomnom/assetfinder
mv ~/go/bin/assetfinder /usr/bin/
#httpx
GO111MODULE=on go get -v github.com/projectdiscovery/httpx/cmd/httpx
mv ~/go/bin/httpx /usr/bin/
#dirsearch
git clone https://github.com/maurosoria/dirsearch.git
cd dirsearch/
pip install -r requirements.txt
rm db/dicc.txt
mv ../../dicc.txt db/
cd ..
#gitdorker you need to add github token here
git clone https://github.com/obheda12/GitDorker.git
pip install -r GitDorker/requirements.txt
mv ../tokens GitDorker/
#naabu
apt install -y libpcap-dev
GO111MODULE=on go get -v github.com/projectdiscovery/naabu/v2/cmd/naabu
mv ~/go/bin/naabu /usr/bin/
#subover
go get github.com/Ice3man543/SubOver
mv ~/go/bin/SubOver /usr/bin/
#gau
GO111MODULE=on go get -u -v github.com/lc/gau
mv ~/go/bin/gau /usr/bin/
#brutespray
git clone https://github.com/x90skysn3k/brutespray.git
pip install -r brutespray/requirements.txt
#Gxss
go get -u github.com/KathanP19/Gxss
mv ~/go/bin/Gxss /usr/bin/
#gf
git clone https://github.com/tomnomnom/gf.git
go get -u github.com/tomnomnom/gf
mv ~/go/bin/gf /usr/bin/
mkdir ~/.gf
cp gf/examples/*.json ~/.gf/
git clone https://github.com/1ndianl33t/Gf-Patterns.git
cp Gf-Patterns/*.json ~/.gf
#dalfox
GO111MODULE=on go get -v github.com/hahwul/dalfox/v2
mv ~/go/bin/dalfox /usr/bin/
#smuggler
git clone https://github.com/defparam/smuggler.git
#s3brute
git clone https://github.com/ghostlulzhacks/s3brute.git
#subjs
GO111MODULE=on go get -u -v github.com/lc/subjs
mv ~/go/bin/subjs /usr/bin/
#qsreplace
go get -u github.com/tomnomnom/qsreplace
mv ~/go/bin/qsreplace /usr/bin/
#nmap
apt-get update
snap install nmap
#nuclei
GO111MODULE=on go get -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei
mv ~/go/bin/nuclei /usr/bin/
#nuclei templates
nuclei -update-templates
mv ../top-xss-params-omar.yaml ~/nuclei-templates/vulnerabilities/generic/
#jaeles
GO111MODULE=on go get github.com/jaeles-project/jaeles
mv ~/go/bin/jaeles /usr/bin/
#jaeles signtures and then need to edit signtures
jaeles config init
rm ~/.jaeles/base-signatures/fuzz/ -r -d
mv ../fuzz/ ~/.jaeles/base-signatures/
