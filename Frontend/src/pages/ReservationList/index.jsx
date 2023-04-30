import { useState, useEffect } from 'react';
import Table from '../ReservationTable'
import axios from 'axios';
import {useDispatch, useSelector} from 'react-redux'
import TableGuest from '../ReservationTableGuest';
import './style.css'
import { useNavigate } from 'react-router-dom';

const Reservations = () => {
    const [reservations, setReservations] = useState([])
    const [query, setQuery] = useState({user_type: "host", state: 'P', page: 1})
    const [totalPages, setTotalPages] = useState(1)

    const token = localStorage.getItem('token')

    let navigate = useNavigate()
    const change = (reservation_id, state) => {
        if (state === 'A') {
            axios.put(`http://localhost:8000/hotels/reservation/${reservation_id}/approve/`, {},
                    {headers: {'Authorization': 'Bearer ' + token}}
            )
            .catch(error => console.log(error))
            console.log('30', reservation_id)
            // navigate('#')
            window.location.reload()
        }
        else if (state === 'D') {
            axios.put(`http://localhost:8000/hotels/reservation/${reservation_id}/deny/`, {},
                    {headers: {'Authorization': 'Bearer ' + token}}
            )
            .catch(error => console.log(error))
            // navigate('#')
            window.location.reload()
        }
        else if (state === 'Ca') {
            axios.put(`http://localhost:8000/hotels/reservation/${reservation_id}/approvecancel/`, {},
                    {headers: {'Authorization': 'Bearer ' + token}}
            )
            .catch(error => console.log(error))
            // navigate('#')
            window.location.reload()
        }
        else if (state === 'T') {
            axios.put(`http://localhost:8000/hotels/reservation/${reservation_id}/terminate/`, {},
                    {headers: {'Authorization': 'Bearer ' + token}}
            )
            .catch(error => console.log(error))
            console.log("53", token)
            // navigate('#')
            window.location.reload()
        }
        else if (state === 'PC') {
            axios.put(`http://localhost:8000/hotels/reservation/${reservation_id}/cancel/`, {},
                    {headers: {'Authorization': 'Bearer ' + token}}
            )
            .catch(error => console.log(error))
            // navigate('#')
            window.location.reload()
        }
        else if (state === 'F') {
            axios.put(`http://localhost:8000/hotels/reservation/${reservation_id}/finish/`, {},
                    {headers: {'Authorization': 'Bearer ' + token}}
            )
            .catch(error => console.log(error))
            // navigate('#')
            window.location.reload()
        }
    }

    useEffect(() => {
        
    }, [navigate])

    useEffect(() => {
        const {user_type, state, page} = query;
        // fetch from reservation list
        axios.get(`http://localhost:8000/hotels/reservation/list/?user_type=${user_type}&state=${state}&page=${page}`, 
                {headers: {'Authorization': 'Bearer ' + token}}
        )
        .then(response => {
                            if (response.status === 200) {
                                console.log(response.data)
                                return response.data
                            } else {
                                throw Error("Get error when fetching data")
                            }
                        })
        .then(data => {
            setReservations(data.results);
            setTotalPages(Math.max(Math.ceil(data.count / 2), 1));
        })
        .catch(error => console.log(error))
    }, [query])

    return <>
    <main>
    <p>
        <label for='user_type'>Choose User Type:</label>
        <select 
            id="user_type" 
            value={query.user_type}
            onChange={event => setQuery({...query, user_type: event.target.value, page:1})}>
            <option key="guest" value="guest">Guest</option>
            <option key="host" value='host'>Host</option>
        </select>
    </p>
    <p>
        <label for="state">Choose state: </label>
        <select id="state"
                value={query.state}
                onChange={event => setQuery({...query, state: event.target.value, page: 1})}>
            <option key="P" value="P">Pending</option>
            <option key="A" value="A">Approved</option>
            <option key="Ca" value="Ca">Cancelled</option>
            <option key="D" value="D">Denied</option>
            <option key="E" value="E">Expired</option>
            <option key="P" value="T">Terminated</option>
            <option key="P" value="F">Finished</option>
        </select>
    </p>
    {(query.user_type === 'host')
      ? <Table reservations={reservations} change={change}/>
      : <TableGuest reservations={reservations} change={change}/>}
    <p>
        {query.page > 1
            ? <button onClick={() => setQuery({...query, page: query.page - 1})}>Previous</button>
            : <></>
        }
        {query.page < totalPages
            ? <button onClick={() => setQuery({...query, page: query.page + 1})}>Next</button>
            : <></>
        }
    </p>
    <p>Page {query.page} out of {totalPages}</p>
    </main>
    </>
}
export default Reservations