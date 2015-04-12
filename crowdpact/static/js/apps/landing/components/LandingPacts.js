import React from 'react';


class LandingPacts extends React.Component {
    render() {
        return (
            <div className="landing-pacts">
                <div className="container">
                    {this.renderPacts()}
                </div>
            </div>
        );
    }

    renderPacts() {
        return this.props.pageData.get('pacts').map((pact, i) => {
            let items = pact.get('items').map((item, j) => {
                return (
                    <div className="pact-item" key={j}>
                        {item.get('name')}
                    </div>
                );
            });

            return (
                <div className="pact-section" key={i}>
                    <div className="section-header">{pact.get('title')}</div>
                    {items}
                </div>
            );
        });
    }
}

export default LandingPacts;
