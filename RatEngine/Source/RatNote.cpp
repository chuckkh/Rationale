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

#include <cmath>
#include "RatIO.h"
#include "RatNote.h"

uint8 RatNote::globalTonalCenter = 60;
double RatNote::bit7 = pow(2, 7);
double RatNote::bit14 = pow(2, 14);
double RatNote::semitone = pow(2, 1.0 / 12.0);

RatNote::RatNote(uint32 id_, double time_, double duration_, uint32 num_ = 1, uint32 den_ = 1, double centOffset_ = 0, uint8 instrument_ = 1, uint8 voice_ = 0, uint8 vel_ = 100, uint8 region_ = 0)
	: id(id_), time(time_), duration(duration_), num(num_), den(den_), voice(voice_), region(region_), instrument(instrument_), vel(vel_), centOffset(centOffset_), selected(false)
{
	createNoteOn();
	createNoteOff();
	resetTuning();

}

int RatNote::createNoteOn()
{
	//uint8 nn_, uint8 vel_, uint8 channel_, double timestamp_, juce::String out_
	noteOn = std::make_shared<RatNoteOn>(idealNn, vel, RatNote::instruments[instrument][0].second, time, instrument);
	return 0;
}

int RatNote::createNoteOff()
{
	//uint8 nn_, uint8 vel_, uint8 channel_, double timestamp_, juce::String out_
	noteOff = std::make_shared<RatNoteOff>(idealNn, 0, RatNote::instruments[instrument][0].second, time+duration, instrument);
	return 0;
}

void RatNote::updateNoteOn()
{

}

void RatNote::updateNoteOff()
{

}

int RatNote::play()
{
	return 0;
}

uint32 RatNote::getId()
{
	return id;
}

uint8 RatNote::getInstrument()
{
	return instrument;
}

uint8 RatNote::getVoice()
{
	return voice;
}

uint8 RatNote::getVel()
{
	return vel;
}

uint8 RatNote::getRegion()
{
	return region;
}

bool RatNote::getSelected()
{
	return selected;
}

uint32 RatNote::getNum()
{
	return num;
}

uint32 RatNote::getDen()
{
	return den;
}

double RatNote::getCentOffset()
{
	return centOffset;
}

double RatNote::getTime()
{
	return time;
}

double RatNote::getDuration()
{
	return duration;
}

uint8 RatNote::getIdealNn()
{
	return idealNn;
}

uint8 RatNote::getMtsByte1()
{
	return mtsByte1;
}

uint8 RatNote::getMtsByte2()
{
	return mtsByte2;
}

std::shared_ptr<RatMidiMessage> RatNote::getNoteOn()
{
	return noteOn;
}

std::shared_ptr<RatMidiMessage> RatNote::getNoteOff()
{
	return noteOff;
}

void RatNote::setId(uint32 _id)
{
	id = _id;
}

void RatNote::setInstrument(uint8 instrument_)
{
	instrument = instrument_;
	noteOn->setInstrument(instrument_);
	noteOff->setInstrument(instrument_);
//	noteOn->setOut(instrument_);
//	noteOn->setPreMessageOut(instrument_);
//	noteOff->setOut(instrument_);
	// update NoteOn / NoteOff
}

void RatNote::setVoice(uint8 _voice)
{
	voice = _voice;
	// update NoteOn / NoteOff
}

void RatNote::setVel(uint8 vel_)
{
	vel = vel_;
	noteOn->setVelocity(float(vel_) / 127.0);
}

void RatNote::setRegion(uint8 region_)
{
	region = region_;
}

void RatNote::setSelected(bool selected_)
{
	selected = selected_;
}

void RatNote::setNum(uint32 num_)
{
	num = num_;
	resetTuning();
}

void RatNote::setDen(uint32 den_)
{
	den = den_;
	resetTuning();
}

void RatNote::setCentOffset(double centOffset_)
{
	centOffset = centOffset_;
	resetTuning();
}

void RatNote::setTime(double time_)
{
	time = time_;
	noteOn->setTimeStamp(time_);
	noteOff->setTimeStamp(time_ + duration);
}

void RatNote::setDuration(double duration_)
{
//	double current = noteOff->getTimeStamp();
	duration = duration_;
//	noteOff->addToTimeStamp(duration_ - current);
	noteOff->setTimeStamp(time + duration_);
}

void RatNote::setIdealNn(uint8 idealNn_)
{
	idealNn = idealNn_;
}

void RatNote::setMtsByte1(uint8 mtsByte1_)
{
	mtsByte1 = mtsByte1_;
}

void RatNote::setMtsByte2(uint8 mtsByte2_)
{
	mtsByte2 = mtsByte2_;
}

void RatNote::resetTuning()
{
	double goal = (log(num / den) / log(semitone)) * RatNote::regions[region]->getNum() / RatNote::regions[region]->getDen() + centOffset * 0.01 + RatNote::globalTonalCenter;
	goal = round(goal * bit14 / bit14);
	tuningBytes = { 127, 127, 8, 2, 1, 1, uint8(goal), uint8(goal) };
	setIdealNn(uint8(goal));
	goal -= idealNn;
	goal *= bit7;
	tuningBytes.push_back(uint8(goal));
	setMtsByte1(uint8(goal));
	goal *= bit7;
	tuningBytes.push_back(uint8(goal));
	setMtsByte2(uint8(goal));
	if (noteOn != nullptr)
	{
		noteOn->setNoteNumber(idealNn);
		noteOn->setPreMessage(&tuningBytes, 10);
	}
	if (noteOff != nullptr)
	{
		noteOff->setNoteNumber(idealNn);
	}
}