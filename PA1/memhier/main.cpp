#include <cstdio>
#include <fstream>
#include <iostream>

using namespace std;
/*
dtlb = data translation lookaside buffer
dc = data cache
pt = page table
l2 = second level data cache
*/
class Config {
 public:
  int dtlb_set_count;
  int dc_set_count;

  int dtlb_associativity;
  int dc_associativity;
  int l2_associativity;

  int virtual_page_count;
  int virtual_page_size;
  int virtual_page_bit_count;

  int physical_page_count;
  int physical_page_size;
  int physical_page_bit_count;
};