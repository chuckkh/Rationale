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
					  
#include "RatRegion.h"
#include <vector>

RatRegion::RatRegion(uint32 num_, uint32 den_, double centOffset_ = 0)
{
	setNum(num_);
	setDen(den_);
	setCentOffset(centOffset_);
}


void RatRegion::setNum(uint32 num_)
{
	num = num_;
}
void RatRegion::setDen(uint32 den_)
{
	den = den_;
}
void RatRegion::setCentOffset(double centOffset_)
{
	centOffset = centOffset_;
}
uint32 RatRegion::getNum()
{
	return num;
}
uint32 RatRegion::getDen()
{
	return den;
}
double RatRegion::getCentOffset()
{
	return centOffset;
}
