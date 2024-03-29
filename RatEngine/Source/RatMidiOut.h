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

#include <string>
#include "JuceHeader.h"
#include "RatIO.h"

#pragma once

class RatMidiOut //: public RatIO
{
public:
	RatMidiOut(juce::String, uint8);
	RatMidiOut(juce::String, int);
	RatMidiOut();
	RatMidiOut(std::string, uint8);
	RatMidiOut(std::string, int);
	void setOutputDeviceKey(juce::String);
	juce::String getOutputDeviceKey();
	void setChannel(uint8);
	uint8 getChannel();
private:
//	std::shared_ptr<juce::MidiOutput> outputDevice;
	juce::String outputDeviceKey;
	uint8 channel;
};

