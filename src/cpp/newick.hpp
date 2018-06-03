#ifndef __NEWICK_HPP__
#define __NEWICK_HPP__

#include <boost/tokenizer.hpp>
#include <boost/multi_array.hpp>
#include <boost/algorithm/string.hpp>

#include <string>
#include <unordered_set>
#include <iostream>

#include "TaxonSet.hpp"

using namespace std;

typedef boost::multi_array<double, 2> dm_type;

int newick_to_ts(const string& s, unordered_set<string>& taxa) {
  typedef boost::tokenizer<boost::char_separator<char> > 
    tokenizer;
  boost::char_separator<char> sep(";\n", "(),:");
  tokenizer tokens(s, sep);

  int taxon_count = 0;

  string prevtok = "";
  
  for (auto tok : tokens) {
    boost::algorithm::trim(tok);


    if (tok == ":" || tok == "," || tok == "(" || tok == ")") {
    } else {
      if (prevtok == ")" or prevtok == ":") {	
	continue;
      }
      if(tok.find_first_not_of(' ') != string::npos) {
	taxa.insert(tok);
	taxon_count ++;
      }
    }
    prevtok = tok;
  }
  return taxon_count;
}

void newick_to_dm(const string& s, TaxonSet& ts, dm_type& dist_mat, dm_type& mask_mat ) {
  typedef boost::tokenizer<boost::char_separator<char> > 
    tokenizer;
  boost::char_separator<char> sep(";\n", "():,");
  
  tokenizer tokens(s, sep);
  
  vector<double> dists(ts.size(), 0);
  vector<double> ops(ts.size(), 0);

  vector<Taxon> seen;
  string prevtok = "";
  
  for (auto tok : tokens) {
    
    if (tok == "(") {
      for (Taxon s : seen) {
	ops[s] += 1;
	dists[s] += 1;
      }
    }
    else if (tok == ")") {
      for (Taxon s : seen) {
	if (ops[s]) {
	  dists[s] -= 1;
	  ops[s] -= 1;
	} else {
	  dists[s] += 1;
	}
      }
    }
    else if (tok == ":") {
    } else if (tok == ",") {
    } else {
      if (prevtok == ")" or prevtok == ":" or (tok == " " and prevtok == ",")) {
	continue;
      }
      boost::algorithm::trim(tok);
      Taxon id = ts[tok];
      for (Taxon other : seen) {
	dist_mat[other][id] += dists[other] + 2;
	dist_mat[id][other] += dists[other] + 2;
	mask_mat[other][id] += 1;
	mask_mat[id][other] += 1;	
      }
      seen.push_back(id);
    }
    prevtok = tok;
  }
}

#endif
