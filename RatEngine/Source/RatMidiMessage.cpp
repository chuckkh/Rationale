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

RatMidiMessage::RatMidiMessage(uint8 b1, uint8 b2, uint8 b3, double timestamp_, uint8 instrument_, uint32 id_, std::shared_ptr<RatMidiMessage> ptnr_)
    : juce::MidiMessage(b1, b2, b3, timestamp_),
    partner(ptnr_), tuningBytes{ 240, 127, 127, 8, 2, 1, 1, 0, 0, 0, 0, 247 }
{
    preMessage = std::make_shared<juce::MidiMessage>(&tuningBytes, 12);
    setInstrument(instrument_);
    setId(id_);
    //setOut(out_);
}

RatMidiMessage::~RatMidiMessage()
{
    std::cerr << "Destroying base RatMidiMessage\n";
}

juce::String RatMidiMessage::getOut()
{
    return out;
}

void RatMidiMessage::setOut(juce::String out_)
{
    out = out_;
}

/*
void RatMidiMessage::setPreMessage(const void* data, int sz)
{
//    juce::MidiMessage* temp = new juce::MidiMessage();
//    std::shared_ptr<juce::MidiMessage> temp_ = std::make_shared<juce::MidiMessage>(juce::MidiMessage::createSysExMessage(data, sz));
//    *temp = juce::MidiMessage::createSysExMessage(data, sz);
    std::cerr << "tuningBytes: ";
    for (auto bt_ : tuningBytes)
    {
        std::cerr << int(bt_) << " ";
    }
    std::cerr << std::endl;
    preMessage = std::make_shared<juce::MidiMessage>(data, sz);
//    preMessage = std::make_shared<juce::MidiMessage>(juce::MidiMessage::createSysExMessage(data, sz));
//    preMessage.reset(temp);
}
/**/

void RatMidiMessage::setPreMessage()
{
//    juce::MidiMessage* temp = new juce::MidiMessage();
/*
    std::cerr << "tuningBytes: ";
    for (auto bt_ : tuningBytes)
    {
        std::cerr << int(bt_) << " ";
    }
    std::cerr << std::endl;
    /**/
    //    int sz_ = tuningBytes.size();
//    sz_ = (sz_ >= 12 ? 12 : sz_);
    void* voidPtr{ &tuningBytes };
    preMessage = std::make_shared<juce::MidiMessage>(voidPtr, 12);
//    preMessage = std::make_shared<juce::MidiMessage>(juce::MidiMessage::createSysExMessage(&tuningBytes, sz_));
//    *temp = juce::MidiMessage::createSysExMessage(&tuningBytes, sz_);
}

juce::MidiMessage* RatMidiMessage::getPreMessage()
{
    return preMessage.get();
}

void RatMidiMessage::setPreMessageOut(juce::String out_)
{
//    preMessage->setOut(out_);
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

void RatMidiMessage::setPartner(std::shared_ptr<RatMidiMessage> prtnr_)
{
    partner = prtnr_;
    //partner(prtnr_);
}

std::shared_ptr<RatMidiMessage> RatMidiMessage::getPartner()
{
    return partner;
}

void RatMidiMessage::setIdealNn(uint8 idealNn_)
{
    idealNn = idealNn_;
}

uint8 RatMidiMessage::getIdealNn()
{
    return idealNn;
}

uint8 RatMidiMessage::getTuningByte(uint8 ind_)
{
    if (12 <= ind_)
    {
        return -1;
    }
    else
    {
        return tuningBytes[ind_];
    }
}

void RatMidiMessage::setTuningByte(uint8 ind_, uint8 val_)
{
//    while (tuningBytes.size() <= ind_)
//    {
//        tuningBytes.push_back(0);
//    }
    if (ind_ < 12)
    {
        tuningBytes[ind_] = val_;
    }
}
