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
#include "RatEvent.h"
#include "RatRegion.h"
#include "RatMidiMessage.h"
#include "RatNoteOn.h"
#include "RatNoteOff.h"
#include <memory>
#include <vector>

class RatNote //: public RatEvent
{
public:
	RatNote(uint32, double, double, uint32, uint32, double, uint8, uint8, uint8, uint8);
	RatNote(int, int, int);
	int createNoteOn();
	int createNoteOff();
	void updateNoteOn();
	void updateNoteOff();

	int play();
	static uint8 globalTonalCenter;
	static double globalCentsOffset;
	uint32 getId();
	uint8 getInstrument();
	uint8 getVoice();
	uint8 getVel();
	uint8 getRegion();
	bool getSelected();
	uint32 getNum();
	uint32 getDen();
	double getCentOffset();
	double getTime();
	double getDuration();
	uint8 getIdealNn();
	uint8 getMtsByte1();
	uint8 getMtsByte2();
	std::shared_ptr<RatMidiMessage> getNoteOn();
	std::shared_ptr<RatMidiMessage> getNoteOff();
	void setId(uint32);
	void setInstrument(uint8);
	void setVoice(uint8);
	void setVel(uint8);
	void setRegion(uint8);
	void setSelected(bool);
	void setNum(uint32);
	void setDen(uint32);
	void setCentOffset(double);
	void setTime(double);
	void setDuration(double);
	void setIdealNn(uint8);
	void setMtsByte1(uint8);
	void setMtsByte2(uint8);
	void resetTuning();
	static std::vector<std::unique_ptr<RatRegion>> regions;
	static std::vector<std::vector<std::pair<juce::String, uint8>>> instruments;
	static double bit7;
	static double bit14;
	static double semitone;

private:
	uint32 id;
	uint8 instrument;
	uint8 voice;
	uint8 vel;
	uint8 region;
	double time, duration;
	bool selected;
	uint32 num;
	uint32 den;
//	uint32 cents;
	double centOffset;
	std::shared_ptr<RatMidiMessage> noteOn, noteOff;
//	std::shared_ptr<RatNoteOn> noteOn;
//	std::shared_ptr<RatNoteOff> noteOff;
	uint8 idealNn;
	uint8 mtsByte1;
	uint8 mtsByte2;
	std::vector<uint8> tuningBytes;
//	uint32 beat;
//	uint32 beatSubNum;
//	uint32 beatSubDen;
};
