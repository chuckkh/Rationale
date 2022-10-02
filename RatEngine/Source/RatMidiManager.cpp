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

void RatMidiManager::resetOuts()
{
	ratMidiOuts.clear();
}

void RatMidiManager::addOut(uint32 instNumber, juce::String devName, uint8 channel)
{
	while (ratMidiOuts.size() < uint64(instNumber + 1))
	{
		std::vector<RatMidiOut> temp;
		ratMidiOuts.push_back(temp);
	}

	ratMidiOuts[instNumber].push_back(RatMidiOut(devName, channel));
}

uint8 RatMidiManager::findAvailableNoteNumber(uint8 requested)
{
	uint8 outp = requested;
	int16 offset = 1;
	int8 sign = 1;
	while (noteNumbers.test(requested))
	{
		requested += offset * sign;
		offset += 1;
		sign = -sign;
		if (requested < 0 || requested > 127)
		{
			requested += offset * sign;
			offset += 1;
			sign = -sign;
		}
	}
	noteNumbers.set(requested);
	return requested;
}

void RatMidiManager::clearAvailableNoteNumber(uint8 nn)
{
	noteNumbers.set(nn, false);
}

void RatMidiManager::addMidiMessage(std::shared_ptr<RatMidiMessage> message_)
{
	midiScore.push_back(message_);
//	midiScore.insert(std::pair<double, std::shared_ptr<RatMidiMessage>>(time_, message_));
}

bool compareRatMidiMessages(const RatMidiMessage& first, const RatMidiMessage& second)
{
	return (first.getTimeStamp() < second.getTimeStamp());
}

void RatMidiManager::sortMidiScore()
{
	midiScore.sort(compareRatMidiMessages);
}

void RatMidiManager::eraseMidiMessage(uint32 id_)
{
	std::list<std::shared_ptr<RatMidiMessage>>::iterator it = midiScore.begin(), theEnd = midiScore.end();
	while (it != theEnd)
	{
		if ((*it)->getId() == id_)
		{
			it = midiScore.erase(it);
		}
		else
		{
			it++;
		}
	}
}

void RatMidiManager::clearMidiScore()
{
	midiScore.clear();
}