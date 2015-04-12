import React from 'react';

import LandingBanner from './LandingBanner';
import LandingHeader from './LandingHeader';
import LandingPacts from './LandingPacts';


class LandingApp extends React.Component {
    constructor(...args) {
        super(...args);

        this.state = {};
    }

    render() {
        return (
            <div className="landing-app">
                <LandingHeader {...this.props} {...this.state} />
                <LandingBanner {...this.props} {...this.state} />
                <LandingPacts {...this.props} {...this.state} />
            </div>
        );
    }
}

export default LandingApp;
