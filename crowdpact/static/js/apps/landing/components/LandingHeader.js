import React from 'react';

import debounce from 'lodash/function/debounce';


class LandingHeader extends React.Component {
    constructor(...args) {
        super(...args);

        this.onClickLogin = this.onClickLogin.bind(this);
        this.onSearch = debounce(this.onSearch.bind(this), 400);
    }

    render() {
        return (
            <div className="landing-header">
                <div className="container">
                    <div className="landing-title">
                        <a href="/">CrowdPact</a>
                    </div>
                    <div className="landing-search">
                        <input onChange={this.onSearch} placeholder="Find pacts" type="text" />
                    </div>
                    <div className="landing-buttons">
                        <button onClick={this.onClickLogin} type="button">Login</button>
                    </div>
                </div>
            </div>
        );
    }

    onClickLogin() {
        console.log('onClickLogin');
    }

    onSearch() {
        console.log('onSearch');
    }
}

export default LandingHeader;
