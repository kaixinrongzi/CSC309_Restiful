import { useState, useEffect } from 'react'
import axios from 'axios'
import './style.css'
import * as images from '../../assets/images';

function Property(props) {
    const [hotel, setHotel] = useState("");
    const hotel_id = props.hotel_id

    useEffect(() => {
        axios.get(`http://localhost:8000/hotels/${hotel_id}/view/`)
        .then(response => {
            setHotel(response.data);
            console.log(response.data);
        })
        .catch(error => {
            console.log(error);
        });
    }, [])
    
    function isUrl(str) {
        const pattern = new RegExp('^(https?:\\/\\/)?' + // protocol
          '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|' + // domain name
          '((\\d{1,3}\\.){3}\\d{1,3}))' + // OR ip (v4) address
          '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*' + // port and path
          '(\\?[;&a-z\\d%_.~+=-]*)?' + // query string
          '(\\#[-a-z\\d_]*)?$', 'i'); // fragment locator
        return pattern.test(str);
    }

    const image1 = hotel.image1
    const image2 = hotel.image2
    const image3 = hotel.image3
    console.log("33", image1)
    // console.log("34", hotel)

    // const image2 = "https://freepngimg.com/thumb/mario/20698-7-mario-transparent-background.png"
    const Display = ({ imageURL }) => {
        return (
            <>
                {isUrl(imageURL) && (
                    <>
                        {console.log("no!")}
                        <img src={`${imageURL}`} alt="image" width="300" height="500"/>
                    </>
                )}
                {!!imageURL && (
                    <>
                        {console.log("yes!")}
                        <img src={require(`../../assets/images/${imageURL}`)} alt="image" width="300" height="500" />
                    </>
                )}
            </>
        );
    };
    
    return <>
    <main>
    <table>
        <thead>
            <th>Property_name</th>
            <th>Description</th>
            <th>Owner</th>
            <th>Rating</th>
            <th>Capacity</th>
            <th>Beds</th>
            <th>Baths</th>
            <th>is_active</th>
        </thead>
        <tbody>
            <td>{hotel.name}</td>
            <td>{hotel.description}</td>
            <td>{hotel.owner}</td>
            <td>{hotel.rating}</td>
            <td>{hotel.capacity}</td>
            <td>{hotel.beds}</td>
            <td>{hotel.baths}</td>
            <td>{hotel.is_active}</td>
        </tbody>
    </table>
    <Display imageURL={image1} />
    <Display imageURL={image2} />
    <Display imageURL={image3} />
    
    {/* <img src={`${image}`} alt="image" width="300" height="500"/> */}
    </main>
    </>
}
export default Property
