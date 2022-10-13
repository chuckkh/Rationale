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
std::vector<std::unique_ptr<RatRegion>> RatNote::regions;
std::vector<std::vector<std::pair<juce::String, uint8>>> RatNote::instruments;

RatNote::RatNote(uint32 id_, double time_, double duration_, uint32 num_ = 1, uint32 den_ = 1, double centOffset_ = 0, uint8 instrument_ = 1, uint8 voice_ = 0, uint8 vel_ = 100, uint8 region_ = 0)
	: id(id_), time(time_), duration(duration_), num(num_), den(den_), voice(voice_), region(region_), instrument(instrument_), vel(vel_), centOffset(centOffset_), selected(false)
{
	createNoteOn();
	createNoteOff();
	resetTuning();

}

RatNote::RatNote(int a, int b, int c)
{
	//uint32 id_, double time_, double duration_, uint32 num_ = 1, uint32 den_ = 1, double centOffset_ = 0, uint8 instrument_ = 1, uint8 voice_ = 0, uint8 vel_ = 100, uint8 region_ = 0
	id = a;
	instrument = b;
	voice = 0;
	vel = 0;
	region = 0;
	time = 0.0;
	duration = 1.0;
	selected = false;
	num = 1;
	den = 1;
	centOffset = 0.0;
	idealNn = c;
	mtsByte1 = 0;
	mtsByte2 = 0;

}

int RatNote::createNoteOn()
{
	//uint8 nn_, uint8 vel_, uint8 channel_, double timestamp_, juce::String out_
	//RatNoteOn temp(idealNn, vel, RatNote::instruments[instrument][0].second, time, instrument, id);
//	noteOn = std::make_shared<RatNoteOn>(idealNn, vel, RatNote::instruments[instrument][0].second, time, instrument);
	uint8 nn_ = 60;
	uint8 arg3_ = 1;
	if (noteOn == nullptr)
	{
		noteOn = std::make_unique <RatNoteOn>(nn_, vel, arg3_, time, instrument, id, noteOff);
	}
	else
	{
		noteOn.reset(new RatNoteOn(nn_, vel, arg3_, time, instrument, id, noteOff));
	}
	std::cerr << "noteOn created : " << noteOn->getId() << std::endl;
	if (noteOff != nullptr)
	{
		noteOff->setPartner(noteOn);
	}
	return 0;
}

int RatNote::createNoteOff()
{
	//uint8 nn_, uint8 vel_, uint8 channel_, double timestamp_, juce::String out_
	if (noteOff == nullptr)
	{
		noteOff = std::make_shared<RatNoteOff>(60, 0, 1, time + duration, instrument, id, noteOn);
	}
//	RatNoteOff temp(idealNn, 0, RatNote::instruments[instrument][0].second, time + duration, instrument, id);
	else
	{
		noteOff.reset(new RatNoteOff(60, 0, 1, time + duration, instrument, id, noteOn));
	}
	if (noteOn != nullptr)
	{
		noteOn->setPartner(noteOff);
	}
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

void RatNote::setId(uint32 id_)
{
	id = id_;
	std::cerr << "id is now: " << id << std::endl;
}

void RatNote::setInstrument(uint8 instrument_)
{
	instrument = instrument_;
	noteOn->setInstrument(instrument_);
	noteOff->setInstrument(instrument_);
	std::cerr << "inst is now: " << instrument << std::endl;
//	noteOn->setOut(instrument_);
//	noteOn->setPreMessageOut(instrument_);
//	noteOff->setOut(instrument_);
	// update NoteOn / NoteOff
}

void RatNote::setVoice(uint8 voice_)
{
	voice = voice_;
	std::cerr << "voice is now: " << voice << std::endl;
	// update NoteOn / NoteOff
}

void RatNote::setVel(uint8 vel_)
{
	vel = vel_;
	noteOn->setVelocity(float(vel_) / 127.0);
	std::cerr << "vel is now: " << vel << std::endl;
}

void RatNote::setRegion(uint8 region_)
{
	region = region_;
	std::cerr << "reg is now: " << region << std::endl;
}

void RatNote::setSelected(bool selected_)
{
	selected = selected_;
	std::cerr << "sel is now: " << selected << std::endl;
}

void RatNote::setNum(uint32 num_)
{
	num = num_;
	std::cerr << "num is now: " << num << std::endl;
	resetTuning();
}

void RatNote::setDen(uint32 den_)
{
	den = den_;
	std::cerr << "den is now: " << den << std::endl;
	resetTuning();
}

void RatNote::setCentOffset(double centOffset_)
{
	centOffset = centOffset_;
	std::cerr << "centoffset is now: " << centOffset << std::endl;
	resetTuning();
}

void RatNote::setTime(double time_)
{
	time = time_;
	std::cerr << "time is now: " << time << std::endl;
	noteOn->setTimeStamp(time_);
	noteOff->setTimeStamp(time_ + duration);
}

void RatNote::setDuration(double duration_)
{
//	double current = noteOff->getTimeStamp();
	duration = duration_;
	std::cerr << "duration is now: " << duration << std::endl;
//	noteOff->addToTimeStamp(duration_ - current);
	noteOff->setTimeStamp(time + duration_);
}

void RatNote::setIdealNn(uint8 idealNn_)
{
	idealNn = idealNn_;
	noteOn->setIdealNn(idealNn_);
	noteOff->setIdealNn(idealNn_);
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
	std::cerr << "resetTuning: " << std::endl;
	uint32 rnum = RatNote::regions[region]->getNum();
	uint32 rden = RatNote::regions[region]->getDen();
	std::cerr << "ratio..." << (log(double(num) * double(rnum) / (double(den) * double(rden))) / log(semitone)) << std::endl;
	double goal = (log(double(num) * double(rnum) / (double(den) * double(rden))) / log(semitone)) + centOffset * 0.01 + RatNote::globalTonalCenter;
	std::cerr << " goal: " << goal;
	uint8 b1 = trunc(goal);
//	goal = round(goal * bit14 / bit14);
	std::cerr << " goal: " << goal;
	// Byte 7 here is the one that changes if the note number is not available.
	noteOn->setTuningByte(7, b1);
	noteOn->setTuningByte(8, b1);

//	uint8 bytes[8] = { 127, 127, 8, 2, 1, 1, b1, b1 };
//	for ()
	setIdealNn(b1);
//	goal -= idealNn;
//	goal *= bit7;
	goal = bit7 * (goal - b1);
	std::cerr << " goal: " << goal;
	b1 = trunc(goal);
//	tuningBytes.push_back(b1);
	noteOn->setTuningByte(9, b1);
	setMtsByte1(b1);
	goal = bit7 * (goal - b1);
	std::cerr << " goal: " << goal << std::endl;
	b1 = trunc(goal);
//	tuningBytes.push_back(b1);
	noteOn->setTuningByte(10, b1);

	setMtsByte2(b1);
	if (noteOn != nullptr)
	{
		noteOn->setNoteNumber(idealNn);
		noteOn->setPreMessage();
	}
	if (noteOff != nullptr)
	{
		noteOff->setNoteNumber(idealNn);
	}
}