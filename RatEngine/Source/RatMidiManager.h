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

//#include "RatIOManager.h"
#include "JuceHeader.h"
//#include "RatMidiMessage.h"
#include "RatMidiInputCallback.h"
#include "RatNoteOn.h"
#include <queue>
#include <map>
#include <memory>
#include <bitset>
#include <forward_list>
#include <list>
#include <atomic>
#include <set>

enum class RatPlayMode { Stop, Play, Edit, Scrub };


class RatMidiManager : public juce::MidiMessageSequence, public juce::MidiInputCallback
{
public:
	struct AvailableNoteNumbers
	{
		std::bitset<128> noteNumbers;
	};

private:
	class ChainOfAvailableNoteNumbers
	{
		std::list<AvailableNoteNumbers> seriesOfAvailableNoteNumbers;

	};

public:

	RatMidiManager();
	void handleIncomingMidiMessage(juce::MidiInput*, const juce::MidiMessage&) override;
	void sendRatMidiMessage(RatMidiMessage&, juce::String);
	void stepThroughMidiScoreTo(double);
	void startPlayback();
	void stopPlayback();
	void continuePlayback();
	void setSPP(uint16);
	void incrementMidiBeatClock();
	void addInput(juce::String);
	void addOutput(juce::String);
	void removeInput(juce::String);
	void removeOutput(juce::String);
	int sendMidi(RatMidiMessage);
	void setActiveMidiInput(juce::String);
	void clearMidiInDevices();
	void addMidiInDevice(juce::String, juce::String);
	void clearMidiOutDevices();
	void addMidiOutDevice(juce::String, juce::String);
	void resetOuts();
	void addOut(uint32, juce::String, uint8);
	uint8 findAvailableNoteNumber(uint8, std::bitset<128>&);
	void clearAvailableNoteNumber(uint8, std::bitset<128>&);
	void addMidiMessage(std::shared_ptr<RatMidiMessage>);
	void sortMidiScore();
	void eraseMidiMessage(uint32);
//	void uneraseMidiMessage(uint32);
	void clearMidiScore();
	void prepareToPlay();
	double getCurrentMidiScoreTime();
	void setCurrentMidiScoreTime(double);
	void addToCurrentMidiScoreTime(double);
	double getSongPosition();
	void setSongPosition(double);
	void clearMidiScoreDelete();
	void addActiveMidiOutput(juce::String);

	// In case a note is added or edited during playback, this retrieves a note
	// number that is not used anywhere in the existing score.
	uint8 getUnusedNoteNumber();

	// In case a note added during playback ends, this returns its note number
	// to the list.
	void setUnusedNoteNumber(uint8);
	void setUsedNoteNumber(uint8);
	void clearUsedNoteNumber(uint8);
private:
	//std::map <juce::String, std::pair<juce::MidiInput, uint16>> activeMidiInputs;
	std::unique_ptr<juce::MidiInput> activeMidiInput;
	RatMidiInputCallback midiInputCallback;
	std::map<juce::String, std::unique_ptr<juce::MidiOutput>> activeMidiOutputs;
	std::map<juce::String, juce::String> midiInDevices;
	std::map<juce::String, juce::String> midiOutDevices;
	std::bitset<128> noteNumbers;
	std::map<uint8, std::shared_ptr<RatNoteOn>> soundingNotes;
//	std::map<double, std::forward_list<std::shared_ptr<RatMidiMessage>>> midiScore;
//	std::map<double, std::shared_ptr<RatMidiMessage>> midiScore;
	
	//std::list<std::shared_ptr<RatMidiMessage>> midiScore;
	std::list<RatMidiMessage*> midiScore1, midiScoreDelete;
	std::list<std::shared_ptr<RatMidiMessage>> midiScore;
	std::vector<std::vector<RatMidiOut>> ratMidiOuts;
//	double currentMidiScoreTime;
	std::atomic<double> currentMidiScoreTime;
	double songPosition;
	std::list<std::shared_ptr<RatMidiMessage>>::iterator midiScoreIt;
	bool playing;
	RatPlayMode playMode = RatPlayMode::Stop;
	std::queue<uint8> unusedNoteNumbers;
	std::set<uint8> usedNoteNumbers;
};

