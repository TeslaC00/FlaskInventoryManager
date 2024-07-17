import React from 'react';
import { Route, Redirect } from 'react-router-dom';
import { getToken } from '../utils/token';

const PrivateRoute = ({ component: Component, ...rest }) => {
  const token = getToken();
  return (
    <Route
      {...rest}
      render={props =>
        token ? (
          <Component {...props} />
        ) : (
          <Redirect to="/login" />
        )
      }
    />
  );
};

export default PrivateRoute;