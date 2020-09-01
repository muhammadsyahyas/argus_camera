%module cpp

%include <std_string.i>
%include <std_vector.i>
%include <stdint.i>

%typemap(in) uint8_t* {
  $1 = (uint8_t*) PyInt_AsLong($input);
}


%typemap(in,numinputs=0) int* n (int temp) "$1 = &temp;"

%typemap(argout) int* n {
  %append_output(PyLong_FromLong(*$1));
}

namespace std {
  %template (UInt32Vector) vector<uint32_t>;
  %template (UInt64Vector) vector<uint64_t>;
  %template (FloatVector) vector<float>;
  %template (FloatVectorVector) vector<vector<float> >;
}

%{
#include "../src/ArgusCamera.hpp"
%}

%include "../src/ArgusCamera.hpp"
