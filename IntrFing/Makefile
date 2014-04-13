CXX = g++
CXXFLAGS = -Wall -Wextra -std=c++11 -Ignuplotcpp
LIBS = -lGLU -lglut -lfreeimageplus
HEADERS = $(wildcard *.hpp)
OBJECTS = $(patsubst %.cpp, %.o, $(wildcard *.cpp))

include **/Makefile.mk

%.o : %.cpp $(HEADERS)
	$(CXX) $(CXXFLAGS) -c -o $@ $<

img:
	make -C img

main: $(OBJECTS)
	$(CXX) $(CXXFLAGS) $^ -o $@ $(LIBS)

all: main
