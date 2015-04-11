import React from 'react';

import PactApp from './components/PactApp';


function renderPactApp(mountNode) {
    React.render(<PactApp />, mountNode);
}

global.renderPactApp = renderPactApp;
