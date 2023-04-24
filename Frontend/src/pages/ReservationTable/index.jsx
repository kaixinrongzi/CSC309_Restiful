import { Link } from 'react-router-dom';

const Table = ({reservations}) => {
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
                            {reservation.state !== 'F'
                                ? <Link to="/reservations/${reservation.id}/">Change status</Link>
                                : <></>
                            }
                        </td>
                    </tr>
            ))}
        </tbody>
    </table>
}
export default Table