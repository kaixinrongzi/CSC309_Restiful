import { useState, useEffect } from 'react';
import Table from '../ReservationTable'
import axios from 'axios';
import {useDispatch, useSelector} from 'react-redux'
import TableGuest from '../ReservationTableGuest';

const Reservations = () => {
    const [reservations, setReservations] = useState([])
    const [query, setQuery] = useState({user_type: "host", state: "", page: 1})
    const [totalPages, setTotalPages] = useState(1)

    const token = localStorage.getItem('token')

    const change = (reservation_id, state) => {
        setReservations(reservations.map(reservation => {
            if (reservation.id === reservation_id) {
                reservation.state = state;
            }
            return reservation;
        }))
    }

    useEffect(() => {
        const {state, page} = query;
        // fetch from reservation list
        axios.get(`http://localhost:8000/hotels/reservation/list/?user_type=${user_type}&state=${state}&page=${page}`, 
                {headers: {'Authorization': 'Bearer' + token}}
        )
        .then(response => {
                            if (response.ok) {
                                return response.json()
                            } else {
                                throw Error("Get error when fetching data")
                            }
                        })
        .then(json => {
            setReservations(json.results);
            setTotalPages(Math.max(Math.ceil(json.count / 2), 1));
        }, [query])
        .catch(error => console.log(error))
    })

    return <>
    <p>
        <label>Choose User Type:
            <select 
                id="user_type" 
                value={query.user_type}
                onChange={event => setQuery({...query, user_type: event.target.value, page:1})}>
                <option key="guest" value="guest">Guest</option>
                <option key="host" value='host'>Host</option>
            </select>
        </label>
    </p>
    {/* <Link to='/reservations/guest'>Guest mode</Link> */}
    <p>
        <label>Choose state:
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
    </label>
    </p>
    {(user_type === 'host')
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
    </>
}
export default Reservations