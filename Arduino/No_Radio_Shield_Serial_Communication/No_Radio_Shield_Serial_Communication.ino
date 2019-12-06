/* trackuino copyright (C) 2010  EA5HAV Javi
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
 */

// Trackuino custom libs
#include "config.h"
#include "afsk_avr.h"
#include "aprs.h"
#include "pin.h"
#include "power.h"
#include <Arduino.h>

// Module variables
static int32_t next_aprs = 3000;


void setup()
{
  Serial.begin(9600);
  afsk_setup();

}
int count = 0;
void loop()
{
  if(Serial.available()){
    int r = 1;
    r = Serial.read() - '0';
    if ((int32_t) (millis() - next_aprs) >= 0) {
      aprs_send("##" + String(r));
      next_aprs += APRS_PERIOD * 1000L;
      while (afsk_flush()) {
        power_save();
      }
    } else {
      // Discard GPS data received during sleep window
      while (Serial.available()) {
        Serial.read();
      }
    }
  }
  power_save(); // Incoming GPS data or interrupts will wake us up
}
