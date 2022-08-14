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
#include "RatMidiManager.h"

RatMidiManager::RatMidiManager()
{
	
}

void RatMidiManager::addInput(juce::String inputName)
{

}

void RatMidiManager::addOutput(juce::String outputName)
{

}

void RatMidiManager::removeInput(juce::String inputName)
{

}

void RatMidiManager::removeOutput(juce::String outputName)
{

}

int RatMidiManager::sendMidi(RatMidiMessage msg)
{
	return 0;
}

void RatMidiManager::clearMidiInDevices()
{
	midiInDevices.clear();
}

void RatMidiManager::clearMidiOutDevices()
{
	midiOutDevices.clear();
}

void RatMidiManager::addMidiInDevice(juce::String name, juce::String dev)
{
	midiInDevices[name] = dev;
}

void RatMidiManager::addMidiOutDevice(juce::String name, juce::String dev)
{
	midiOutDevices[name] = dev;
}

void RatMidiManager::setActiveMidiInput(juce::String name)
{
	if (midiInDevices.count(name))
	{
		juce::String device = midiInDevices[name];
		activeMidiInput = juce::MidiInput::openDevice(device, &midiInputCallback);
		activeMidiInput->start();
	}
//	activeMidiInput.reset(juce::MidiInput::openDevice())
}