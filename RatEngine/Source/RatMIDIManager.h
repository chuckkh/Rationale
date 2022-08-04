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

#include "RatIOManager.h"
#include "RatMIDIMessage.h"
#include "JuceHeader.h"
#include <queue>
#include <map>
#include <memory>
class RatMIDIManager : public RatIOManager
{
public:
	RatMIDIManager();
	void addInput(juce::String);
	void addOutput(juce::String);
	void removeInput(juce::String);
	void removeOutput(juce::String);
	int sendMIDI(RatMIDIMessage);
	
private:
	std::map <juce::String, std::pair<juce::MidiInput, uint16>> activeMidiInputs;
	std::map <juce::String, std::pair<juce::MidiOutput, uint16>> activeMidiOutputs;

};

