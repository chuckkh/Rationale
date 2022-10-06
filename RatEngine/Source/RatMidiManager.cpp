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
#include "RatNote.h"
#include <iostream>
#include <typeinfo>
#include <map>
#include <memory>

RatMidiManager::RatMidiManager()
	: currentMidiScoreTime(0)
{
	
}

void RatMidiManager::handleIncomingMidiMessage(juce::MidiInput* input, const juce::MidiMessage& msg)
{

	if (msg.isSongPositionPointer()) {

		std::cout << "\nReceived: SPP: " << msg.getSongPositionPointerMidiBeat();
	}
	else if (msg.isMidiClock()) {
		std::cout << "...tick ";
	}
	else if (msg.isMidiStart()) { std::cout << '\n' << "Received: MIDI Start"; }
	else if (msg.isMidiStop()) { std::cout << '\n' << "Received: MIDI Stop"; }
	else if (msg.isMidiContinue()) { std::cout << '\n' << "Received: MIDI Continue"; }
	else if (msg.isSysEx()) {
		std::cout << '\n' << "Received SysEx:";
		int sz = msg.getSysExDataSize();
		for (int i = 0; i < sz; i++) {
			std::cout << " " << *(msg.getSysExData() + i);
		}
	}
}

void RatMidiManager::sendRatMidiMessage(RatMidiMessage &msg)
{
	juce::String nm = RatNote::instruments[msg.getInstrument()][0].first;
	juce::String identifier = midiOutDevices[nm];
	if (msg.getPreMessage() != nullptr)
	{
		activeMidiOutputs[identifier]->sendMessageNow(*msg.getPreMessage());
	}
	activeMidiOutputs[identifier]->sendMessageNow(msg);
}

void RatMidiManager::stepThroughMidiScoreTo(double t_)
{
	std::bitset<128> nn_;
	std::map<uint8, std::shared_ptr<RatNoteOn>> sn_;
	double cmst_ = currentMidiScoreTime;
	std::list<std::shared_ptr<RatMidiMessage>>::iterator msit_ = midiScore.begin();
	if (t_ < cmst_)
	{
		nn_ = { 0 };
		cmst_ = 0;
	}
	else if (t_ > cmst_)
	{
		nn_ = noteNumbers;
		sn_ = soundingNotes;
		while ((*msit_)->getTimeStamp() < cmst_)
		{
			++msit_;
		}
	}
	while (cmst_ < t_)
	{
		// The time has to keep jumping to the next iterator until it's >= t_.
		// Each msg has to go through find/clear note numbers
		auto mm_ = *msit_;
		if (mm_->isNoteOn())
		{

		}

	}


	int a = 0;
}

void RatMidiManager::startPlayback()
{
	prepareToPlay();
	//
	// I have to redo this! To find the right score index for the starting point.
	//
	playing = true;
	playMode = RatPlayMode::Play;
	//currentScoreIndex = midiManager.getNextIndexAtTime(currentScoreTime);
	//scoreCursor = midiManager.begin();
}

void RatMidiManager::stopPlayback()
{
	playing = false;
	playMode = RatPlayMode::Stop;
}

void RatMidiManager::continuePlayback()
{
	playing = true;
	playMode = RatPlayMode::Play;
}

void RatMidiManager::setSPP(uint16 sixteenths)
{
	stepThroughMidiScoreTo(double(sixteenths) * 0.25);
	setCurrentMidiScoreTime(double(sixteenths) * 0.25);
	//
	// I have to redo this! To find the right score index for the starting point.
	//

}

void RatMidiManager::incrementMidiBeatClock()
{
	/*
	double t_ = getCurrentScoreTime() + 1.0 / 24.0;
	setCurrentScoreTime(t_);
	if (playing)
	{

		while (currentScoreTime >= midiManager.getEventTime(currentScoreIndex))
		{
			auto eventHolder = midiManager.getEventPointer(currentScoreIndex);

			std::shared_ptr<RatMidiMessage> scoreEvent = std::dynamic_pointer_cast<RatMidiMessage>(std::make_shared<juce::MidiMessage>(eventHolder->message));
			std::shared_ptr<juce::MidiMessage> pre = scoreEvent->getPreMessage();
			if (pre == nullptr)
				// noteoff
			{
				//send message
				midiManager.clearAvailableNoteNumber(scoreEvent->getChannel());
			}
			else
				// noteon
			{

			}

		}
	}
	*/
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
		activeMidiInput = juce::MidiInput::openDevice(device, this);
		activeMidiInput->start();
	}
//	activeMidiInput.reset(juce::MidiInput::openDevice())
}

void RatMidiManager::addActiveMidiOutput(juce::String name)
{
	if (activeMidiOutputs.count(name) == 0)
	{
		juce::String device = midiOutDevices[name];
		activeMidiOutputs[name] = juce::MidiOutput::openDevice(device);
	}
}

void RatMidiManager::resetOuts()
{
	activeMidiOutputs.clear();
	ratMidiOuts.clear();
}

void RatMidiManager::addOut(uint32 instNumber, juce::String devName, uint8 channel)
{
	while (ratMidiOuts.size() < uint64(instNumber) + 1)
	{
		std::vector<RatMidiOut> temp;
		ratMidiOuts.push_back(temp);
	}

	ratMidiOuts[instNumber].push_back(RatMidiOut(devName, channel));
}

uint8 RatMidiManager::findAvailableNoteNumber(uint8 requested, std::bitset<128>&)
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

void RatMidiManager::clearAvailableNoteNumber(uint8 nn, std::bitset<128>&)
{
	noteNumbers.set(nn, false);
}

void RatMidiManager::addMidiMessage(std::shared_ptr<RatMidiMessage> message_)
{
	std::cerr << "not done line 151\n";
	std::shared_ptr<RatMidiMessage> temp = std::make_shared<RatMidiMessage>(144, 60, 100, 0.0, 1, 1);
	temp = message_;
	midiScore.push_back(temp);
	
//	midiScore.push_back(message_);
//	midiScore.insert(midiScore.end(), message_);
//	midiScore.push_back(std::make_shared<RatMidiMessage>(1, 1, 1, 1.0, 1, 1));
//	midiScore.back() = message_;
	std::cerr << "done?" << '\n';
//	std::wcerr << midiScore.back()->getId() << '\n';
//	std::shared_ptr<RatMidiMessage> temp;
//	temp = message_;
//	std::wcerr << temp->getId() << ' ' << temp->isNoteOn() << '\n';
//	midiScore.push_back(temp);
//	midiScore.insert(std::pair<double, std::shared_ptr<RatMidiMessage>>(time_, message_));
}

bool compareRatMidiMessages(const std::shared_ptr<RatMidiMessage> first, const std::shared_ptr<RatMidiMessage> second)
{
	return (first->getTimeStamp() < second->getTimeStamp());
}

void RatMidiManager::sortMidiScore()
{
	midiScore.sort(compareRatMidiMessages);
}

void RatMidiManager::eraseMidiMessage(uint32 id_)
{
	std::list<std::shared_ptr<RatMidiMessage>>::iterator it = midiScore.begin();
	std::cerr << "size of MidiScore: " << midiScore.size() << '\n';

	//midiScore.erase(removeIterator, midiScore.end());
/*
	for (std::shared_ptr<RatMidiMessage> mm : midiScore)
	{
		std::cerr << "erasing?? \n";
		std::cerr << typeid(mm.get()).name() << '\n';
		auto wtf = mm.get();
		if (wtf == nullptr)
		{
			std::cerr << "null\n";
		}
		else
		{
			std::cerr << wtf->getId() << '\n';
		}
	}
/**/
	while (!midiScore.empty() && it != midiScore.end())
	{
//		std::cerr << "erasing? \n";
//		std::cerr << typeid(*it).name() << std::endl;
//		std::cerr << (**it).getId() << std::endl;
//		if (false)
		if ((*it) != nullptr && (*it)->getId() == id_)
		{
			std::cerr << "erasing id" << id_ << "\n";
			auto temp = midiScore.erase(it);
			it = temp;
//			std::cerr << "erased\n";
		}
		else
		{
			std::cerr << "not erasing id" << (*it)->getId() << "\n";
			it++;
//			std::cerr << "not erased\n";
		}
	}/**/
	std::cerr << "size of MidiScore: " << midiScore.size() << '\n';
}

void RatMidiManager::clearMidiScore()
{
	midiScore.clear();
}

void RatMidiManager::prepareToPlay()
{
	sortMidiScore();
	midiScoreIt = midiScore.begin();
	while ((*midiScoreIt)->getTimeStamp() < currentMidiScoreTime)
	{
		++midiScoreIt;
	}
}

double RatMidiManager::getCurrentMidiScoreTime()
{
	return currentMidiScoreTime;
}

void RatMidiManager::setCurrentMidiScoreTime(double t_)
{
	currentMidiScoreTime = t_;
}

void RatMidiManager::addToCurrentMidiScoreTime(double delta_)
{
	currentMidiScoreTime = currentMidiScoreTime + delta_;
}

void RatMidiManager::clearMidiScoreDelete()
{
	midiScoreDelete.clear();
}