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
    for (juce::MidiDeviceInfo& dev : iDevices) {
        auto name = dev.name.dropLastCharacters(std::max(0, dev.name.length() - 56));
        sendString(name);
//        sendString(dev.identifier.dropLastCharacters(std::max(0, dev.identifier.length()-56)));
        midiInDevices[name] = dev.identifier;
    }
    sendString("MidiInEnd");
}

void RatEngine::sendAvailableMidiOutDevices()
{
    std::cout << "Getting Available MIDI Out Devices..." << std::endl;
    auto oDevices = MidiOutput::getAvailableDevices();
    sendString("MidiOutBegin");
    for (juce::MidiDeviceInfo& dev : oDevices) {
        auto name = dev.name.dropLastCharacters(std::max(0, dev.name.length() - 56));
//        sendString(dev.identifier.dropLastCharacters(std::max(0, dev.identifier.length()-56)));
        sendString(name);
        midiOutDevices[name] = dev.identifier;
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
}

void RatEngine::endItAll() {
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