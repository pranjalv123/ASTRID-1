#ifndef __LOGGER_HPP__
#define __LOGGER_HPP__

#include <set>
#include <iostream>

using namespace std;

class NullStream : public ostream {
public:
    void setFile() { /* no-op */ }
    template<typename TPrintable>
    NullStream& operator<<(TPrintable const&)
  { return this;/* no-op */ }
};

class Logger {
public:
  static Logger& get();
  static ostream& log(string tag, string fname, int lineno);
  static void enable(string tag);
  static bool isEnabled(string tag);
  static void enable(string tag, Logger& logger);
  
  static void disable(string tag);
  static void setLevel(Logger& logger);
private:
  Logger();
  static set<string> enabled_tags;
  static set<string> enabled_files;
  static set<string> disabled_tags;
  static set<string> disabled_files;
  static int ilevel;
  static void getIlevel(string& level);
  static NullStream nstream;
  
};

#define LOG(tag) if (Logger::isEnabled(tag)) (Logger::log((tag), (__BASE_FILE__), (__LINE__)))
#define DEBUG LOG("DEBUG")
#define ERR LOG("ERROR")
#define WARN LOG("WARNING")
#define INFO LOG("INFO")
#define PROGRESS LOG("PROGRESS")


#endif
