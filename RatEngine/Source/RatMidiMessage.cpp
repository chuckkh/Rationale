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

/*
  ==============================================================================

    RatMidiMessage.cpp
    Created: 2 Aug 2022 10:41:36pm
    Author:  Home

  ==============================================================================
*/

#include "RatMidiMessage.h"

/*
RatMidiMessage::RatMidiMessage(uint8 nn_, uint8 vel_, uint8 channel_, double timestamp_, juce::String out_)
    : juce::MidiMessage(144 + (channel_ % 17), nn_ & 127, vel_ & 127, timestamp_)
{
    preMessage = nullptr;
}
*/

RatMidiMessage::RatMidiMessage(uint8 b1, uint8 b2, uint8 b3, double timestamp_, uint8 instrument_, uint32 id_)
    : juce::MidiMessage(b1, b2, b3, timestamp_)
{
    preMessage = nullptr;
    setInstrument(instrument_);
    setId(id_);
    //setOut(out_);
}

juce::String RatMidiMessage::getOut()
{
    return out;
}

void RatMidiMessage::setOut(juce::String out_)
{
    out = out_;
}

void RatMidiMessage::setPreMessage(const void* data, int sz)
{
    preMessage.reset(&juce::MidiMessage::createSysExMessage(data, sz));
}

std::shared_ptr<juce::MidiMessage> RatMidiMessage::getPreMessage()
{
    return preMessage;
}

void RatMidiMessage::setPreMessageOut(juce::String out_)
{
    preMessage->setOut(out_);
}

int RatMidiMessage::trigger()
{
    return 0;
}

uint8 RatMidiMessage::getInstrument()
{
    return instrument;
}

void RatMidiMessage::setInstrument(uint8 instrument_)
{
    instrument = instrument_;
}

uint32 RatMidiMessage::getId()
{
    return id;
}

void RatMidiMessage::setId(uint32 id_)
{
    id = id_;
}