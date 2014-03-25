CXX = g++
CXXFLAGS = -Wall -Wextra -std=c++11 -Ignuplotcpp
LIBS = -lGLU -lglut -lfreeimageplus
OBJECTS = $(patsubst %.cpp, %.o, $(wildcard *.cpp))

include **/Makefile.mk

%.o : %.cpp
	$(CXX) $(CXXFLAGS) -c $^ -o $@

main: $(OBJECTS)
	$(CXX) $(CXXFLAGS) $^ -o $@ $(LIBS)

all: main
