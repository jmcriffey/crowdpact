import React from 'react';


class LandingBanner extends React.Component {
    constructor(...args) {
        super(...args);

        this.onSignup = this.onSignup.bind(this);
    }

    render() {
        return (
            <div className="landing-banner">
                <div className="container">
                    {this.renderAbout()}
                    {this.renderSignup()}
                </div>
            </div>
        );
    }

    renderAbout() {
        return (
            <div className="landing-about">
                <div className="about-large">
                    {this.props.pageData.get('landing_text_large')}
                </div>
                <div className="about-small">
                    {this.props.pageData.get('landing_text_small')}
                </div>
            </div>
        );
    }

    renderSignup() {
        return (
            <div className="landing-signup">
                <form className="landing-signup-form" ref="signupForm">
                    <input placeholder="Pick a username" name="name" ref="name" type="text" />
                    <input placeholder="Your email" ref="email" type="text" />
                    <input placeholder="Create a password" ref="password1" type="password" />
                    <input placeholder="Re-enter password" ref="password2" type="password" />

                    <button onClick={this.onSignup} type="button">Signup for CrowdPact</button>
                </form>
            </div>
        );
    }

    onSignup() {
        console.log('onSignup');
    }
}

export default LandingBanner;
