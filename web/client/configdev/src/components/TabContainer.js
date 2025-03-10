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
import { Tabs, Tab } from "@material-ui/core";

export default class TabContainer extends React.Component {
  render() {
    const { classes, labels } = this.props;

    if (!labels) {
      return null;
    }

    const titles = [
      labels.configuration, labels.players, labels.screensavers, labels["radio.playlists"], labels.podcasts, 
      labels.streams, labels.system
    ]
    return (
      <Tabs
        value={this.props.tabIndex}
        onChange={this.props.handleTabChange}
        TabIndicatorProps={{className: classes.tabSelection}}
        variant="scrollable"
        scrollButtons="auto"
      >
        {titles.map((text, index) => (<Tab key={index} label={text} />))}
      </Tabs>
    );
  }
}
