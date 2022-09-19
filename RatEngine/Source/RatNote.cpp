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
					  
#include "RatIO.h"
#include "RatNote.h"

uint8 RatNote::tonalCenter = 60;

RatNote::RatNote(uint32 _id, uint32 _num = 1, uint32 _den = 1, double _centOffset = 0, uint8 _instrument = 1, uint8 _voice = 0, uint8 _vel = 100, uint8 _region = 0)
{
	id = _id;
	num = _num;
	den = _den;
	voice = _voice;
	region = _region;
	selected = 0;
	instrument = _instrument;
	vel = _vel;
	centOffset = _centOffset;
	selected = false;
}
RatNote::RatNote(int _num, int _den, int _cents=0) : num(_num), den(_den), centOffset(_cents)
{
	id = 0;
	voice = 0;
	region = 0;
	selected = false;
	instrument = 1;
	vel = 100;
	centOffset = 0;

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

void RatNote::setId(uint32 _id)
{
	id = _id;
}

void RatNote::setInstrument(uint8 _instrument)
{
	instrument = _instrument;
}

void RatNote::setVoice(uint8 _voice)
{
	voice = _voice;
}

void RatNote::setVel(uint8 _vel)
{
	vel = _vel;
}

void RatNote::setRegion(uint8 _region)
{
	region = _region;
}

void RatNote::setSelected(bool _selected)
{
	selected = _selected;
}

void RatNote::setNum(uint32 _num)
{
	num = _num;
}

void RatNote::setDen(uint32 _den)
{
	den = _den;
}

void RatNote::setCentOffset(double _centOffset)
{
	centOffset = _centOffset;
}

void RatNote::setTime(double _time)
{
	time = _time;
}

void RatNote::setDuration(double _duration)
{
	duration = _duration;
}

int createNoteOn()
{
	
	return 0;
}