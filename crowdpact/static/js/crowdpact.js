import React from 'react';

import AccountSignupApp from './apps/account/components/AccountSignupApp';


const APPS = {
    AccountSignupApp
};

global.CrowdPact = {
    render(appName, mountNode) {
        const Component = APPS[appName]; //eslint-disable-line

        React.render(<Component />, mountNode); //eslint-disable-line
    }
};
