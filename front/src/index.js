import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import AuthContext from './Context';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import axios from 'axios'; 

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
});

axios.defaults.baseURL = 'http://131.159.192.72:5000/http';
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
axios.defaults.headers.post['Access-Control-Allow-Origin'] = '*';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <ThemeProvider theme={darkTheme}>
      <AuthContext>
        <App/>  
      </AuthContext>
    </ThemeProvider>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
