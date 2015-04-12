import {fromJS} from 'immutable';
import Reflux from 'reflux';

import LandingActions from '../actions/LandingActions';


let data = fromJS({showLogin: false});

export default Reflux.createStore({
    listenables: [LandingActions],

    onToggleShowLogin() {
        data = data.set('showLogin', !data.get('showLogin'));
        this.trigger();
    },

    get data() {
        return data;
    }
});
