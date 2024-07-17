import jwtDecode from 'jwt-decode';
import { getToken, removeToken } from './token';

export const isTokenExpired = () => {
  const token = getToken();
  if (token) {
    const decodedToken = jwtDecode(token);
    return decodedToken.exp * 1000 < Date.now();
  }
  return true;
};

export const logout = () => {
  removeToken();
  window.location.href = '/login';
};