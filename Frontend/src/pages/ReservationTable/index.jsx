const Table = (props) => {
    const reservations = props.reservations
    const change = props.change
    return <>
    <table>
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
                        {reservation.state === 'P' && (
                            <p>
                                <button onClick={() => {
                                    alert("You will approve the reservation")
                                    props.change(reservation.id, 'A')
                                }}>Approve</button>
                                <button onClick={() => {
                                    alert("you want to deny the reservation")
                                    props.change(reservation.id, 'D')
                                }}>Deny</button>
                            </p>
                        )}
                        {reservation.state === 'PC' && (
                            <p>
                                <button onClick={() => {
                                    alert("You want to approve the cancellation")
                                    props.change(reservation.id, 'Ca')
                                }}>Approve Cancel</button>
                                <button onClick={() => {
                                    alert("You want to deny the cancellation")
                                    props.change(reservation.id, 'A')
                                }}>Deny Cancel</button>
                            </p>
                        )}
                        {reservation.state === 'A' && (
                            <p>
                                <button onClick={() => {
                                    alert("You want to terminate the reservation.")
                                    props.change(reservation.id, 'T')
                                }}>Terminate</button>
                            </p>
                        )}
                        </td>
                    </tr>
            ))}
        </tbody>
    </table>
    </>
}
export default Table