import {useLocation, NavLink, BrowserRouter, Routes, Route, Outlet} from 'react-router-dom'

export default function Layout(){
    return <><header>
           <ul>
             <a href="index.html"><li>Restiful, bring the world to you</li></a>
             <li>
                 <NavLink to='/hotels/search'>Travelling to</NavLink>
                 <div class="travel_subdiv">
                     <date></date>
                 </div>
             </li>
             <li>
                <details>
                    <summary>earth</summary>

                        <ul class="submenu">
                         <li>
                              {/*<a href='/accounts/register'>Sign Up</a>*/}
                              <NavLink to='/accounts/register'>Sign Up</NavLink>
                         </li>
                         <li>
                              {/*<a href='/accounts/login'>Sign In</a>*/}
                              <NavLink to='/accounts/login'>Sign In</NavLink>
                         </li>
                         <li>
                              {/*<a href='/accounts/myaccount'>My Account</a>*/}
                              <NavLink to='/accounts/myaccount' >My Account</NavLink>
                              <ul>
                                <li><NavLink to='/accounts/profile' >My Profile</NavLink></li>
                                <li><NavLink to='/hotels/view' >My Hotels</NavLink></li>
                                <li><NavLink to='/hotels/reservations/list/guest' >My Bookings</NavLink></li>
                                <li><NavLink to='/hotels/reservations/list/host' >History Reservations</NavLink></li>
                                <li><NavLink to='/hotels/reservations/create' >Create reservation</NavLink></li>
                                <li><NavLink to='/hotels/notifications/view' >My Notifications</NavLink></li>
                                <li><NavLink to='/hotels/comments/view' >My Comments</NavLink></li>
                                <li><NavLink to='/accounts/logout' > Log Out</NavLink></li>
                                {/*<li><NavLink to='/hotels/availability/add' > Hotel Availability</NavLink></li>*/}
                              </ul>
                         </li>
                        </ul>
                </details>
             </li>
          </ul>
        </header>
        <Outlet /></>
}
