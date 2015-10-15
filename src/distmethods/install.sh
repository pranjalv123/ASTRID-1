# cd to distmethods folder
cd "$( dirname "${BASH_SOURCE[0]}" )"

echo "Installing FastME..."
# Install FastME
wget http://www.ncbi.nlm.nih.gov/CBBresearch/Desper/FastME.tar -O FastME.tar
tar xvf FastME.tar
mv program FastME
cd FastME
make
cd ..
cp FastME/bin/fastme .
echo "Installed FastME!"


echo "Installing FastME 2..."
# Install FastME
wget http://www.atgc-montpellier.fr/download/sources/fastme/fastme-2.1.4.tar.gz -O FastME2.tar.gz
tar xvf FastME2.tar.gz
cd fastme-2.1.4
./configure
make
cd ..
cp fastme-2.1.4/src/fastme fastme2
echo "Installed FastME 2!"


echo "Installing PhyD*..."
# Install PhyDStar
wget http://www.atgc-montpellier.fr/download/binaries/phyd/PhyDstar.tar.gz -O PhyDstar.tar.gz
tar xvf PhyDstar.tar.gz
cp PhyDstar/PhyDstar.jar .
echo "Installed PhyD*!"

