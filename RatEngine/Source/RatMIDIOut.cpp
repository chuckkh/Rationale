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

#include "JuceHeader.h"
#include "RatMidiOut.h"

RatMidiOut::RatMidiOut()
{
	
}

RatMidiOut::RatMidiOut(std::string _name, uint8 _channel)
{
	outputDeviceKey = juce::String(_name);
	channel = _channel;
}

RatMidiOut::RatMidiOut(std::string _name, int _channel)
{
	outputDeviceKey = juce::String(_name);
	channel = uint8(_channel);
}

RatMidiOut::RatMidiOut(juce::String _name, uint8 _channel)
{
	outputDeviceKey = _name;
	channel = _channel;
}

RatMidiOut::RatMidiOut(juce::String _name, int _channel)
{
	outputDeviceKey = _name;
	channel = uint8(_channel);
}

void RatMidiOut::setOutputDeviceKey(juce::String _name)
{
	outputDeviceKey = _name;
}

juce::String RatMidiOut::getOutputDeviceKey()
{
	return outputDeviceKey;
}

void RatMidiOut::setChannel(uint8 _channel)
{
	channel = _channel;
}

uint8 RatMidiOut::getChannel()
{
	return channel;
}