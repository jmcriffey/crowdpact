import {fromJS} from 'immutable';
import React from 'react';
import 'whatwg-fetch';

import LandingApp from './apps/landing/components/LandingApp';


const APPS = {
    LandingApp
};

global.CrowdPact = {
    render(appName, pageData, mountNode) {
        const Component = APPS[appName]; //eslint-disable-line

        React.render(<Component pageData={fromJS(pageData)} />, mountNode); //eslint-disable-line
    }
};
