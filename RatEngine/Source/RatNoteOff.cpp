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

#include "RatNoteOff.h"

RatNoteOff::RatNoteOff(uint8 nn_, uint8 vel_, uint8 channel_, double timestamp_, uint8 instrument_, uint32 id_, std::shared_ptr<RatMidiMessage> ptnr_)
	: RatMidiMessage(128 + (channel_ % 17), nn_ & 127, vel_ & 127, timestamp_, instrument_, id_, ptnr_)
//	: juce::MidiMessage(128 + (channel_ % 17), nn_ & 127, vel_ & 127, timestamp_)
{
	nn = nn_;
	vel = vel_;
	channel_ %= 17;
	channel = channel_;
}

RatNoteOff::~RatNoteOff()
{

}

int RatNoteOff::play()
{
	return 0;
}

int RatNoteOff::trigger()
{
	return 0;
}