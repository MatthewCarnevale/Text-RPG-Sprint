import * as React from 'react';
import * as ReactDOM from 'react-dom';

import {App} from './App.jsx'; 
import {MainUI} from './MainUI.jsx';
import {CreationUI} from './CharCreation.jsx'
import {AchievementUI} from './AchievementMenu.jsx'


const loginElement = document.getElementById('login');
if(loginElement){
    ReactDOM.render(<App />, document.getElementById('login'));
}

const creationElement = document.getElementById('create_ui'); 
if(creationElement){
    ReactDOM.render(<CreationUI />, document.getElementById('create_ui'));
}

const achievementElement = document.getElementById('achievement_ui');
if(achievementElement){
    ReactDOM.render(<AchievementUI />, document.getElementById('achievement_ui'));
}

const uiElement = document.getElementById('main_ui');
if(uiElement){
    ReactDOM.render(<MainUI />, document.getElementById('main_ui'))
}

