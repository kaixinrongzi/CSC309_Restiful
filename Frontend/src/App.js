import logo from './logo.svg';
//import './App.css';
import './css/style1.css'
import './css/style2.css'
import './css/index.css'
import './css/bulma/bulma.css'
import './css/bulma/bulma.css.map'
import './css/bulma/bulma.min.css'
import './css/bulma/bulma-rtl.css'
import './css/bulma/bulma-rtl.css.map'
import './css/bulma/bulma-rtl.min.css'
import Register from './Register.js'
import LogIn from './login.js'
import React, {Suspense} from 'react';
import Reservations from './pages/ReservationList';
//import { BrowserRouter, NavLink, redirect, Routes, Route, useRoutes} from "react-router-dom";

function App() {

  return (
      <>
      <header>
           <ul>
             <a href="index.html"><li>Restiful, bring the world to you</li></a>
             <li>
                 Travelling to
                 <div class="travel_subdiv">
                     <date></date>
                 </div>
             </li>
             <li>
                <details>
                    <summary>earth</summary>

                        <ul class="submenu">
                         <li>
                               <a href='/register'>Sign Up</a>
                         </li>
                         <li>
                              <a href='/login'>Sign In</a>
                         </li>
                         <li><a href="I have a property to post">Post Your Property</a></li>
                         <li><a href="./users/contact.html">Contact Us</a></li>
                        </ul>
                </details>

             </li>
          </ul>
        </header>
        </>);
}

export default App;
