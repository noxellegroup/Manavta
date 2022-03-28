import React from 'react'
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';
import Home from './Home';
import Login from './Login';

export default function RouterPage() {
  return (
    <div>
        <Router>
            <Switch>
                <Route path="/" exact component={Home}/>
                <Route path="/Login" exact component={Login}/>
            </Switch>
        </Router>
    </div>
  )
}
