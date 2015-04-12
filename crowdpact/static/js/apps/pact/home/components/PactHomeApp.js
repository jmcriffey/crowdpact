import React from 'react';


class PactHomeApp extends React.Component {
    render() {
        console.log(this.props.pageData.get('user'));

        return (
            <h1>Welcome Home!</h1>
        );
    }
}

export default PactHomeApp;
