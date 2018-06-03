#include "newick.hpp"
#include "TaxonSet.hpp"
#include <algorithm>
#include <string>
#include <fstream>
#include <iostream>
#include <cctype>
#include <boost/program_options.hpp>

namespace po = boost::program_options;
using namespace std;

void impute(dm_type& dist_mat, dm_type& mask_mat, dm_type& impute_mat, unordered_set<string>& taxa) {
  for (int i = 0; i < taxa.size(); i++) {
    for (int j = 0; j < taxa.size(); j++) {
      if ((i != j) && mask_mat[i][j] == 0) {
	dist_mat[i][j] = impute_mat[i][j];
	mask_mat[i][j] = 1;
      }
    }
  }
}

int main(int argc, char** argv) {


  po::options_description desc("ASTRID v2.0");

  //desc.add_options()
  //  ("input", po::value<string>(), "gene trees in newick format");

  desc.add_options()
    ("matrix", po::value<string>(), "output for matrix");

  desc.add_options()
    ("taxlist", po::value<string>(), "output for taxon mapping file");  

  desc.add_options()
    ("n_missing", po::value<string>(), "number of missing elements");  
  
  desc.add_options()
    ("taxcutoff", po::value<int>()->default_value(0), "minimum taxa in a tree");  

  desc.add_options()
    ("impute-tree", po::value<string>()->default_value(""), "impute missing values from tree"); 
  desc.add_options()
    ("impute-mat", po::value<string>()->default_value(""), "impute missing values from matrix");  
  
  desc.add_options()
    ("nanplaceholder", po::value<string>()->default_value("--"), "representation for nan in matrix");  

  
  po::variables_map vm;
  po::store(po::parse_command_line(argc, argv, desc), vm);
  po::notify(vm);    

  vector<string> trees;

  //ifstream infile(vm["input"].as<string>());
  string line;
  while (getline(cin, line)) {
    trees.push_back(line);
  }

  unordered_set<string> taxa;
  for (string& tree : trees) {
    int ntaxa = newick_to_ts(tree, taxa);
    if (ntaxa < vm["taxcutoff"].as<int>()) {
      tree.clear();
    }
  }
  
  TaxonSet ts(taxa.size());
  
  for (string t : taxa) {
    ts.add(t);
  }
  ts.freeze();
  
  dm_type dist_mat(boost::extents[taxa.size()][taxa.size()]);
  dm_type mask_mat(boost::extents[taxa.size()][taxa.size()]);

  for (string& tree : trees)  {
    if (tree.size())
      newick_to_dm(tree, ts, dist_mat, mask_mat);
  }

  
  // if (vm["impute-mat"].as<str>().size()) {
  //   dm_type impute_dist_mat(boost::extents[taxa.size()][taxa.size()]);
  //   dm_type impute_mask_mat(boost::extents[taxa.size()][taxa.size()]);
  //   read_dist_mat(val["impute-mat"], impute_dist_mat, impute_mask_mat);
  //   impute(dist_mat, mask_mat, impute_dist_mat);
  // }
  if (vm["impute-tree"].as<string>().size()) {
    dm_type impute_dist_mat(boost::extents[taxa.size()][taxa.size()]);
    dm_type impute_mask_mat(boost::extents[taxa.size()][taxa.size()]);
    ifstream infile(vm["impute-tree"].as<string>());
    string line;
    getline(infile, line);
    newick_to_dm(line, ts, impute_dist_mat, impute_mask_mat);
    impute(dist_mat, mask_mat, impute_dist_mat, taxa);
  }

  ofstream matfile(vm["matrix"].as<string>());
  ofstream taxlist(vm["taxlist"].as<string>());
  ofstream missingfile(vm["n_missing"].as<string>());    

  int n_missing = 0;
  
  matfile << taxa.size() << endl;
  for (int i = 0; i < taxa.size(); i++) {
    dist_mat[i][i] = 0;
    mask_mat[i][i] = 1;    
    matfile << i << " ";
    for (int j = 0; j < taxa.size(); j++)  {
      dist_mat[i][j] /= mask_mat[i][j];
      if (mask_mat[i][j])
	matfile << dist_mat[i][j]  << " ";
      else {
	matfile << vm["nanplaceholder"].as<string>()  << " ";
	n_missing ++;
      }
    }
    matfile << endl;
    taxlist << ts[i] << endl;
  }

  missingfile << n_missing << endl;
  
}
