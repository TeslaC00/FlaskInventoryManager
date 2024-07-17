import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import PrivateRoute from './components/PrivateRoute';
import Home from 'app/templates/base.html';
import Login from 'app/templates/auth/login.html';
import { isTokenExpired, logout } from './utils/auth';

const App = () => {
  if (isTokenExpired()) {
    logout();
  }

  return (
    <Router>
      <Switch>
        <Route path="/login" component={login} />
        <PrivateRoute path="/" component={base} />
      </Switch>
    </Router>
  );
};

export default App;