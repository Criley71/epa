#include <cstdio>
#include <fstream>
#include <iostream>
#include <string>
#include <typeinfo>
using namespace std;
/*
dtlb = data translation lookaside buffer
dc = data cache
pt = page table
l2 = second level data cache
*/
class Config {
 public:
  // data translation lookaside buffer
  int dtlb_set_count;  // max 256
  int dtlb_set_size;
  bool dtlb_enabled;
  int dtlb_associativity;

  int page_size;
  int pt_offset_bit;
  int pt_index_bits;

  int virtual_page_count;  // max 8192, must be power of 2
  int virtual_page_size;   // (bytes)
  int virtual_page_num;

  int physical_page_count;  // max 1024, must be power of 2
  int physical_page_size;
  int physical_page_bit_count;

  int dc_set_count;  // max 8192
  int dc_set_size;
  int dc_associativity;
  int dc_line_size;  // min 8 (bytes)
  bool dc_write_thru_no_allo;

  int l2_set_count;
  int l2_set_size;
  int l2_associativity;
  int l2_line_size;  // >= dc_line_size (bytes)
  bool l2_write_thru_no_allo;
  bool l2_enabled;

  bool virt_to_phys_trans;
};

Config init(); //function to read in config and set variables 

int main(int argc, char* argv[]) {
  Config config = init();
  
}

Config init() {
  Config config;
  ifstream fin("trace.config");

  string line;
  string substr;
  int colon_index;


  while (getline(fin, line)) {
    if (!line.empty()) {
      if (line.find("Data TLB configuration") == 0) {  // looks for dtlb header
        for (int i = 0; i < 2; i++) {
          getline(fin, line);  // gets next line in dltb head, should be "Numer of sets:"
          if (line.find("Number of sets") == 0) {
            colon_index = line.find(':')+2;
            substr = line.substr(colon_index, line.size());
            config.dtlb_set_count = stoi(substr);
            //cout << "dltb set count: " << config.dtlb_set_count << "\n";
            //cout << typeid(config.dtlb_set_count).name() << "\n";
            substr = "";
          }else if(line.find("Set size") == 0){
            colon_index = line.find(':')+2;
            substr = line.substr(colon_index, line.size());
            config.dtlb_set_size = stoi(substr);
            cout << "dltb set size: " << config.dtlb_set_size << "\n";
            cout << typeid(config.dtlb_set_size).name() << "\n";
          }
        }
      }
    }
  }
  return config;
}