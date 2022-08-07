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

    RatEngine.h
    Created: 11 Feb 2022 2:06:16am
    Author:  Home

  ==============================================================================
*/

#pragma once
#include <JuceHeader.h>
#include <string>
#include <algorithm>
#include <map>
#include "RatIOManager.h"
#include "RatNote.h"

class RatEngine : public juce::InterprocessConnection
{
public:
    //RatEngine(bool, int);
    //RatEngine(int);
    RatEngine(int, juce::JUCEApplication&);
    /*RatEngine(int);
    RatEngine();*/
    ~RatEngine();
    void messageReceived(const MemoryBlock&) override;
    void connectionMade() override;
    void connectionLost() override;
    void endItAll();
    void run();
    void sendStdString(const std::string&);
    void sendString(const juce::String&);
    void sendAvailableMidiInDevices();
    void sendAvailableMidiOutDevices();
    void setCbPort(int);
    void addNote(int);
//    bool sendMessageNoHeader(const MemoryBlock&);
//    void timerCallback();

private:
    int cbport;
    bool active = true;
    std::unique_ptr<juce::MidiOutput> mdout;

    juce::OwnedArray<RatIOManager> ioManagers;
    JUCEApplication& app;
    std::map<uint32, std::unique_ptr<RatNote>> score;
    std::map<juce::String, juce::String> midiInDevices;
    std::map<juce::String, juce::String> midiOutDevices;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (RatEngine)
};
