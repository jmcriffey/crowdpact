import React from 'react';


class LandingBanner extends React.Component {
    constructor(...args) {
        super(...args);

        this.onLogin = this.onLogin.bind(this);
        this.onSignup = this.onSignup.bind(this);
    }

    render() {
        return (
            <div className="landing-banner">
                <div className="container">
                    {this.renderAbout()}
                    {this.renderForm()}
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

    renderForm() {
        return (
            this.props.data.get('showLogin') ?
            this.renderLogin() :
            this.renderSignup()
        );
    }

    renderLogin() {
        return (
            <div className="landing-login">
                <form className="landing-login-form" ref="loginForm">
                    <input
                    name="csrfmiddlewaretoken"
                    type="hidden"
                    value={this.props.pageData.get('csrf_token')} />

                    <input placeholder="Your username" name="username" ref="username" type="text" />
                    <input placeholder="Your password" name="password" ref="password" type="password" />

                    <button onClick={this.onLogin} type="button">Login to CrowdPact</button>
                </form>
            </div>
        );
    }

    renderSignup() {
        return (
            <div className="landing-signup">
                <form className="landing-signup-form" ref="signupForm">
                    <input
                    name="csrfmiddlewaretoken"
                    type="hidden"
                    value={this.props.pageData.get('csrf_token')} />

                    <input placeholder="Pick a username" name="username" ref="username" type="text" />
                    <input placeholder="Your email" name="email" ref="email" type="text" />
                    <input placeholder="Create a password" name="password" ref="password" type="password" />

                    <button onClick={this.onSignup} type="button">Signup for CrowdPact</button>
                </form>
            </div>
        );
    }

    onLogin() {
        fetch(this.props.pageData.get('login_url'), {
            body: new FormData(React.findDOMNode(this.refs.loginForm)),
            method: 'POST'
        })
        .then(res => res.json())
        .then(data => {
            if (data.next) {
                window.location = data.next;
            }
        })
        .catch(err => console.error(err));
    }

    onSignup() {
        fetch(this.props.pageData.get('signup_url'), {
            body: new FormData(React.findDOMNode(this.refs.signupForm)),
            method: 'POST'
        })
        .then(res => res.json())
        .then(data => {
            if (data.next) {
                window.location = data.next;
            }
        })
        .catch(err => console.error(err));
    }
}

export default LandingBanner;
