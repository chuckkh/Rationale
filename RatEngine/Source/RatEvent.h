#pragma once
#include "JuceHeader.h"

class RatEvent
{
public:
	virtual int play() = 0;
	uint32 getBeatTime();
private:
	uint32 beatTime;

};