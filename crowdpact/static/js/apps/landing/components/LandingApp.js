import React from 'react';

import LandingBanner from './LandingBanner';
import LandingHeader from './LandingHeader';
import LandingPacts from './LandingPacts';
import LandingStore from '../stores/LandingStore';


class LandingApp extends React.Component {
    constructor(...args) {
        super(...args);

        this.state = {data: LandingStore.data};
    }

    componentWillMount() {
        this.unregister = LandingStore.listen(this.onStoreChange.bind(this));
    }

    componentWillUnmount() {
        this.unregister();
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

    onStoreChange() {
        this.setState({data: LandingStore.data});
    }
}

export default LandingApp;
