import {fromJS} from 'immutable';
import React from 'react';
import 'whatwg-fetch';

import LandingApp from './apps/landing/components/LandingApp';
import PactHomeApp from './apps/pact/home/components/PactHomeApp';


const APPS = {
    LandingApp,
    PactHomeApp
};

global.CrowdPact = {
    render(appName, pageData, mountNode) {
        const Component = APPS[appName]; //eslint-disable-line

        React.render(<Component pageData={fromJS(pageData)} />, mountNode); //eslint-disable-line
    }
};
