import * as React from 'react';
import * as ReactDOM from 'react-dom';

import {App} from './App.jsx'; 
import {MainUI} from './MainUI.jsx';
import {AchievementUI} from './AchievementMenu.jsx'
import {CreationUI} from './CharCreation.jsx';
import {Options} from './OptionMenu.jsx';
import {About} from './AboutUs.jsx';

const loginElement = document.getElementById('login');
if(loginElement){
    ReactDOM.render(<App />, loginElement);
}

const creationElement = document.getElementById('create_ui'); 
if(creationElement){
    ReactDOM.render(<CreationUI />, creationElement);
}

const achievementElement = document.getElementById('achievement_ui');
if(achievementElement){
    ReactDOM.render(<AchievementUI />, document.getElementById('achievement_ui'));
}

const uiElement = document.getElementById('main_ui');
if(uiElement){
    ReactDOM.render(<MainUI />,  uiElement)
}

const optionElement = document.getElementById('options');
if(optionElement){
    ReactDOM.render(<Options />, optionElement)
}

const landingElement = document.getElementById('about_page')
if(landingElement){
    ReactDOM.render(<About />, landingElement)
}