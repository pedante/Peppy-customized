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

import React from 'react';
import {FormControl} from '@material-ui/core';
import Factory from "../Factory";

export default class LanguagesMenu extends React.Component {
  render() {
    const { params, updateState, languages, language } = this.props;

    if (!languages) {
      return null;
    }

    let keys = [];
    let translations = [];

    languages.forEach((lang) => {
      if (lang.name === language) {
        keys = Object.keys(lang.translations);
        translations = lang.translations;
      }
    })

    return (
        <FormControl>
          {keys.map((v) => {return Factory.createCheckbox(v, params, updateState, translations)})}
        </FormControl>
    );
  }
}
