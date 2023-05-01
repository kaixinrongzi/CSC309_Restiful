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
import {LogIn, LogOut} from './login.js'
import Profile from './profile.js'
import Hotels from './hotel.js'
import MyBookings from './bookings.js'
import Layout from './layout.js'
import MyPropertyReservations from './propertyreservation.js'
import Reservation from './components/Reservation'
import {NotificationViewAll, NotificationView} from './notification.js'
import {CommentAdd, CommentView, CommentsView, CommentsforHotelView} from './comment.js'
import {ReplyAdd, ReplyView} from './reply.js'
import React, {Suspense} from 'react';
import { BrowserRouter, NavLink, redirect, Routes, Route, useRoutes} from "react-router-dom";

function App() {

    return <BrowserRouter>
        <Routes>
            <Route path='/'  element={<Layout/>}>
                <Route path='accounts/register' element={<Register/>}></Route>
                <Route path='accounts/login' element={<LogIn/>}></Route>
                <Route path='accounts/profile' element={<Profile/>}></Route>
                <Route path='hotels/view' element={<Hotels/>}></Route>
                <Route path='hotels/reservations/list/guest' element={<MyBookings/>}></Route>
                <Route path='hotels/reservations/list/host' element={<MyPropertyReservations/>}></Route>
                <Route path='hotels/reservations/create' element={<Reservation hotel_id={8} price={100}/>}></Route>
                <Route path='hotels/notifications/view' element={<NotificationViewAll/>}></Route>
                <Route path='hotels/notification/view' element={<NotificationView/>}></Route>
                <Route path='hotels/comments/view' element={<CommentsView/>}></Route>
                <Route path='hotels/comment/view' element={<CommentView/>}></Route>
                <Route path='hotels/reply/view' element={<ReplyView/>}></Route>
                <Route path='hotels/comment/add' element={<CommentAdd/>}></Route>
                <Route path='hotels/hotel/comments/view' element={<CommentsforHotelView/>}></Route>
                <Route path='hotels/reply/add' element={<ReplyAdd/>}></Route>
                <Route path='accounts/logout' element={<LogOut/>}></Route>
            </Route>
        </Routes>
    </BrowserRouter>}

export default App;
