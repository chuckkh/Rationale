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
#include "RatEvent.h"
#include "JuceHeader.h"

class RatNoteOn :
    public RatEvent, juce::MidiMessage
{
public:
    RatNoteOn::RatNoteOn(uint8, uint8, uint32, uint8, uint8, uint8);
    int trigger() override;
    void setMTS(const void *, int);
    std::shared_ptr<juce::MidiMessage> getMTS();
private:
    std::shared_ptr<juce::MidiMessage> MTSMessage;
    juce::String out;
};

