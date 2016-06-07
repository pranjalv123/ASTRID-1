#include "Logger.hpp"
#include "Options.hpp"
#include <iostream>
#include <ostream>
#include <iomanip>
#include <ctime>
#include <cstring>

using namespace std;

int Logger::ilevel;
set<string> Logger::enabled_tags;
set<string> Logger::enabled_files;
set<string> Logger::disabled_tags;
set<string> Logger::disabled_files;
NullStream Logger::nstream;

Logger::Logger() {
  string level;
  if (Options::inited) {
    Options::get("v verbose", &level);
    getIlevel(level);
    setLevel(*this);
  }
  else {
    ilevel = -1;
    setLevel(*this);
  }
}

Logger& Logger::get() {
  static Logger* logger = new Logger();
  if (logger->ilevel == -1) {
    delete logger;
    logger = new Logger();
  }
  
  return *logger;

}

ostream& Logger::log(string tag, string fname, int lineno) {
  Logger& logger = get();
  time_t t = time(nullptr);
  tm time = *localtime(&t);

  
  if (logger.enabled_tags.count(tag)) {
#if defined(__GNUC__) and __GNUC__ >= 5
    cerr << "[" << std::put_time(&time, "%d-%m-%Y %H:%M:%S") << "] " << tag << " {" << rindex(fname.c_str(), '/') + 1 << ":" << lineno << "} " ;
#else
    cerr << '[' << ctime(t) << ']' << tag  << " {" << rindex(fname.c_str(), '/') + 1 << ":" << lineno << "} " ;
#endif
    return cerr;
  }
  return nstream;
}

void Logger::enable(string tag) {
  Logger& logger = get();
  logger.enabled_tags.insert(tag);
}
void Logger::enable(string tag, Logger& logger) {
  logger.enabled_tags.insert(tag);
}

bool Logger::isEnabled(string tag) {
  Logger& logger = get();
  return logger.enabled_tags.count(tag);
}

void Logger::disable(string tag) {
  Logger& logger = get();
  logger.enabled_tags.erase(tag);
}

void Logger::setLevel(Logger& logger) {
  for (auto& tag : logger.enabled_tags) {
    logger.enabled_tags.erase(tag);
  }
  switch (ilevel) {
  case -1:
  case 3:
    enable("DEBUG", logger);
  case 2:
    enable("INFO", logger);
  case 1:
    enable("PROGRESS", logger);
  }
  enable("WARNING", logger);
  enable("ERROR", logger);
}

void Logger::getIlevel(string& level) {
  ilevel = 0;
  if (level == "")
    return;
  ilevel++;
  if (level == "progress")
    return;
  ilevel++;
  if (level == "info") 
    return;
  ilevel++;
  if (level == "debug") 
    return;
  return;
  
}
