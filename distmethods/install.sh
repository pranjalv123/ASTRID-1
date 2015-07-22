# cd to distmethods folder
cd "$( dirname "${BASH_SOURCE[0]}" )"

# Install FastME
wget http://www.ncbi.nlm.nih.gov/CBBresearch/Desper/FastME.tar -O FastME.tar
tar xvf FastME.tar
mv program FastME
cd FastME
make
cd ..
cp FastME/bin/fastme .

# Install PhyDStar
wget http://www.atgc-montpellier.fr/download/binaries/phyd/PhyDstar.tar.gz -O PhyDstar.tar.gz
tar xvf PhyDstar.tar.gz
cp PhyDstar/PhyDstar.jar .
