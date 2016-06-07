#ifndef OPTIONS_HPP__
#define OPTIONS_HPP__
#include <string>
#include <vector>
#include <map>
#include <getopt.h>
using namespace std;

class Options {
public:
  static int help;

  static int get(string opts, string* arg);
  static int get(string opts) {
    return get(opts, 0);
  }
  

  static void init(int argc, char** argv);

  static string str();
  
  static bool inited;

  static vector<string> argv;
private:
  
  static string input;
  static map<string, string> opts_map;
  
};

#endif
