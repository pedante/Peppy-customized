/* Copyright 2019-2021 Peppy Player peppy.player@gmail.com
 
This file is part of Peppy Player.
 
Peppy Player is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
 
Peppy Player is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
 
You should have received a copy of the GNU General Public License
along with Peppy Player. If not, see <http://www.gnu.org/licenses/>.
*/

import React from "react";
import Clock from "../screensavers/Clock";
import Logo from "../screensavers/Logo";
import Lyrics from "../screensavers/Lyrics";
import Weather from "../screensavers/Weather";
import Random from "../screensavers/Random";
import Slideshow from "../screensavers/Slideshow";

export const screensaversSections = [
  "clock", "logo", "lyrics", "peppyweather", "random", "slideshow", "peppymeter", "spectrum"
];

export default class ScreensaversTab extends React.Component {
  render() {
    if (!this.props.screensavers) {
      return null;
    }

    const { classes, labels, topic, updateState, screensavers } = this.props;
    const p = screensavers[screensaversSections[topic]];

    return (
      <main className={classes.content}>
        {topic === 0 && <Clock labels={labels} classes={classes} values={p} updateState={updateState}/>}
        {topic === 1 && <Logo labels={labels} classes={classes} values={p} updateState={updateState}/>}
        {topic === 2 && <Lyrics labels={labels} classes={classes} values={p} updateState={updateState}/>}
        {topic === 3 && <Weather labels={labels} classes={classes} values={p} updateState={updateState}/>}
        {topic === 4 && <Random labels={labels} classes={classes} values={p} updateState={updateState}/>}
        {topic === 5 && <Slideshow labels={labels} classes={classes} values={p} updateState={updateState}/>}
      </main>
    );
  }
}
