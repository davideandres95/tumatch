import './App.css';
import ApplicationBar from './ApplicationBar';
import Homepage from './Homepage';
import React from "react";
import {getContext} from './Context';
import Auth from './Auth';
import {
  BrowserRouter as Router,
  Routes,
  Route
} from "react-router-dom";


function App (props) {
  const {isAuth,} = React.useContext(getContext());
  return (
    <Router>
      <ApplicationBar/>

      <Routes>
        <Route path="/" element={
            isAuth ? <Homepage/> : <Auth/>
        }/>
        <Route path="/" element={
          isAuth && <Homepage/>
        }/>
      </Routes>
    </Router>
  );
}

export default App;
