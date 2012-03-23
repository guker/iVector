#include "configuration.h"
#include <sstream>
using namespace std;

Configuration::Configuration() {
	//Fill default values
	fileListInDir = "./other/";
	baseDir = "";
	outLoc = "./iVectors";
	threads = 8;
	limitFeatures = true;
	seed = 23;
	width = 200;
	height = 35937;
}

string Configuration::toString() {
	stringstream ss;
	ss << "File list directory: " << fileListInDir << "\n";
	ss << "Base directory for documents: " << baseDir << "\n";
	ss << "Save directory: " << outLoc << "\n";
	ss << "Threads available: " << threads << "\n";
	ss << "Limit features by square root: " << limitFeatures << "\n";
	ss << "Seed for T-matrix generation: " << seed << "\n";
	ss << "iVector size: " << width << "\n";
	ss << "height: " << height << "\n";
	return ss.str();
}