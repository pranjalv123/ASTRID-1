#ifndef TAXONSET_HPP__
#define TAXONSET_HPP__

#include <string>
#include <vector>
#include <bitset>
#include <map>
#include <sstream>
#include <unordered_set>
#include <algorithm>

#include "BitVector.hpp"
using namespace std;

typedef int Taxon;
typedef BitVectorFixed clade_bitset;
class Clade;

class TaxonSet {
private:
  unordered_set<string> taxa_set;
  vector<string> taxa;
  map<string, Taxon> index;
  map<clade_bitset, Clade&> clade_map;
  bool frozen;
public:
  clade_bitset taxa_bs;

  TaxonSet(int size);
  TaxonSet(string str);

  int resize_clades(string str);
  
  void add_clade_taxa(string str, unordered_set<string>& taxa_set);

  void freeze();
  
  Taxon operator[](const string& str) {
    return add(str);
  }
  const string& operator[](const Taxon i) const {
    return taxa.at(i);
  }
  size_t size() const;
  Taxon add(const string& str);
  string str() const {
    stringstream ss;
    for (size_t i = 0; i < taxa.size(); i++) {
      ss << i << "\t" << taxa[i] << endl;
    }
    return ss.str();
  }
  vector<string>& sort_taxa() {
    sort(taxa.begin(), taxa.end());
    return taxa;
  }
};

#endif // TAXONSET_HPP__
