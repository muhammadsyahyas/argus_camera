%module cpp

%include <std_string.i>
%include <std_vector.i>
%include <stdint.i>

%typemap(in,numinputs=0) int *n (int temp) {
  $1 = &temp;
}

%typemap(argout) int *n {
  PyObject *o;
  o = PyLong_FromLong(*$1);
  $result = SWIG_Python_AppendOutput($result, o);
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
