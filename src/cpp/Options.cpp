#include "Options.hpp"
#include "Logger.hpp"
#include <cassert>
#include <iostream>
#include <iterator>
#include <sstream>

bool Options::inited = false;

vector<string> Options::argv;
map<string, string> Options::opts_map;
string Options::input;

enum option_type {SHORT, LONG, ARG, END, EMPTY};

option_type get_option_type(string& arg) {
  if (arg.size() == 0) return EMPTY;
  if (arg[0] != '-') return ARG;
  if (arg.size() == 1) {
    cerr << "INVALID ARGUMENT " << arg << endl;
    exit(1);
  }
  if (arg[1] == '-') {
    if (arg.size() == 2) return END;
    arg = string(arg, 2); //remove starting --
    return LONG;
  }
  if (arg.size() > 2) {
    cerr << "INVALID ARGUMENT " << arg << endl;
    exit(1);
  }
  arg = string(arg, 1);
  return SHORT;
}

string Options::str() {
  return input;
}

void Options::init(int argc_, char** argv_) {

  for (int i = 1; i < argc_; i++) {
    //    cerr << i << " " << argv_[i] << endl;
    argv.push_back(string(argv_[i]));
    input += string(argv_[i]) + " ";
  }

  argv.push_back("--");
  
  string last_option = "";
  
  for (string arg : argv) {
    option_type opttype = get_option_type(arg);
    //    DEBUG << arg << " " <<  opttype << endl;
    switch(opttype) {
    case SHORT:
    case LONG:
      if (last_option != "") {
	opts_map[last_option] = "";
      }
      last_option = arg;
      break;
    case ARG:
      if (last_option == ""){
	cerr << "ARGUMENT WITHOUT OPTION: " << arg << endl;
	exit(1);
      }
      opts_map[last_option] = arg;
      last_option = "";
      break;
    case END:
      if (last_option != "") {
	opts_map[last_option] = "";
      }
    }

  }

  // DEBUG << "OPTIONS MAP:\n";
  // for (auto& kv : opts_map) {
  //   DEBUG << kv.first << " = " << kv.second << endl;
  // }
  
  inited = true;
}


int Options::get(string opts, string* arg) {
  assert(inited);

  stringstream ss(opts);
  istream_iterator<std::string> begin(ss);
  istream_iterator<std::string> end;
  vector<string> vopts(begin, end);
  
  for (auto& opt : vopts) {
    if (opts_map.count(opt)) {
      if (arg)
	*arg = opts_map[opt];

      return 1;
    }

  }
  return 0;
  
  // opterr = 0;
  
  // struct option opts[] = {{ longopt.c_str(), optional_argument, 0, 0},
  // 			  { 0, 0, 0, 0}
  // };
  // int c;
  // int option_index;
  // string optstring = "-:";
  // if (shortopt) {
  //   if (arg)
  //     optstring = ":" + string(&shortopt, 1) + ":";
  //   else
  //     optstring = ":" + string(&shortopt, 1) ;
  // }
  // while ((c = getopt_long(argc, argv, optstring.c_str(), &(opts[0]), &option_index)) != -1) {
  //   if (c == shortopt || c == 0 ) {
  //     if (arg && (size_t)optarg)
  // 	*arg = string(optarg);
  //     optind = 1;
  //     return 1;
  //     cout << shortopt << " " << longopt << " " << arg << endl;
  //   }
  // }
  // optind = 1;
  // return 0;  
}

