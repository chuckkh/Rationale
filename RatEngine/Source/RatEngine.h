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
#include "RatIOManager.h"

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
    void sendString(const std::string&);
    void sendString(const juce::String&);
    void sendAvailableMidiInDevices();
    void sendAvailableMidiOutDevices();
    void setCbPort(int);
    bool sendMessageNoHeader(const MemoryBlock&);
//    void timerCallback();

private:
    int cbport;
    bool active = true;
    juce::OwnedArray<RatIOManager> ioManagers;
    JUCEApplication& app;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (RatEngine)
};