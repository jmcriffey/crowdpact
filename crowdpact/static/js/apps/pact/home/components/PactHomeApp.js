import React from 'react';


class PactHomeApp extends React.Component {
    render() {
        return (
            <div>
                <h1>
                    Welcome to CrowdPact {this.props.pageData.get('user').get('username')}!
                </h1>
                <a href={this.props.pageData.get('logout_url')}>Logout</a>
            </div>
        );
    }
}

export default PactHomeApp;
