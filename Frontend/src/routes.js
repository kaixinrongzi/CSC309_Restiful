import React, {Suspense} from 'react';
import { BrowserRouter, Routes, Route, useRoutes} from "react-router-dom";
//import Home from "./home";
import App from './App';
import Register from './Register.js'
//import Login from './login.js'
import Profile from './profile.js'
//import UserLogIn from "./pages/login";
// import { User, UserItem } from '';

//const User = React.lazy(()=>import("./user"))
//const UserItem = React.lazy(()=>import("./userItem"))

export default
<BrowserRouter>
<Suspense fallback={<div>loading...</div>}>
    <Routes>
        <Route index element={<App/>}></Route>
        <Route path='/register' element={<Register/>}></Route>
        <Route path='/profile' element={<Profile props/>}></Route>
    </Routes>
</Suspense>
</BrowserRouter>