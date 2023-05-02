import { Link } from "react-router-dom"

const TableGuest = (props) => {

    
    const reservations = props.reservations

    return <table>
        <thead>
            <th>Start Date</th>
            <th>End Date</th>
            <th>State</th>
            <th>Number of Guests</th>
            <th>Guest</th>
            <th>Hotel</th>
            <th>Edit</th>
        </thead>
        <tbody>
            {
                reservations.map(reservation => (
                    <tr key={reservation.id}>
                        <td>{reservation.start_date}</td>
                        <td>{reservation.end_date}</td>
                        <td>{reservation.state}</td>
                        <td>{reservation.guests}</td>
                        <td>{reservation.guest}</td>
                        <td>{reservation.hotel}</td>
                        <td>
                            {
                                (reservation.state === 'A') && (
                                    <p>
                                    <button onClick={() => {
                                        alert("You will Cancel the reservation")
                                        props.change(reservation.id, 'PC')
                                    }}>Cancel</button>
                                    <button onClick={() => {
                                        alert("you want to finish the reservation")
                                        props.change(reservation.id, 'F')
                                    }}>Finish</button>
                                    </p>
                                )
                             
                            }
                            {
                                (reservation.state === 'F') && (
                                    <p>
                                        <Link to='/hotels/comment/add'>
                                            <button>Comment</button>
                                        </Link>
                                    </p>
                                )
                            }
                            
                        </td>
                    </tr>
            ))}
        </tbody>
    </table>
}
export default TableGuest
