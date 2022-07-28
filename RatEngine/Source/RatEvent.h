//    Copyright 2008, 2009, 2010, 2022 Charles S. Hubbard, Jr.
//
//    This file is part of Rationale.
//
//    Rationale is free software: you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by
//    the Free Software Foundation, either version 3 of the License, or
//    (at your option) any later version.
//
//    Rationale is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU General Public License for more details.
//
//    You should have received a copy of the GNU General Public License
//    along with Rationale.  If not, see <http://www.gnu.org/licenses/>.
					  
#pragma once
#include "JuceHeader.h"
#include <vector>
#include <map>
#include <string>

class RatEvent
{
public:
	virtual int trigger() = 0;
	std::vector<uint16> getBeatTime();
	void setBeatTime(std::vector<uint16>);
	void setBeatTime(uint16, uint16);
private:
	//std::vector<uint32> beatTime;

	/*
	"beat" is a 16-bit number simply representing the number of 
	beats.... 
	*/
	uint16 bar;
	uint8 beat;
	uint16 ticks;
//	uint16 durationBeats;
//	uint16 durationTicks;
//	uint16 id;
//	std::map<std::string, uint16> arbitrary;
	
//	uint32 beatSubNum;
//	uint32 beatSubDen;

};
