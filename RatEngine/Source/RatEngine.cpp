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

    RatEngine.cpp
    Created: 11 Feb 2022 2:06:39am
    Author:  Charles S. Hubbard, Jr.

  ==============================================================================
*/

#include "RatEngine.h"
#include <string>
#include <iostream>
//#include <chrono>
//#include <thread>
/*
RatEngine::RatEngine(int portno) {
    cbport = portno;
    connectToSocket("127.0.0.1", cbport, 10000);
    std::string mystr = "Hello World!";
    bool sent;
    for (int r = 0; r < 4; r++) {
        MemoryBlock myMessage;
        myMessage.setSize(12);
        for (int i = 0; i < 12; i++) {
            myMessage[i] = mystr[i];
        }
        sent = sendMessage(myMessage);
    }
    int g;
    std::cin >> g;
    //startTimer(100000);
//    std::function<void()> endItAll = [&]() {this->active = false; };
//    while (active) {
//        callAfterDelay(100000, endItAll);
//    }
}*/

RatEngine::RatEngine(int port, JUCEApplication &a) :
    cbport(port),
    juce::InterprocessConnection::InterprocessConnection(false),
    app(a) {
    setTonalCenter(60);
}

/*RatEngine::RatEngine(int port) :
    cbport(port),
    juce::InterprocessConnection::InterprocessConnection(false) {
    
}

RatEngine::RatEngine() :
    cbport(5899),
    juce::InterprocessConnection::InterprocessConnection(false) {

}*/

void RatEngine::setCbPort(int pno) {
    cbport = pno;
}

void RatEngine::run() {
    std::cout << "Well howdy do!" << std::endl;
    //int cbport = 5899;
    bool connected = connectToSocket("127.0.0.1", cbport, 5000);
    std::cout << (connected ? "Connected " : "Not connected ") << cbport << std::endl;
    std::string mystr = "Hello World!";
    bool sent;
/*    for (int r = 0; r < 4; r++) {
        MemoryBlock myMessage;
        myMessage.setSize(12);
        for (int i = 0; i < 12; i++) {
            myMessage[i] = mystr[i];
        }
        sent = sendMessage(myMessage);
    }*/
    std::cout << "running..." << std::endl;
//    int g;
//    std::cin >> g;
}

void RatEngine::sendStdString(const std::string& outMsg)
{
    int messageLength = outMsg.length();
    MemoryBlock myMessage;
    int i = 0;
    for (; i < messageLength; i++) {
        myMessage[i] = outMsg[i];
    }
    myMessage[i] = 'C';
    i++;
    myMessage[i] = 'B';
    bool sent = juce::InterprocessConnection::sendMessageNoHeader(myMessage);
}

void RatEngine::sendString(const juce::String& outMsg)
{
    int messageLength = outMsg.length();
    MemoryBlock myMessage;
    myMessage.setSize(messageLength+2);
    int i = 0;
    for (; i < messageLength; i++) {
        myMessage[i] = outMsg[i];
    }
    myMessage[i] = 'C';
    i++;
    myMessage[i] = 'B';
    bool sent = juce::InterprocessConnection::sendMessageNoHeader(myMessage);
}

void RatEngine::sendAvailableMidiInDevices()
{
    std::cout << "Getting Available MIDI In Devices..." << std::endl;
    auto iDevices = MidiInput::getAvailableDevices();
    sendString("MidiInBegin");
    midiManager.clearMidiInDevices();
    for (juce::MidiDeviceInfo& dev : iDevices) {
        auto name = dev.name.dropLastCharacters(std::max(0, dev.name.length() - 56));
        sendString(name);
//        sendString(dev.identifier.dropLastCharacters(std::max(0, dev.identifier.length()-56)));
        midiManager.addMidiInDevice(name, dev.identifier);
    }
    sendString("MidiInEnd");
}

void RatEngine::sendAvailableMidiOutDevices()
{
    std::cout << "Getting Available MIDI Out Devices..." << std::endl;
    auto oDevices = MidiOutput::getAvailableDevices();
    sendString("MidiOutBegin");
    midiManager.clearMidiOutDevices();
    for (juce::MidiDeviceInfo& dev : oDevices) {
        auto name = dev.name.dropLastCharacters(std::max(0, dev.name.length() - 56));
//        sendString(dev.identifier.dropLastCharacters(std::max(0, dev.identifier.length()-56)));
        sendString(name);
        midiManager.addMidiOutDevice(name, dev.identifier);
/*        if (dev.name.compare("loopMIDI Port") == 0)
        {
            mdout = juce::MidiOutput::openDevice(dev.identifier);
            uint8 vel = 100;
            juce::MidiMessage mdmsg = juce::MidiMessage::noteOn(1, 60, vel);
            for (int i = 0; i < 100; i++)
            {
                mdout->sendMessageNow(mdmsg);
            }
        }*/
    }
    sendString("MidiOutEnd");
    sendSysExTest();
}

void RatEngine::sendSysExTest()
{
    juce::Array<MidiDeviceInfo> devices = juce::MidiOutput::getAvailableDevices();

    //juce::MidiOutput midout();
    auto midout = juce::MidiOutput::openDevice(devices[1].identifier);
    uint8 data[] = {127, 127, 8, 2, 0, 1, 60, 61, 100, 100};
    int sz = 10;

    juce::MidiMessage msg = juce::MidiMessage::createSysExMessage(data, sz);

    midout->sendMessageNow(msg);
    std::cerr << "MTS sent!";
    std::cout << "MTS sent!";
}

void RatEngine::endItAll() {
//    std::cout << "endItAll: line 186" << std::endl;
    for (int r = 0; r < 1; r++) {
        MemoryBlock myMessage;
        std::string mystr = "ENDCB";
        myMessage.setSize(5);
        for (int i = 0; i < 5; i++) {
            myMessage[i] = mystr[i];
        }
        bool sent = juce::InterprocessConnection::sendMessageNoHeader(myMessage);
    }
    app.systemRequestedQuit();
    //active = false;
    while (active) {

    }
    std::cout << "ending..." << std::endl;
//    int g;
//    std::cin >> g;
}

RatEngine::~RatEngine() {
//    std::cout << "~RatEngine: line 207" << std::endl;
    disconnect();
}

void RatEngine::messageReceived(const juce::MemoryBlock &msg) 
{
//    sendMessage(msg);
    juce::String textMessage = msg.toString();
    std::cout << "Rationale to Engine: " << textMessage << std::endl;
    if (textMessage.compare("GetMidiIn") == 0) {
        sendAvailableMidiInDevices();
    }
    else if (textMessage.compare("GetMidiOut") == 0) {
        sendAvailableMidiOutDevices();
    }
    else if (textMessage.compare("ENDCB") == 0) {
        std::cout << "That's all, folks!" << std::endl;
        active = 0;
        endItAll();
//        app.quit();
//        app.systemRequestedQuit();
        //shutdown();
    }
    else if (textMessage.startsWith("midiTimingInDevice:")) {
        juce::String device = textMessage.substring(19);
        midiManager.setActiveMidiInput(device);
    }
    else if (textMessage.startsWith("addNote:")) {
        int c1 = 8;
        int c2 = textMessage.indexOf(c1, ":")+1;
        int c3 = textMessage.indexOf(c2, ":")+1;
        int id = textMessage.substring(c1, c2).getIntValue();
        int inst = textMessage.substring(c2, c3).getIntValue();
        int region = textMessage.substring(c3).getIntValue();
        if (score.count(id) == 0)
        {
            score[id] = std::make_unique<RatNote>(1,1,0);
        }
        std::cout << "RtoE: addNote:" << id << ":" << inst << ":" << region << std::endl;
    }
    else if (textMessage.startsWith("modNote:")) {
        int c1 = 8;
        int c2 = textMessage.indexOf(c1, ":") + 1;
        int c3 = textMessage.indexOf(c2, ":") + 1;
        int id = textMessage.substring(c1, c2).getIntValue();
        juce::String attribute = textMessage.substring(c2, c3);
        if (attribute.compare("inst") == 0)
        {
            score[id]->setInstrument(uint8(textMessage.substring(c3).getIntValue()));
        }
        else if (attribute.compare("voice") == 0)
        {
            score[id]->setVoice(uint8(textMessage.substring(c3).getIntValue()));
        }
        else if (attribute.compare("region") == 0)
        {
            score[id]->setRegion(uint8(textMessage.substring(c3).getIntValue()));
        }
        else if (attribute.compare("time") == 0)
        {
            score[id]->setTime(textMessage.substring(c3).getDoubleValue());
        }
        else if (attribute.compare("dur") == 0)
        {
            score[id]->setDuration(textMessage.substring(c3).getDoubleValue());
        }
        else if (attribute.compare("db") == 0)
        {
            score[id]->setVel(uint8(textMessage.substring(c3).getIntValue()));
        }
        else if (attribute.compare("num") == 0)
        {
            score[id]->setNum(uint32(textMessage.substring(c3).getIntValue()));
        }
        else if (attribute.compare("den") == 0)
        {
            score[id]->setDen(uint32(textMessage.substring(c3).getIntValue()));
        }
        std::cout << "RtoE: modNote" << std::endl;
    }
    else if (textMessage.startsWith("delNote:")) {
        uint32 id = uint32(textMessage.substring(8).getIntValue());
        deleteBuffer[id] = std::move(score[id]);
        score.erase(id);
        std::cout << "RtoE: delNote" << std::endl;
    }
    else if (textMessage.startsWith("undelNote:")) {
        uint32 id = uint32(textMessage.substring(10).getIntValue());
        score[id] = std::move(deleteBuffer[id]);
        deleteBuffer.erase(id);
        std::cout << "RtoE: undelNote" << std::endl;
    }
    else if (textMessage.startsWith("definitiveDelNote:")) {
        uint32 id = uint32(textMessage.substring(18).getIntValue());
        score.erase(id);
        std::cout << "RtoE: definitiveDelNote" << std::endl;
    }
    else if (textMessage.startsWith("addRegion:")) {
        std::cout << "RtoE: addRegion" << std::endl;
    }
    else if (textMessage.startsWith("modRegion:")) {
        std::cout << "RtoE: modRegion" << std::endl;
    }
    else if (textMessage.startsWith("addInst:")) {
        std::cout << "RtoE: addInst" << std::endl;
    }
    else if (textMessage.startsWith("unAddInst")) {
        std::cout << "RtoE: unAddInst" << std::endl;
    }
    else if (textMessage.startsWith("addOut:")) {
        std::cout << "RtoE: addOut" << std::endl;
    }
    else if (textMessage.startsWith("unaddRegion:")) {
        std::cout << "RtoE: unaddRegion" << std::endl;
    }
    else if (textMessage.startsWith("resetAll")) {
        score.clear();
        deleteBuffer.clear();
        std::cout << "RtoE: resetAll" << std::endl;
    }
    juce::MemoryBlock checker = msg;
    int a = 0;
//    std::cin >> a;
}

void RatEngine::connectionMade()
{

}

void RatEngine::connectionLost()
{

}

void RatEngine::addNote(int id)
{
    if (score.count(id)==0)
    {

    }
}

int RatEngine::getTonalCenter()
{
    //return RatEngine::tonalCenter;
}

void RatEngine::setTonalCenter(int tc=60)
{
    //RatEngine::tonalCenter = tc;
}

