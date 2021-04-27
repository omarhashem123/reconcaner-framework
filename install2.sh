sudo apt-get update
sudo snap install go --classic
sudo apt install python3-pip
sudo apt install python-pip
python3 -m pip install -U pip
python3 -m pip install -U setuptools
sudo apt-get update
curl -sL https://deb.nodesource.com/setup_14.x | sudo bash -
sudo apt -y install nodejs
curl -sL https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
sudo apt-get update && sudo apt-get install yarn
mkdir webtool
mkdir webtool/clickjack
mv clickjack.py webtool/clickjack/
cd webtool/
mkdir technology
cd technology
git clone https://github.com/AliasIO/wappalyzer.git
cd wappalyzer
sudo apt remove cmdtest
sudo apt remove yarn
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
sudo apt-get update
sudo apt-get install yarn -y
yarn install
yarn run link
sudo apt install -y gconf-service libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget
cd ../../
git clone https://github.com/guelfoweb/knock.git
cd knock/
pip install -r requirements.txt
sudo python3 setup.py install
cd ..
sudo knockpy --set apikey-virustotal=89d6092ffcd7b9638ee19601509c9ff7c4b05ce789fcb68124213c05f361377c
GO111MODULE=on go get -v github.com/projectdiscovery/shuffledns/cmd/shuffledns
sudo mv ~/go/bin/shuffledns /usr/bin/
git clone https://github.com/blechschmidt/massdns.git
cd massdns/
make
cd ..
GO111MODULE=on go get -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder
sudo mv ~/go/bin/subfinder /usr/bin/
subfinder --help
mv ../config.yaml ~/.config/subfinder/
go get -u github.com/tomnomnom/assetfinder
sudo mv ~/go/bin/assetfinder /usr/bin/
GO111MODULE=on go get -v github.com/projectdiscovery/httpx/cmd/httpx
sudo mv ~/go/bin/httpx /usr/bin/
git clone https://github.com/maurosoria/dirsearch.git
cd dirsearch/
pip install -r requirements.txt
rm db/dicc.txt
mv ../../dicc.txt db/
cd ..
git clone https://github.com/obheda12/GitDorker.git
pip install -r GitDorker/requirements.txt
mv ../tokens GitDorker/
sudo apt install -y libpcap-dev
GO111MODULE=on go get -v github.com/projectdiscovery/naabu/v2/cmd/naabu
sudo mv ~/go/bin/naabu /usr/bin/
go get github.com/Ice3man543/SubOver
sudo mv ~/go/bin/SubOver /usr/bin/
GO111MODULE=on go get -u -v github.com/lc/gau
sudo mv ~/go/bin/gau /usr/bin/
git clone https://github.com/x90skysn3k/brutespray.git
pip install -r brutespray/requirements.txt
go get -u github.com/KathanP19/Gxss
sudo mv ~/go/bin/Gxss /usr/bin/
git clone https://github.com/tomnomnom/gf.git
go get -u github.com/tomnomnom/gf
sudo mv ~/go/bin/gf /usr/bin/
mkdir ~/.gf
cp gf/examples/*.json ~/.gf/
git clone https://github.com/1ndianl33t/Gf-Patterns.git
cp Gf-Patterns/*.json ~/.gf
GO111MODULE=on go get -v github.com/hahwul/dalfox/v2
sudo mv ~/go/bin/dalfox /usr/bin/
git clone https://github.com/defparam/smuggler.git
git clone https://github.com/ghostlulzhacks/s3brute.git
GO111MODULE=on go get -u -v github.com/lc/subjs
sudo mv ~/go/bin/subjs /usr/bin/
sudo mv ~/go/bin/qsreplace /usr/bin/
sudo apt-get update
snap install nmap
GO111MODULE=on go get -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei
sudo mv ~/go/bin/nuclei /usr/bin/
nuclei -update-templates
mv ../top-xss-params-omar.yaml ~/nuclei-templates/vulnerabilities/generic/
GO111MODULE=on go get github.com/jaeles-project/jaeles
sudo mv ~/go/bin/jaeles /usr/bin/
jaeles config init
rm ~/.jaeles/base-signatures/fuzz/ -r -d
mv ../fuzz/ ~/.jaeles/base-signatures/
